#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 17:14:13 2023

@author: Anthony Chow

Shortcuts to access sources or some useful functions

"""

import os
from collections.abc import Iterable


class Sources:
    "module to access sources"

    def __init__(self, root_dir=None):
        if root_dir is None:
            root_dir = os.path.join(
                os.path.split(os.path.abspath(__file__))[0], 'sources')
        self.root_dir = root_dir

    @property
    def root_dir(self):
        "the root dir of the sources"
        return self.__root_dir

    @root_dir.setter
    def root_dir(self, name):
        if os.path.exists(name) and os.path.isdir(name):
            self.__root_dir = name
            self.__contains = {os.path.splitext(x)[0]: x
                               for x in os.listdir(name)}
        else:
            raise ValueError(f"path '{name}' does not exist or not a dir")

    def __getattribute__(self, name):
        try:
            obj = super().__getattribute__(name)
        except AttributeError:
            if name in self.__contains:
                path = os.path.join(self.root_dir, self.__contains[name])
                if os.path.isdir(path):
                    return type(self)(path)
                return path
            raise AttributeError(
                f"'{type(self)}' object has no attribute '{name}'")
        else:
            return obj


SOURCES = Sources()


def equal_pos(pos1, pos2):
    "test if the pos1 == pos2"
    if not all((isinstance(x, Iterable) for x in (pos1, pos2))):
        return False
    return all((x == y for x, y in zip(pos1, pos2)))

def in_rect(pos, rect):
    "test if the pos in rect"
    return all((a < x < a + b for x, (a, b) in zip(pos, zip(rect[:2], rect[2:]))))
