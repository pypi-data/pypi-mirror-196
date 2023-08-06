# -*- coding: utf-8 -*-

"""Storage module.

This module implements the functionalities to save and load files.
"""

import tarfile
import zipfile
import json
import pickle
from io import BytesIO
from logging import getLogger
from os import getpid, listdir, mkdir, remove
from os.path import exists, isdir, join
from signal import signal, SIGINT, SIGTERM
from sys import exit as sys_exit
from time import time


logger = getLogger(__name__)


class Container:
    """File container handler.

    This class implements a single interface for writing and reading
    files in a tarball, a zip archive, or a directory.

    Attributes
    ----------
    path : str
        Path to the container.
    format : str
        Container type ('tar', 'zip' or 'dir').
    killed : bool
        Set to True when a stop signal is received during a write.
    signum : int
        Signal number.
    lockfile : str
        Path of the locking file.

    """

    def __init__(self, path, **kwargs):
        """Initialize the container handler.

        Parameters
        ----------
        path : str
            Path to the container.

        Keyword Arguments
        -----------------
        create : bool
            Set to True if the container can be created.

        """
        self.path = path
        if path.endswith('.tar'):
            self.format = 'tar'
        elif path.endswith('.zip'):
            self.format = 'zip'
        else:
            self.format = 'dir'
        self.killed = False
        self.signum = None
        self.lockfile = f'{self.path}.lock'
        if kwargs.get('create', False):
            self.create()
        self.check()

    def __str__(self):
        """Return a string representation of the container.

        Returns
        -------
        str
            String representation of the container.

        """
        return self.path

    def create(self):
        """Create the container in the file system.

        """
        if exists(self.path):
            return
        if self.format == 'tar':
            with tarfile.open(self.path, 'w'):
                pass
        elif self.format == 'zip':
            with zipfile.ZipFile(self.path, 'w'):
                pass
        elif self.format == 'dir':
            mkdir(self.path)

    def check(self):
        """Ensure that the container exists and is valid.

        Raises
        ------
        Exception
            If reading or creating the container is impossible.

        """
        if not exists(self.path):
            raise FileNotFoundError(f"container '{self.path}' not found")
        if self.format == 'tar':
            if not tarfile.is_tarfile(self.path):
                raise FileExistsError(f"'{self}' is not a valid tar file")
        elif self.format == 'zip':
            if not zipfile.is_zipfile(self.path):
                raise FileExistsError(f"'{self}' is not a valid zip file")
        elif self.format == 'dir':
            if not isdir(self.path):
                raise FileExistsError(f"'{self}' is an existing file")

    def names(self):
        """Return the name of the files stored in the container.

        Returns
        -------
        list of str
            Name of the files stored in the container.

        """
        if self.format == 'tar':
            with tarfile.open(self.path, 'r') as archive:
                listing = archive.getnames()
        elif self.format == 'zip':
            with zipfile.ZipFile(self.path, 'r') as archive:
                listing = archive.namelist()
        elif self.format == 'dir':
            listing = listdir(self.path)
        return sorted(listing)

    def lock(self):
        """Lock the container.

        """
        logger.debug("locking %s", self)
        locked = False
        while not locked:
            try:
                with open(self.lockfile, 'x', encoding='utf-8') as file:
                    file.write(str(getpid()))
                locked = True
            except IOError:
                pass

    def unlock(self):
        """Unlock the container.

        """
        logger.debug("unlocking %s", self)
        remove(self.lockfile)

    def add(self, series, name):
        """Add a file in the container.

        Parameters
        ----------
        series : bytes
            File data.
        name : str
            File name.

        """
        sigint = signal(SIGINT, self.handler)
        sigterm = signal(SIGTERM, self.handler)
        if self.format == 'tar':
            self.lock()
            with tarfile.open(self.path, 'a') as archive:
                info = tarfile.TarInfo(name)
                info.mtime = time()
                info.size = len(series)
                archive.addfile(info, BytesIO(series))
            self.unlock()
        elif self.format == 'zip':
            self.lock()
            with zipfile.ZipFile(self.path, 'a') as archive:
                archive.writestr(name, series)
            self.unlock()
        elif self.format == 'dir':
            with open(join(self.path, name), 'wb') as file:
                file.write(series)
        if self.killed:
            if self.signum == SIGINT:
                raise KeyboardInterrupt
            sys_exit(143)
        signal(SIGINT, sigint)
        signal(SIGTERM, sigterm)

    def get(self, name):
        """Return the file data.

        Parameters
        ----------
        name : str
            Name of the file to retrieve.

        Returns
        -------
        bytes
            File data.

        """
        if self.format == 'tar':
            with tarfile.open(self.path, 'r') as archive:
                buffer = archive.extractfile(name)
                series = bytes(buffer.read())
        elif self.format == 'zip':
            with zipfile.ZipFile(self.path, 'r') as archive:
                series = archive.read(name)
        elif self.format == 'dir':
            with open(join(self.path, name), mode='rb') as file:
                series = file.read()
        return series

    def handler(self, signum, frame=None):
        """Custom signal handler.

        Parameters
        ----------
        signum : int
            Signal number.
        frame : frame object
            Current stack frame.

        """
        self.killed = True
        _ = frame
        self.signum = signum


def serialize(data, name):
    """Return the serialized data.

    Parameters
    ----------
    data : dict
        Data to be serialized.
    name : str
        Serialization format or file name.

    Returns
    -------
    bytes
        Serialized data.

    """
    if name.endswith('json'):
        return json.dumps(data).encode('utf-8')
    if name.endswith('pyc'):
        return pickle.dumps(data)
    raise RuntimeError(f"invalid serialization format '{name}'")


def deserialize(series, name):
    """Return the deserialized data.

    Parameters
    ----------
    series : bytes
        Data to be deserialized.
    name : str
        Serialization format or file name.

    Returns
    -------
    dict
        Deserialized data.

    """
    if name.endswith('json'):
        return json.loads(series.decode('utf-8'))
    if name.endswith('pyc'):
        return pickle.loads(series)
    raise RuntimeError(f"invalid deserialization format '{name}'")
