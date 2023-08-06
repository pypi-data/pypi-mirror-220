# -*- coding: utf-8 -*-
# Copyright 2023, SERTIT-ICube - France, https://sertit.unistra.fr/
# This file is part of sertit-utils project
#     https://github.com/sertit/sertit-utils
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Vectors tools

You can use this only if you have installed sertit[full] or sertit[vectors]
"""
import logging
import os
import re
import shutil
import tarfile
import tempfile
import zipfile
from pathlib import Path
from typing import Any, Generator, Union

import numpy as np
import pandas as pd
from cloudpathlib import AnyPath, CloudPath
from cloudpathlib.exceptions import AnyPathTypeError
from fiona._err import CPLE_AppDefinedError
from fiona.errors import UnsupportedGeometryTypeError

from sertit import files, misc, strings

try:
    import geopandas as gpd
    from shapely import wkt
    from shapely.geometry import MultiPolygon, Polygon, box
except ModuleNotFoundError as ex:
    raise ModuleNotFoundError(
        "Please install 'geopandas' to use the rasters package."
    ) from ex

from sertit.logs import SU_NAME

LOGGER = logging.getLogger(SU_NAME)

WGS84 = "EPSG:4326"

EXT_TO_DRIVER = {
    ".shp": "ESRI Shapefile",
    ".kml": "KML",
    ".kmz": "KMZ",
    ".json": "GeoJSON",
    ".geojson": "GeoJSON",
    ".gml": "GML",
}

SHP_CO_FILES = [".dbf", ".prj", ".sbn", ".sbx", ".shx", ".sld"]


def corresponding_utm_projection(lon: float, lat: float) -> str:
    """
    Find the EPSG code of the UTM projection from a lon/lat in WGS84.

    .. code-block:: python

        >>> corresponding_utm_projection(lon=7.8, lat=48.6)  # Strasbourg
        'EPSG:32632'

    Args:
        lon (float): Longitude (WGS84)
        lat (float): Latitude (WGS84)

    Returns:
        str: EPSG string

    """
    # EPSG code begins with 32
    # Then 6 if north, 7 if south -> (np.sign(lat) + 1) / 2 * 100 == 1 if lat > 0 (north), 0 if lat < 0 (south)
    # Then EPSG code with usual formula np.floor((180 + lon) / 6) + 1)
    epsg = int(32700 - (np.sign(lat) + 1) / 2 * 100 + np.floor((180 + lon) / 6) + 1)
    return f"EPSG:{epsg}"


def from_polygon_to_bounds(
    polygon: Union[Polygon, MultiPolygon]
) -> (float, float, float, float):
    """
    Convert a :code:`shapely.polygon` to its bounds, sorted as :code:`left, bottom, right, top`.

    .. code-block:: python

        >>> poly = Polygon(((0., 0.), (0., 1.), (1., 1.), (1., 0.), (0., 0.)))
        >>> from_polygon_to_bounds(poly)
        (0.0, 0.0, 1.0, 1.0)

    Args:
        polygon (MultiPolygon): polygon to convert

    Returns:
        (float, float, float, float): left, bottom, right, top
    """
    left = polygon.bounds[0]  # xmin
    bottom = polygon.bounds[1]  # ymin
    right = polygon.bounds[2]  # xmax
    top = polygon.bounds[3]  # ymax

    assert left < right
    assert bottom < top

    return left, bottom, right, top


def from_bounds_to_polygon(
    left: float, bottom: float, right: float, top: float
) -> Polygon:
    """
    Convert the bounds to a :code:`shapely.polygon`.

    .. code-block:: python

        >>> poly = from_bounds_to_polygon(0.0, 0.0, 1.0, 1.0)
        >>> print(poly)
        'POLYGON ((1 0, 1 1, 0 1, 0 0, 1 0))'

    Args:
        left (float): Left coordinates
        bottom (float): Bottom coordinates
        right (float): Right coordinates
        top (float): Top coordinates

    Returns:
        Polygon: Polygon corresponding to the bounds

    """
    return box(min(left, right), min(top, bottom), max(left, right), max(top, bottom))


def get_geodf(
    geometry: Union[Polygon, list, gpd.GeoSeries], crs: str
) -> gpd.GeoDataFrame:
    """
    Get a GeoDataFrame from a geometry and a crs

    .. code-block:: python

        >>> poly = Polygon(((0., 0.), (0., 1.), (1., 1.), (1., 0.), (0., 0.)))
        >>> geodf = get_geodf(poly, crs=WGS84)
        >>> print(geodf)
                                                    geometry
        0  POLYGON ((0.00000 0.00000, 0.00000 1.00000, 1....

    Args:
        geometry (Union[Polygon, list]): List of Polygons, or Polygon or bounds
        crs (str): CRS of the polygon

    Returns:
        gpd.GeoDataFrame: Geometry as a geodataframe
    """
    if isinstance(geometry, list):
        if isinstance(geometry[0], Polygon):
            pass
        else:
            try:
                geometry = [from_bounds_to_polygon(*geometry)]
            except TypeError as ex:
                raise TypeError(
                    "Give the extent as 'left', 'bottom', 'right', and 'top'"
                ) from ex
    elif isinstance(geometry, Polygon):
        geometry = [geometry]
    elif isinstance(geometry, gpd.GeoSeries):
        geometry = geometry.geometry
    else:
        raise TypeError("geometry should be a list or a Polygon.")

    return gpd.GeoDataFrame(geometry=geometry, crs=crs)


def set_kml_driver() -> None:
    """
    Set KML driver for Fiona data (use it at your own risks !)

    .. code-block:: python

        >>> path = "path/to/kml.kml"
        >>> gpd.read_file(path)
        fiona.errors.DriverError: unsupported driver: 'LIBKML'

        >>> set_kml_driver()
        >>> gpd.read_file(path)
                       Name  ...                                           geometry
        0  CC679_new_AOI2_3  ...  POLYGON Z ((45.03532 32.49765 0.00000, 46.1947...
        [1 rows x 12 columns]

    """
    import fiona

    drivers = fiona.drvsupport.supported_drivers

    if "LIBKML" not in drivers:
        drivers["LIBKML"] = "rw"
    if "KML" not in drivers:  # Just in case
        drivers["KML"] = "rw"


def get_aoi_wkt(
    aoi_path: Union[str, CloudPath, Path], as_str: bool = True
) -> Union[str, Polygon]:
    """
    Get AOI formatted as a WKT from files that can be read by Fiona (like shapefiles, ...)
    or directly from a WKT file. The use of KML has been forced (use it at your own risks !).

    See: https://fiona.readthedocs.io/en/latest/fiona.html#fiona.open

    It is assessed that:

    - only **one** polygon composes the AOI (as only the first one is read)
    - it should be specified in lat/lon (WGS84) if a WKT file is provided

    .. code-block:: python

        >>> path = "path/to/vec.geojson"  # OK with ESRI Shapefile, geojson, WKT, KML...
        >>> get_aoi_wkt(path)
        'POLYGON Z ((46.1947755465253067 32.4973553439109324 0.0000000000000000, 45.0353174370802520 32.4976496856158974
        0.0000000000000000, 45.0355748149750283 34.1139970085580018 0.0000000000000000, 46.1956059695554089
        34.1144793800670882 0.0000000000000000, 46.1947755465253067 32.4973553439109324 0.0000000000000000))'

    Args:
        aoi_path (Union[str, CloudPath, Path]): Absolute or relative path to an AOI.
            Its format should be WKT or any format read by Fiona, like shapefiles.
        as_str (bool): If True, return WKT as a str, otherwise as a shapely geometry

    Returns:
        Union[str, Polygon]: AOI formatted as a WKT stored in lat/lon
    """
    aoi_path = AnyPath(aoi_path)
    if not aoi_path.is_file():
        raise FileNotFoundError(f"AOI file {aoi_path} does not exist.")

    if aoi_path.suffix == ".wkt":
        try:
            with open(aoi_path, "r") as aoi_f:
                aoi = wkt.load(aoi_f)
        except Exception as ex:
            raise ValueError("AOI WKT cannot be read") from ex
    else:
        try:
            # Open file
            aoi_file = read(aoi_path, crs=WGS84)

            # Get envelope polygon
            geom = aoi_file["geometry"]
            if len(geom) > 1:
                LOGGER.warning(
                    "Your AOI contains several polygons. Only the first will be treated !"
                )
            polygon = geom[0].convex_hull

            # Convert to WKT
            aoi = wkt.loads(str(polygon))

        except Exception as ex:
            raise ValueError("AOI cannot be read by Fiona") from ex

    # Convert to string if needed
    if as_str:
        aoi = wkt.dumps(aoi)

    LOGGER.debug("Specified AOI in WKT: %s", aoi)
    return aoi


def get_wider_exterior(vector: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Get the wider exterior of a MultiPolygon as a Polygon

    Args:
        vector (gpd.GeoDataFrame): Polygon to simplify

    Returns:
        vector: gpd.GeoDataFrame: Wider exterior
    """

    # Get the footprint max (discard small holes stored in other polygons)
    wider = vector[vector.area == np.max(vector.area)]

    # Only select the exterior of this footprint(sometimes some holes persist)
    if not wider.empty:
        poly = Polygon(list(wider.exterior.iat[0].coords))
        wider = gpd.GeoDataFrame(geometry=[poly], crs=wider.crs)

        # Resets index as we only got one polygon left which should have index 0
        wider.reset_index(inplace=True)

    return wider


def _to_polygons(val: Any) -> Polygon:
    """
    Convert to polygon (to be used in pandas) -> convert the geometry column

    Args:
        val (Any): Pandas value that has a "coordinates" field

    Returns:
        Polygon: Pandas value as a Polygon
    """
    # Donut cases
    if len(val["coordinates"]) > 1:
        poly = Polygon(val["coordinates"][0], val["coordinates"][1:])
    else:
        poly = Polygon(val["coordinates"][0])
        pass

    return poly


def shapes_to_gdf(shapes: Generator, crs: str) -> gpd.GeoDataFrame:
    """
    Convert rasterio shapes to geodataframe

    Args:
        shapes (Generator): Shapes from rasterio
        crs: Wanted CRS of the vector. If None, using naive or origin CRS.
    Returns:
        gpd.GeoDataFrame: Shapes as a GeoDataFrame
    """
    # Convert results to pandas (because of invalid geometries) and save it
    pd_results = pd.DataFrame(shapes, columns=["geometry", "raster_val"])

    if not pd_results.empty:
        # Convert to proper polygons(correct geometries)
        pd_results.geometry = pd_results.geometry.apply(_to_polygons)

    # Convert to geodataframe with correct geometry
    gdf = gpd.GeoDataFrame(pd_results, geometry=pd_results.geometry, crs=crs)

    # Return valid geometries
    gdf = make_valid(gdf)

    return gdf


def write(gdf: gpd.GeoDataFrame, path: Union[str, CloudPath, Path], **kwargs) -> None:
    """
    Write vector to disk, managing the common drivers automatically.

    Args:
        gdf (gpd.GeoDataFrame): GeoDataFrame to write on disk
        path (Union[str, CloudPath, Path]): Where to write on disk.
    """
    path = AnyPath(path)

    driver = kwargs.pop("driver", None)
    if not driver:
        driver = EXT_TO_DRIVER.get(path.suffix)
        if driver == "KML":
            set_kml_driver()
        elif driver == "KMZ":
            raise NotImplementedError("Impossible to write a KMZ for now.")

    gdf.to_file(str(path), driver=driver, **kwargs)


def copy(
    src_path: Union[str, Path, CloudPath], dst_path: Union[str, Path, CloudPath]
) -> Union[Path, CloudPath]:
    """
     Copy vector (handles shapefiles additional files)

    Args:
        src_path (Union[str, Path, CloudPath]): Source Path
        dst_path (Union[str, Path, CloudPath]): Destination Path (file or folder)

    Returns:
        Union[Path, CloudPath]: Path to copied vector
    """
    src_path = AnyPath(src_path)
    dst_path = AnyPath(dst_path)

    if not dst_path.is_file():
        dst_path = files.copy(src_path, dst_path)

        # Add files that come with shape
        shp_co_files = [
            file
            for file in src_path.parent.glob(f"{files.get_filename(src_path)}.*")
            if file.suffix in SHP_CO_FILES
        ]
        for co_file in shp_co_files:
            files.copy(co_file, dst_path.with_suffix(co_file.suffix))

    return dst_path


def read(
    path: Union[str, CloudPath, Path], crs: Any = None, archive_regex: str = None
) -> gpd.GeoDataFrame:
    """
    Read any vector:

    - if KML: sets correctly the drivers and open layered KML (you may need :code:`ogr2ogr` to make it work !)
    - if archive (only zip or tar), use a regex to look for the vector inside the archive.
        You can use this `site <https://regexr.com/>`_ to build your regex.
    - if GML: manages the empty errors

    .. code-block:: python

        >>> # Usual
        >>> path = 'D:/path/to/vector.geojson'
        >>> vectors.read(path, crs=WGS84)
                               Name  ...                                           geometry
        0  Sentinel-1 Image Overlay  ...  POLYGON ((0.85336 42.24660, -2.32032 42.65493,...

        >>> # Archive
        >>> arch_path = 'D:/path/to/zip.zip'
        >>> vectors.read(arch_path, archive_regex=r".*map-overlay.kml")
                               Name  ...                                           geometry
        0  Sentinel-1 Image Overlay  ...  POLYGON ((0.85336 42.24660, -2.32032 42.65493,...

    Args:
        path (Union[str, CloudPath, Path]): Path to vector to read. In case of archive, path to the archive.
        crs: Wanted CRS of the vector. If None, using naive or origin CRS.
        archive_regex (str): [Archive only] Regex for the wanted vector inside the archive

    Returns:
        gpd.GeoDataFrame: Read vector as a GeoDataFrame
    """
    tmp_dir = None
    arch_vect_path = None

    try:
        path = AnyPath(path)

        # Load vector in cache if needed (geopandas do not use correctly S3 paths for now)
        if isinstance(path, CloudPath):
            tmp_dir = tempfile.TemporaryDirectory()
            if path.suffix == ".shp":
                # Download everything to disk
                for shp_file in path.parent.glob(path.with_suffix(".*").name):
                    cached_path = shp_file.download_to(tmp_dir.name)
                    if cached_path.suffix == ".shp":
                        path = cached_path
            else:
                path = AnyPath(path.fspath)

        # Manage archive case
        if path.suffix in [".tar", ".zip"]:
            prefix = path.suffix[-3:]
            file_list = files.get_archived_file_list(path)

            try:
                regex = re.compile(archive_regex)
                arch_vect_path = list(filter(regex.match, file_list))[0]

                if isinstance(path, CloudPath):
                    vect_path = f"{prefix}+{path}!{arch_vect_path}"
                else:
                    vect_path = f"{prefix}://{path}!{arch_vect_path}"
            except IndexError:
                raise FileNotFoundError(
                    f"Impossible to find vector {archive_regex} in {files.get_filename(path)}"
                )
        elif path.suffixes == [".tar", ".gz"]:
            raise TypeError(
                ".tar.gz files are too slow to read from inside the archive. Please extract them instead."
            )
        else:
            vect_path = str(path)
    except AnyPathTypeError:
        vect_path = str(path)

    if not os.path.isfile(path):
        raise FileNotFoundError(f"Non existing file: {path}")

    # Open vector
    try:
        # Discard some weird error concerning a NULL pointer that outputs a ValueError (as we already except it)
        fiona_logger = logging.getLogger("fiona")
        fiona_logger.setLevel(logging.CRITICAL)

        # Manage KML driver
        if vect_path.endswith(".kml") or vect_path.endswith(".kmz"):
            vect = _read_kml(vect_path, path, arch_vect_path, tmp_dir)
        else:
            vect = gpd.read_file(vect_path)

        # Manage naive geometries
        if vect.crs and crs:
            vect = vect.to_crs(crs)

        # Set fiona logger back to what it was
        fiona_logger.setLevel(logging.INFO)
    except (ValueError, UnsupportedGeometryTypeError) as ex:
        # Do not print warning for null layer
        if "Null layer" not in str(ex):
            LOGGER.warning(ex)
        vect = gpd.GeoDataFrame(geometry=[], crs=crs)
    except CPLE_AppDefinedError as ex:
        # Needs ogr2ogr here
        if shutil.which("ogr2ogr"):
            # Open as geojson
            if not tmp_dir:
                tmp_dir = tempfile.TemporaryDirectory()
            vect_path_gj = ogr2geojson(path, tmp_dir.name, arch_vect_path)
            vect = gpd.read_file(vect_path_gj)
            vect.crs = None
        else:
            # Do not print warning for null layer
            if "Null layer" not in str(ex):
                LOGGER.warning(ex)
            vect = gpd.GeoDataFrame(geometry=[], crs=crs)

    # Clean
    if tmp_dir:
        tmp_dir.cleanup()

    return vect


def _read_kml(
    vect_path: str,
    path: Union[str, CloudPath, Path],
    arch_vect_path: str = None,
    tmp_dir=None,
) -> gpd.GeoDataFrame:
    """
    Reader of KML data

    Args:
        vect_path (str): Resolved vector path (rteadable by geopandas, not on cloud etc.)
        path (Union[str, CloudPath, Path]): Path to vector to read. In case of archive, path to the archive.
        arch_vect_path: If archived vector, archive path
        tmp_dir:

    Returns:
        gpd.GeoDataFrame: KML as a geopandas GeoDataFrame

    """
    set_kml_driver()
    vect = gpd.GeoDataFrame()

    # Document tags in KML file are separate layers for GeoPandas.
    # When you try to get the KML content, you actually get the first layer.
    # So you need for loop for iterating over layers.
    # https://gis.stackexchange.com/questions/328525/geopandas-read-file-only-reading-first-part-of-kml/328554
    import fiona

    for layer in fiona.listlayers(vect_path):
        try:
            vect_layer = gpd.read_file(vect_path, driver="KML", layer=layer)
            if not vect_layer.empty:
                # KML files are always in WGS84 (and does not contain this information)
                vect_layer.crs = WGS84
                vect = pd.concat([vect, vect_layer])
        except ValueError:
            pass  # Except Null Layer

    # Workaround for archived KML -> they may be empty
    # Convert KML to GeoJSON
    # Needs ogr2ogr here
    if vect.empty:
        if shutil.which("ogr2ogr"):
            # Open the geojson
            if not tmp_dir:
                tmp_dir = tempfile.TemporaryDirectory()
            vect_path_gj = ogr2geojson(path, tmp_dir.name, arch_vect_path)
            vect = gpd.read_file(vect_path_gj)
        else:
            # Try reading it in a basic manner
            LOGGER.warning(
                "Missing `ogr2ogr` in your PATH, your KML may be incomplete. "
                "(KML files can contain unsupported data structures, nested folders etc.)"
            )
            try:
                vect = gpd.read_file(vect_path)
            except Exception:
                # Force set CRS to empty vector
                vect.crs = WGS84

    return vect


def ogr2geojson(
    path: Union[str, CloudPath, Path],
    out_dir: Union[str, CloudPath, Path],
    arch_vect_path: str = None,
) -> str:
    """
    Wrapper of ogr2ogr function, converting the input vector to GeoJSON.

    Args:
        path (Union[str, CloudPath, Path]): Path to vector to read. In case of archive, path to the archive.
        out_dir (Union[str, CloudPath, Path]): Output directory
        arch_vect_path: If archived vector, archive path

    Returns:
        str: Converted file
    """
    assert shutil.which("ogr2ogr")  # Needs ogr2ogr here

    out_dir = str(out_dir)

    if path.suffix == ".zip":
        with zipfile.ZipFile(path, "r") as zip_ds:
            vect_path = zip_ds.extract(arch_vect_path, out_dir)
    elif path.suffix == ".tar":
        with tarfile.open(path, "r") as tar_ds:
            tar_ds.extract(arch_vect_path, out_dir)
            vect_path = os.path.join(out_dir, arch_vect_path)
    else:
        vect_path = str(path)

    vect_path_gj = os.path.join(
        out_dir,
        os.path.basename(vect_path).replace(files.get_ext(vect_path), "geojson"),
    )
    cmd_line = [
        "ogr2ogr",
        "-fieldTypeToString DateTime",  # Disable warning
        "-f GeoJSON",
        strings.to_cmd_string(vect_path_gj),  # dst
        strings.to_cmd_string(vect_path),  # src
    ]
    try:
        misc.run_cli(cmd_line)
    except RuntimeError as ex:
        raise RuntimeError(f"Something went wrong with ogr2ogr: {ex}") from ex

    return vect_path_gj


def make_valid(gdf: gpd.GeoDataFrame, verbose=False) -> gpd.GeoDataFrame:
    try:
        geos_logger = logging.getLogger("shapely.geos")
        previous_level = geos_logger.level
        if verbose:
            logging.debug("Invalid geometries:\n" f"\t{gdf[~gdf.is_valid]}")
        else:
            geos_logger.setLevel(logging.CRITICAL)

        # Discard self-intersection and null geometries
        from shapely.validation import make_valid

        gdf.geometry = gdf.geometry.apply(make_valid)

        if not verbose:
            geos_logger.setLevel(previous_level)
    except ImportError:
        import shapely

        LOGGER.warning(
            f"make_valid not available in shapely (version {shapely.__version__} < 1.8). "
            f"The obtained vector may be broken !"
        )

    return gdf


def simplify_footprint(
    footprint: gpd.GeoDataFrame, resolution: float, max_nof_vertices: int = 50
) -> gpd.GeoDataFrame:
    """
    Simplify footprint.

    Set a number of maximum vertices and this function will try to simplify the footprint to have less than this number of vertices.
    The tolerance will grow to try to respect this number of vertices.

    This function will loop over a number of pixels of tolerence [1, 2, 4, 8, 16, 32, 64] (tolerance of gpd.simplify == resolution * tol_pix)
    If in the end, the number of vertices is still too high, a warning will be emitted.

    Args:
        footprint (gpd.GeoDataFrame): Footprint to be simplified
        resolution (float): Corresponding resolution
        max_nof_vertices (int): Maximum number of vertices of the wanted footprint

    Returns:
        gpd.GeoDataFrame: Simplified footprint
    """
    # Number of pixels of tolerance
    tolerance = [1, 2, 4, 8, 16, 32, 64]

    # Process only if given footprint is too complex (too many vertices)
    def simplify_geom(value):
        nof_vertices = len(value.exterior.coords)
        if nof_vertices > max_nof_vertices:
            for tol in tolerance:
                # Simplify footprint
                value = value.simplify(
                    tolerance=tol * resolution, preserve_topology=True
                )

                # Check if OK
                nof_vertices = len(value.exterior.coords)
                if nof_vertices <= max_nof_vertices:
                    break
        return value

    footprint = footprint.explode(index_parts=True)
    footprint.geometry = footprint.geometry.apply(simplify_geom)

    return footprint
