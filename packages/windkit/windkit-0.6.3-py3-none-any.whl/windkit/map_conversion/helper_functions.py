"""Functions used in several modules."""

import numpy as np

from windkit.geospatial_imports import HAS_GEOPANDAS, requires_geopandas

if HAS_GEOPANDAS:
    import geopandas as gpd


def _get_AL(nodes):
    """
    Create the adjency list of the nodes.

    Nodes are connected if points they have the same position.
    """
    n = len(nodes)
    sorted_index = np.argsort(nodes)
    nodes = np.array(nodes)[sorted_index]

    # initialise adjency lists
    AL = np.zeros(n, set)
    for i in range(n):
        AL[i] = []

    # link lines together
    i = 0
    while i < n - 1:
        end = False
        k = 1
        while (not end) and (i + k < n):
            if nodes[i] == nodes[i + k]:
                a = sorted_index[i]
                b = sorted_index[i + k]
                AL[a].append(b)
                AL[b].append(a)
                k += 1
            else:
                end = True
        i += 1
    return AL


def _sort_counterclockwise_points(middle, ref, points):
    """Return index to sort the points in counterclockwise direction."""
    angles = [_get_angle(middle, ref, points[i]) for i in range(len(points))]
    return np.argsort(angles)


def _get_angle(a, b1, b2):
    """
    Return the angle between ab1, ab2.

    Parameters
    ----------
    a, b1, b2:

    Returns
    -------
    angle: float
        angle in radians

    """
    angle1 = np.arctan2(b1[1] - a[1], b1[0] - a[0])
    angle2 = np.arctan2(b2[1] - a[1], b2[0] - a[0])

    angle = angle2 - angle1
    if angle < 0:
        angle = 2 * np.pi + angle
    return angle


def _dict_to_df(landcover_table):
    """Convert a dict landcover table to a df."""
    requires_geopandas()

    return gpd.GeoDataFrame.from_dict(landcover_table, orient="index")
