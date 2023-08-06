# -*- coding: utf-8 -*-

"""Fonts.

"""

from importlib import resources


def names():
    """Return the name of the available fonts.

    Returns
    -------
    list of str
        Names of the available fonts.

    """
    return []


def path(name):
    """Return the path od the font.

    Parameters
    ----------
    name : str
        Name of the font.

    Returns
    -------
    str
        Path of the font file.

    """
    with resources.path(__package__, name) as file:
        file = str(file)
    return file
