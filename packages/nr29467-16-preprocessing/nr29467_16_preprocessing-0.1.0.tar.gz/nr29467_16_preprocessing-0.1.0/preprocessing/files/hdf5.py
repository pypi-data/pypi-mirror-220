from preprocessing.files.file_handler import FileException, FileHandler, logger
from preprocessing.files import config as cfg

import numpy as np
import h5py as h5

from os import PathLike
from pathlib import Path
from typing import List, Set, Optional


class H5Handler(FileHandler):
    """
    reads and writes hdf5 files
    """

    internal_path: List[str]
    chunking: bool
    compression: str
    verbose: bool

    def __init__(
        self,
        *,
        file: Optional[Path] = None,
        internal_path: str = "/data",
        chunking=True,
        compression="gzip",
        verbose: bool = False,
    ):
        """
        Args:
            file: the default path for this reader to read
            internal_path (str): the internal path to the data in the hdf5 file
            chunking: the chunking to use
            compression: the compression to use
            verbose (bool): log additional information about the file
        """
        super().__init__(file)
        self.internal_path = [i for i in internal_path.split("/") if i != ""]
        self.chunking = chunking
        self.compression = compression
        self.verbose = verbose

    @property
    def valid_ext(self) -> Set:
        return cfg.HDF5_SUFFIXES

    @property
    def ext(self):
        return cfg.HDF5_PREF_SUFFIX

    def shape(self, path: Path | None = None) -> tuple:
        """get the shape of the data in the hdf5 file"""
        if path is None:
            assert self.path is not None, "No path provided"
            path = self.path
        dataset = self._lazy_load(path)
        return tuple(dataset.shape)

    def _lazy_load(self, path: Path) -> h5.Dataset:
        """return the dataset without loading the data"""
        if not self._check_path(path):
            raise FileException("Invalid Path for HDF5 read.", path)

        data_handle = h5.File(path, "r")

        if self.verbose:
            logger.info(
                f"Reading data from {path} with internal path {self.internal_path}"
            )

        dataset = self._get_target_dataset(self.internal_path, data_handle)
        return dataset

    def _get_target_dataset(self, paths: List[str], group: h5.Group) -> h5.Dataset:
        """Take all the remaining parts of the path and look at the next subgroup
        Args:
            paths (List[str]): the remaining parts of the path
            group (h5.Group): the current group to look in
        """
        if paths[0] not in group.keys():
            raise FileException(
                f"Invalid Path for HDF5 read. {paths[0]} not found in {group}",
                str(group),
            )

        item = group[paths[0]]  # get the thing at the next level
        if self.verbose:
            logger.info(f"opening {paths[0]} in {group}")
        if isinstance(item, h5.Dataset):
            return item
        elif isinstance(item, h5.Group):
            return self._get_target_dataset(paths[1:], item)
        raise Exception(f"Invalid item type {type(item)}")

    def read(self, path: Optional[Path] = None) -> np.ndarray:
        """Returns a numpy array and chunking info when given a path
        to an HDF5 file.
        Args:
            path(pathlib.Path): The path to the HDF5 file.
            hdf5_path (str): The internal HDF5 path to the data.
        Returns:
            tuple(numpy.array, tuple(int, int)) : A numpy array
            for the data and a tuple with the chunking size.
        """
        p = self._get_optional_read_path(path)
        return self._lazy_load(p)[()]

    def write(
        self, path: Path, data: np.ndarray, name: Optional[str] = None
    ) -> PathLike:
        """
        Writes numpy array to hdf5 file. Takes an absolute path including filename
        or a path to a directory and a filename to use
        """
        path = self._get_complete_path(path, name)
        logger.info(f"Saving data of shape {data.shape} to {path}")
        with h5.File(path, "w") as f:
            f.create_dataset(
                "/" + "/".join(self.internal_path), data=data, chunks=self.chunking
            )
        return path
