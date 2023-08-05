# (c) 2022 DTU Wind Energy
"""
Module to handle elevation maps.
"""
from .raster_map import read_raster_map
from .vector_map import read_vector_map

try:
    from fiona.errors import DriverError

    HAS_FIONA = True
except (ModuleNotFoundError, ImportError):
    HAS_FIONA = False

# TODO: Make this and read_roughness_map into a generic function
def read_elevation_map(filename, crs=None, **kwargs):
    """Reads file into an elevation map.

    Parameters
    ----------
    filename : str or pathlib.Path
        Path to file
    crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS` (Default: read from file)
    **kwargs : dict
        Additonal keyword arguments passed to reader.
    Returns
    -------
    xarray.DataArray
        elevation_map object
    """
    kwargs = {**kwargs, **{"map_type": "elevation"}}
    if HAS_FIONA:
        try:
            return read_vector_map(filename, crs=crs, **kwargs)
        except DriverError:
            return read_raster_map(filename, crs=crs, **kwargs)
    else:
        return read_raster_map(filename, crs=crs, **kwargs)
