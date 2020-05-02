"""
@fileName: calc_distance.py
@Author:
Sai Manogna Pentyala - spentyal@andrew.cmu.edu
"""

import numpy as np


def calc_distance(position1, position2):
    """
    Calculate distance between two points based on coordinates.
    This method use a spherical trigonometry to calculate distance
    """

    position1 = np.deg2rad(position1)
    position2 = np.deg2rad(position2)

    r = 6378137.0
    avg = (position1 - position2) / 2
    avg_lat = avg[:, 0:1]
    avg_lon = avg[:, 1:2]

    # return distance (m)
    return r * 2 * np.arcsin(
        np.sqrt(np.sin(avg_lat) ** 2 + np.cos(position1[:, 0:1]) * np.cos(position2[:, 0:1]) * np.sin(avg_lon ** 2)))
