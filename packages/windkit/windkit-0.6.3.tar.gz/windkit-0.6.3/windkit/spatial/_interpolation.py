"""Internal interpolation routines

These routines are used to resample and reproject the source data to target grid
"""

import numpy as np
import scipy.interpolate
import xarray as xr

from ..metadata import update_history
from .spatial import (
    are_spatially_equal,
    get_crs,
    is_raster,
    spatial_stack,
    to_point,
    to_raster,
)


def _single_pt(source, target, exclude=True):
    """Broadcast source single point dataset to all points in target dataset

    Parameters
    ----------
    source : xarray.Dataset
        PyWAsP 3D point dataset
    target : xarray.Dataset
        PyWAsP xr.DataSet

    Returns
    -------
    xarray.Dataset
        Broadcasted source xr.DataSet

    Raises
    ------
    ValueError
        If source xr.DataSet contains more than a single point
    """
    if exclude:
        raise ValueError(
            "Single point data provided, but single-point interpolation excluded."
        )
    if source.dims["point"] != 1:
        raise ValueError("Can only project to a single point if point dimension == 1.")
    # Convert target to points
    out_pts = to_point(target)

    # Broadcast the data to all of the points
    out = xr.broadcast(source.squeeze("point"), out_pts, exclude=source.CORE_DIMS)[0]
    out["west_east"] = out_pts.west_east
    out["south_north"] = out_pts.south_north
    out["height"] = out_pts.height

    # Return to raster if target was raster
    if is_raster(target):
        out = to_raster(out)

    return out


def _nearest(source, target):
    """Nearest neighbor interpolation of source point dataset to target grid

    Parameters
    ----------
    source: xarray.Dataset
        PyWAsP 3D point dataset
    target: xarray.Dataset
        PyWAsP 3D point dataset
    """
    # Create a 3D tuple of the input points
    points = (source.west_east, source.south_north, source.height)

    # Combine all of the output points into a tuple
    if is_raster(target):
        out_mesh_x, out_mesh_y, out_mesh_z = np.meshgrid(
            target.west_east, target.south_north, target.height
        )
        xi = (out_mesh_x, out_mesh_y, out_mesh_z)
    else:
        xi = (target.west_east, target.south_north, target.height)

    # Get indices of the nearest point
    idx = scipy.interpolate.griddata(
        points, np.arange(source["point"].size), xi, method="nearest"
    )

    # Subset and reshape array
    out = source.isel(point=idx.flatten())

    # Reshape to raster if necessary
    if is_raster(target):
        # Set new coordinate values to match the target coorinates
        out.coords["west_east"].values = xi[0].flatten()
        out.coords["south_north"].values = xi[1].flatten()
        out.coords["height"].values = xi[2].flatten()
        out = to_raster(out)
    else:
        # Set new coordinate values to match the target coorinates
        out.coords["west_east"].values = xi[0].values
        out.coords["south_north"].values = xi[1].values
        out.coords["height"].values = xi[2].values

    return out


def interpolate_to_grid(source, target, method, exclude=False):
    """Resamples source to target grid

    Parameters
    ----------
    source : xarray.Dataset
        PyWAsP 3D point dataset with geographic coordinates and crs
    target : xarray.Dataset
        PyWAsP dataset with geographic coordinates and crs
    method : string
        Method of interpolation, currently only nearest is supported
    exclude: bool, optional
        To exclude _single_pt interpolation method, by default False

    Returns
    -------
    xr.Dataset
        Source dataset interpolated to the target grid

    Raises
    ------
    ValueError
        If source and target grids are different
    """
    target_crs = get_crs(target.crs)
    source = spatial_stack(source, target_crs, False)

    # Need to always have a height column, so add it if there isn't a height coord
    if "height" not in source.coords:
        source.coords["height"] = xr.DataArray(
            np.repeat([10], source.dims["point"]), dims=["point"]
        )
        for var in source.data_vars:
            source[var].attrs["_pwio_data_is_2d"] = False

    # Only single point and nearest are setup right now
    if source.dims["point"] == 1:
        res = _single_pt(source, target, exclude)
        return update_history(res)

    if method == "nearest":
        res = _nearest(source, target)
        return res

    if not are_spatially_equal(to_point(source), to_point(target)):
        raise ValueError(
            "source and target grids are different, "
            + "so you need to specify an interpolation method."
        )
    return update_history(source)
