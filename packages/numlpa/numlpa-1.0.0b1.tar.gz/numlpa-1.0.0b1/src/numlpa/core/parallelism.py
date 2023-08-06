# -*- coding: utf-8 -*-

"""Parallelism module.

This module allows the identification of the node.
"""

from logging import getLogger, Formatter
from os import getenv

from numlpa import config


logger = getLogger(__name__)


def get_rank():
    """Return the node identifier.

    Returns
    -------
    int
        Id of the node.

    """
    logger.debug("retrieving rank")
    variable = config.get(__name__, 'rank')
    return int(getenv(variable, '0'))


def get_size():
    """Return the number of nodes.

    Returns
    -------
    int
        Number of nodes.

    """
    logger.debug("retrieving size")
    variable = config.get(__name__, 'size')
    return int(getenv(variable, '1'))


def get_format():
    """

    Returns
    -------
    str
        Logging format.

    """
    fomatter = []
    fomatter.append('%(levelname)s')
    size = get_size()
    if size > 1:
        width = len(str(size-1))
        fomatter.append(str(get_rank()).zfill(width))
    fomatter.append('%(name)s')
    fomatter.append('%(message)s')
    return ':'.join(fomatter)


getLogger().handlers[0].setFormatter(Formatter(get_format()))
