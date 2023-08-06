from os import PathLike
from pathlib import Path
from typing import List, Set

import numpy as np
from skimage import io

from preprocessing.files import config as cfg
from preprocessing.files.file_handler import FileHandler


class PNGHandler(FileHandler):
    def __init__(
        self,
        grayscale: bool = False,
        *,
        file: Path | None = None,
    ) -> None:
        """
        Args:
            grayscale (bool): if True, the image will be read as grayscale
            Transforms (List[Transform]): a list of transforms to apply to the image before saving
        """
        super().__init__(file)
        self.grayscale = grayscale

    @property
    def valid_ext(self) -> Set:
        return cfg.PNG_SUFFIXES

    @property
    def ext(self):
        return cfg.PNG_PREF_SUFFIX

    def shape(self, path: Path) -> tuple:
        """get the shape of the data in the png file"""
        return tuple(self.read(path).shape)

    def read(self, path: Path | None = None):
        """Reads the image data from a png
        Args:
            path: path to the png file
        Returns: np.ndarray: numpy array with the image data"""
        p = self._get_optional_read_path(path)
        return io.imread(p, as_gray=self.grayscale)

    def write(self, path: Path, data: np.ndarray, name: str | None = None) -> PathLike:
        """
        Writes a 2d numpy array to a PNG file. Takes an absolute path including filename
        or a path to a directory and a filename to use"""
        path = self._get_complete_path(path, name)
        # TODO: Allow saving at higher bit depth
        # if data.dtype != np.uint8:
        #   data = img_as_ubyte(data)
        io.imsave(path, data, check_contrast=False)
        return path
