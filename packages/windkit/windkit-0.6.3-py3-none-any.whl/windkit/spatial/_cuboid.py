from ._raster import to_raster


def to_cuboid(obj, ignore_raster_check=False):
    """Converts a point based object to a cuboid based object

    Parameters
    ----------
    obj : xarray.Dataset, xarray.DataArray
        WindKit xarray dataset or dataarray containing spatial
        dimensions and CRS variable
    ignore_raster_check : bool
        Check if the object satisfy the requirements to become a raster
        Default set to False (i.e., not to check)

    Returns
    -------
    xarray.Dataset, xarray.DataArray
        Raster version of WindKit xarray dataset or dataarray

    Raises
    ------
    ValueError
        If dataset cannot be converted to cuboid
    """
    return to_raster(obj, ignore_raster_check=ignore_raster_check)
