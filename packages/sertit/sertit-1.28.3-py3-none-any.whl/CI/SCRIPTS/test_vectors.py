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
""" Script testing vector functions """
import os
import tempfile

import geopandas as gpd
import pytest
from fiona.errors import DriverError
from shapely import wkt

from CI.SCRIPTS.script_utils import s3_env, vectors_path
from sertit import ci, files, vectors
from sertit.vectors import WGS84

ci.reduce_verbosity()


@s3_env
def test_vectors():
    """Test geo functions"""
    shp_path = vectors_path().joinpath("aoi.shp")
    kml_path = vectors_path().joinpath("aoi.kml")
    wkt_path = vectors_path().joinpath("aoi.wkt")
    utm_path = vectors_path().joinpath("aoi.geojson")
    ci.assert_geom_equal(shp_path, utm_path)  # Test shp

    # Test 3D vectors
    # with pytest.raises(AssertionError):
    #     ci.assert_geom_equal(shp_path, utm_path, ignore_z=False)

    # KML
    vectors.set_kml_driver()  # An error will occur afterwards if this fails (we are attempting to open a KML file)

    # KML to WKT
    aoi_str_test = vectors.get_aoi_wkt(kml_path, as_str=True)
    aoi_str = (
        "POLYGON Z ((46.1947755465253067 32.4973553439109324 0.0000000000000000, "
        "45.0353174370802520 32.4976496856158974 0.0000000000000000, "
        "45.0355748149750283 34.1139970085580018 0.0000000000000000, "
        "46.1956059695554089 34.1144793800670882 0.0000000000000000, "
        "46.1947755465253067 32.4973553439109324 0.0000000000000000))"
    )
    assert aoi_str == aoi_str_test

    aoi = vectors.get_aoi_wkt(kml_path, as_str=False)

    # WKT to WKT
    aoi2 = vectors.get_aoi_wkt(wkt_path, as_str=False)

    # UTM to WKT
    aoi3 = vectors.get_aoi_wkt(utm_path, as_str=False)

    assert aoi.equals(aoi2)  # No reprojection, should be equal
    assert aoi.equals_exact(
        aoi3, tolerance=0.5 * 10**6
    )  # Reprojection, so almost equal
    assert wkt.dumps(aoi) == aoi_str

    # UTM and bounds
    aoi = vectors.read(kml_path)
    assert "EPSG:32638" == vectors.corresponding_utm_projection(
        aoi.centroid.x, aoi.centroid.y
    )
    env = aoi.envelope[0]
    from_env = vectors.from_bounds_to_polygon(*vectors.from_polygon_to_bounds(env))
    assert env.bounds == from_env.bounds

    # GeoDataFrame
    geodf = vectors.get_geodf(env, aoi.crs)  # GeoDataFrame from Polygon
    ci.assert_geom_equal(geodf.geometry, aoi.envelope)
    ci.assert_geom_equal(
        vectors.get_geodf(geodf.geometry, aoi.crs), geodf
    )  # GeoDataFrame from Geoseries
    ci.assert_geom_equal(
        vectors.get_geodf([env], aoi.crs), geodf
    )  # GeoDataFrame from list of poly

    with pytest.raises(TypeError):
        vectors.get_geodf([1, 2, 3, 4, 5], aoi.crs)
    with pytest.raises(TypeError):
        vectors.get_geodf([1, 2], aoi.crs)

    # Test make_valid
    broken_geom_path = vectors_path().joinpath("broken_geom.shp")
    broken_geom = vectors.read(broken_geom_path)
    assert len(broken_geom[~broken_geom.is_valid]) == 1
    valid = vectors.make_valid(broken_geom, verbose=True)
    assert len(valid[~valid.is_valid]) == 0
    assert len(valid) == len(broken_geom)


@s3_env
def test_kmz():
    """Test KMZ files"""
    kmz_path = vectors_path().joinpath("AOI.kmz")
    gj_path = vectors_path().joinpath("AOI.geojson")

    # Read vectors
    kmz = vectors.read(kmz_path)
    gj = vectors.read(gj_path)

    # Check if equivalent
    assert all(gj.geometry.geom_almost_equals(kmz.to_crs(gj.crs).geometry))


@s3_env
def test_gml():
    """Test GML functions"""
    empty_gml = vectors_path().joinpath("empty.GML")
    not_empty_gml = vectors_path().joinpath("not_empty.GML")
    naive_gml = vectors_path().joinpath("naive.GML")
    not_empty_true_path = vectors_path().joinpath("not_empty_true.geojson")

    # Empty
    empty_gdf = vectors.read(empty_gml, crs=WGS84)
    assert empty_gdf.empty
    assert empty_gdf.crs == WGS84

    # Not empty
    not_empty_true = vectors.read(not_empty_true_path)
    not_empty = vectors.read(not_empty_gml, crs=not_empty_true.crs)
    ci.assert_geom_equal(not_empty, not_empty_true)

    # Naive
    naive = vectors.read(naive_gml)
    assert naive.crs is None


@s3_env
def test_simplify_footprint():
    """Test simplify footprint"""
    complicated_footprint_path = vectors_path().joinpath(
        "complicated_footprint_spot6.geojson"
    )
    max_nof_vertices = 40
    complicated_footprint = vectors.read(complicated_footprint_path)
    ok_footprint = vectors.simplify_footprint(
        complicated_footprint, resolution=1.5, max_nof_vertices=max_nof_vertices
    )
    assert len(ok_footprint.geometry.exterior.iat[0].coords) < max_nof_vertices

    # Just to test
    nof_vertices_complicated = len(
        complicated_footprint.explode(index_parts=True).geometry.exterior.iat[0].coords
    )
    assert nof_vertices_complicated > max_nof_vertices


@s3_env
def test_write():
    vect_paths = [
        vectors_path().joinpath("aoi.shp"),
        vectors_path().joinpath("aoi.kml"),
        vectors_path().joinpath("aoi.geojson"),
    ]

    with tempfile.TemporaryDirectory() as tmp_dir:
        for vect_path in vect_paths:
            vect = vectors.read(vect_path)
            vect_out_path = os.path.join(tmp_dir, os.path.basename(vect_path))
            vectors.write(vect, vect_out_path)
            vect_out = vectors.read(vect_out_path)

            ci.assert_geom_equal(vect_out, vect)


@s3_env
def test_copy():
    shpfile = vectors_path().joinpath("aoi.shp")

    with tempfile.TemporaryDirectory() as tmp_dir:
        # Assert normal copy will fail
        with pytest.raises(DriverError):
            gpd.read_file(files.copy(shpfile, tmp_dir))

        # Assert vector copy will open in geopandas
        gpd.read_file(vectors.copy(shpfile, tmp_dir))
