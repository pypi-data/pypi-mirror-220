#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 17:18:47 2023

@author: anthony

a library of output functions

"""
import numpy as np
import png
from kiri_pathfinding.map_generator import COLORS


COLORS_ARRAY = np.array([[int(c[i: i + 2], 16)for i in (1, 3, 5)] + [255]
                         for c in COLORS], dtype=np.uint8)


def map_to_png(data_map, save=None):
    """
    transform a map into a png image

    params
    ------
    data_map : np.ndarray,
        data to describe the map
    save : str or file-like object,
        the dir or file to save the image

    """
    colored_data = COLORS_ARRAY[data_map.flatten()].reshape(
        (data_map.shape[0], -1))
    pic = png.from_array(colored_data, "RGBA")
    if isinstance(save, str):
        pic.save(save)
    else:
        pic.write(save)
