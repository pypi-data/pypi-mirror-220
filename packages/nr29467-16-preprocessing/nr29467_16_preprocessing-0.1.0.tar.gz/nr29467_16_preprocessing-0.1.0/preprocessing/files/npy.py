from os import PathLike
from pathlib import Path
from typing import Set

import numpy as np

from preprocessing.files.file_handler import FileHandler


class NPYHandler(FileHandler):
    def __init__(self, *, file: Path | None = None, allow_pickle=False) -> None:
        super().__init__(file)
        self.allow_pickle = allow_pickle

    @property
    def valid_ext(self) -> Set:
        return {".npy"}

    @property
    def ext(self) -> str:
        return ".npy"

    def shape(self, path: Path) -> tuple:
        """get the shape of the data in the npy file"""
        return tuple(self.read(path).shape)

    def read(self, path: Path | None = None) -> np.ndarray:
        """
        read a numpy array from an npy file
        Args:
            path: path to file to read
        """
        p = self._get_optional_read_path(path)
        return np.load(p, allow_pickle=self.allow_pickle)

    def write(self, path: Path, data: np.ndarray, name: str | None = None) -> PathLike:
        """
        Writes a numpy array to a npy file
        Args:
            path: filepath to save to or directory if name is supplied
            data: data to save
            name (optional):
        Returns:
            (Path) the path to the file that was saved
        """
        path = self._get_complete_path(path, name)
        np.save(path, data, allow_pickle=self.allow_pickle)
        return path
