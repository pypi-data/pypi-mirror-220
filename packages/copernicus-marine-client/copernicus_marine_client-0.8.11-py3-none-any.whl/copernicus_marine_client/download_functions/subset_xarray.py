import logging
from datetime import datetime
from decimal import Decimal
from typing import List, Literal, Optional, Tuple, Union

import numpy as np
import xarray as xr

COORDINATES_LABEL = {
    "latitude": ["latitude", "nav_lat", "x"],
    "longitude": ["longitude", "nav_lon", "y"],
    "time": ["time_counter", "time"],
    "depth": ["depth", "deptht", "elevation"],
}


def dataset_custom_sel(
    dataset: xr.Dataset,
    coord_type: Literal["latitude", "longitude", "depth", "time"],
    coord_selection: Union[float, slice, datetime, None],
    method: Union[str, None] = None,
) -> xr.Dataset:
    for coord_label in COORDINATES_LABEL[coord_type]:
        if coord_label in dataset.coords:
            dataset = dataset.sel(
                {coord_label: coord_selection}, method=method
            )
    return dataset


def _latitude_subset(
    minimal_latitude: Optional[float],
    maximal_latitude: Optional[float],
    dataset: xr.Dataset,
) -> xr.Dataset:
    if minimal_latitude is not None or maximal_latitude is not None:
        latitude_selection = (
            minimal_latitude
            if minimal_latitude == maximal_latitude
            else slice(minimal_latitude, maximal_latitude)
        )
        latitude_method = (
            "nearest" if minimal_latitude == maximal_latitude else None
        )
        dataset = dataset_custom_sel(
            dataset, "latitude", latitude_selection, latitude_method
        )
    return dataset


def _longitude_subset(
    minimal_longitude: Optional[float],
    maximal_longitude: Optional[float],
    dataset: xr.Dataset,
) -> xr.Dataset:
    def _update_dataset_attributes(dataset: xr.Dataset):
        for coord_label in COORDINATES_LABEL["longitude"]:
            if coord_label in dataset.coords:
                attrs = dataset[coord_label].attrs
                if attrs["valid_min"]:
                    attrs["valid_min"] += 180
                if attrs["valid_max"]:
                    attrs["valid_max"] += 180
                dataset = dataset.assign_coords(
                    {coord_label: (dataset[coord_label] + 360.0) % 360}
                ).sortby(coord_label)
                dataset[coord_label].attrs = attrs
        return dataset

    if minimal_longitude is not None or maximal_longitude is not None:
        if minimal_longitude is not None and maximal_longitude is not None:
            if minimal_longitude > maximal_longitude:
                logging.error(
                    "--minimal-longitude option must be smaller "
                    "or equal to --maximal-longitude"
                )
                raise ValueError
            elif minimal_longitude == maximal_longitude:
                longitude_selection: Union[
                    float, slice, None
                ] = longitude_modulus(minimal_longitude)
                longitude_method = "nearest"
            else:
                if maximal_longitude - minimal_longitude >= 360:
                    longitude_selection = None
                else:
                    minimal_longitude_modulus = longitude_modulus(
                        minimal_longitude
                    )
                    maximal_longitude_modulus = longitude_modulus(
                        maximal_longitude
                    )
                    if maximal_longitude_modulus < minimal_longitude_modulus:
                        maximal_longitude_modulus += 360
                        dataset = _update_dataset_attributes(dataset)
                    longitude_selection = slice(
                        minimal_longitude_modulus,
                        maximal_longitude_modulus,
                    )
                    longitude_method = None

        else:
            longitude_selection = slice(minimal_longitude, maximal_longitude)
            longitude_method = None
        if longitude_selection is not None:
            dataset = dataset_custom_sel(
                dataset, "longitude", longitude_selection, longitude_method
            )
    return dataset


def _temporal_subset(
    start_datetime: Optional[datetime],
    end_datetime: Optional[datetime],
    dataset: xr.Dataset,
) -> xr.Dataset:
    if start_datetime is not None or end_datetime is not None:
        temporal_selection = (
            start_datetime
            if start_datetime == end_datetime
            else slice(start_datetime, end_datetime)
        )
        temporal_method = "nearest" if start_datetime == end_datetime else None
        dataset = dataset_custom_sel(
            dataset, "time", temporal_selection, temporal_method
        )
    return dataset


def _depth_subset(
    minimal_depth: Optional[float],
    maximal_depth: Optional[float],
    dataset: xr.Dataset,
) -> xr.Dataset:
    if minimal_depth is not None or maximal_depth is not None:
        if "elevation" in dataset.dims:
            minimal_depth = (
                minimal_depth * -1.0 if minimal_depth is not None else None
            )
            maximal_depth = (
                maximal_depth * -1.0 if maximal_depth is not None else None
            )
            minimal_depth, maximal_depth = maximal_depth, minimal_depth

        depth_selection = (
            minimal_depth
            if minimal_depth == maximal_depth
            else slice(minimal_depth, maximal_depth)
        )
        depth_method = "nearest" if minimal_depth == maximal_depth else None
        dataset = dataset_custom_sel(
            dataset, "depth", depth_selection, depth_method
        )
    return dataset


def subset(
    ds,
    variables: Optional[List[str]] = None,
    geographical_subset: Optional[
        Tuple[
            Optional[float], Optional[float], Optional[float], Optional[float]
        ]
    ] = None,
    temporal_subset: Optional[
        Tuple[Optional[datetime], Optional[datetime]]
    ] = None,
    depth_range: Optional[Tuple[Optional[float], Optional[float]]] = None,
) -> xr.Dataset:

    if variables:
        ds = ds[np.array(variables)]

    if geographical_subset is not None:
        (
            minimal_latitude,
            maximal_latitude,
            minimal_longitude,
            maximal_longitude,
        ) = geographical_subset
        ds = _latitude_subset(minimal_latitude, maximal_latitude, ds)
        ds = _longitude_subset(minimal_longitude, maximal_longitude, ds)

    if temporal_subset is not None:
        start_datetime, end_datetime = temporal_subset
        ds = _temporal_subset(start_datetime, end_datetime, ds)

    if depth_range is not None:
        minimal_depth, maximal_depth = depth_range
        ds = _depth_subset(minimal_depth, maximal_depth, ds)

    return ds


def longitude_modulus(longitude: float) -> float:
    """
    Returns the equivalent longitude between -180 and 180
    """
    # We are using Decimal to avoid issue with rounding
    modulus = float(Decimal(str(longitude + 180)) % 360)
    # Modulus with python return a negative value if the denominator is negative
    # To counteract that, we add 360 if the result is < 0
    modulus = modulus if modulus >= 0 else modulus + 360
    return modulus - 180
