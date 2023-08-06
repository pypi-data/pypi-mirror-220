import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import wget
import os

# TODO:
# 1: CHECK IF 18S OR 19S SHOULD APPLY


def get_census_dataset() -> gpd.GeoDataFrame:
    os.makedirs("data", exist_ok=True)
    file = wget.download("https://github.com/martin-conur/mcu_geo_utils/blob/main/mcu_geo_utils/data/info_manzanas_censo2017.feather?raw=True", out="data/info_manzanas_censo2017.feather")
    return gpd.read_feather(file)


def get_ismt_dataset() -> gpd.GeoDataFrame:
    os.makedirs("data", exist_ok=True)
    file = wget.download("https://github.com/martin-conur/mcu_geo_utils/blob/main/mcu_geo_utils/data/ISMT_2022_actualizado_simplificado.feather?raw=True", out="data/ISMT_2022_actualizado_simplificado.feather")
    return gpd.read_feather(file)


def get_coverture_percentage(df, other):
    return (
        df
        .assign(
            coverture=df.area / other.area
        )
    )


def get_census_data_from_point(lat: float,
                               lon: float,
                               census_df: gpd.GeoDataFrame,
                               radio: int = 1000) -> pd.DataFrame:
    # defining the geoseries point from 'lat' and 'lon'
    point = (
        gpd.GeoSeries(Point(lon, lat), crs=4326)
        .to_crs(9155)  # TODO 1
        .buffer(1000)
        .to_crs(4326)
    )

    # Creating the filtered dataframe
    def weighted_sum_censo(df):
        coverture = df.pop("coverture")
        return df.mul(coverture, axis=0).sum()

    censo_intersection = census_df.intersects(point.geometry.iloc[0])
    censo_columns = ["TOTAL_VIVI", "NHOMBRES",	"NMUJERES", "coverture"]
    inter_censo = (
        census_df
        .assign(
            geometry=census_df.intersection(point.iloc[0])
        )
        .pipe(get_coverture_percentage, census_df)
        .loc[censo_intersection]
        [censo_columns]
        .pipe(weighted_sum_censo)
        .to_frame()
        .T
    )
    return inter_censo


def get_ismt_data_from_point(lat: float,
                             lon: float,
                             ismt_df: gpd.GeoDataFrame,
                             radio: int = 1000) -> pd.DataFrame:

    # defining the geoseries point from 'lat' and 'lon'
    point = (
        gpd.GeoSeries(Point(lon, lat), crs=4326)
        .to_crs(9155)  # TODO 1
        .buffer(1000)
        .to_crs(4326)
    )
    # Creating the filtered dataframe
    ismt_intersection = ismt_df.intersects(point.geometry.iloc[0])
    columns = [
        'Alto',
        'Medio',
        'Bajo',
        'AB',
        'C1',
        'C2',
        'C3',
        'D',
        'E',
        'ind_hac',
        'alleg',
        'escolar',
        'ind_mat',
        'coverture'
        ]

    inter = (
        ismt_df
        .assign(
            geometry=ismt_df.intersection(point.geometry.iloc[0])
        )
        .pipe(get_coverture_percentage, ismt_df)
        .loc[ismt_intersection]
        [columns]
    )
    coverture = inter.pop("coverture")

    weighted_sum = inter.mul(coverture, axis=0).sum()
    inter_mean = (
        weighted_sum
        .div(coverture.sum())
        [
            ["escolar", "ind_hac", "ind_mat"]
        ]
        .to_frame()
        .T
    )

    inter_sum = (
        weighted_sum
        [
            [
                'Alto',
                'Medio',
                'Bajo',
                'AB',
                'C1',
                'C2',
                'C3',
                'D',
                'E',
                'alleg'
            ]
        ]
        .to_frame()
        .T
    )
    return pd.concat([inter_mean, inter_sum], axis=1)
