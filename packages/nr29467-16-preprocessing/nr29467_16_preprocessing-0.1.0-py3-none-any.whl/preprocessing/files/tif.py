from os import PathLike
from pathlib import Path
import numpy as np

import tifffile

from preprocessing.files.file_handler import FileHandler

class TiffHandler(FileHandler):
    '''
    reads and writes tiff files
    '''
    def __init__(
        self,
        *,
        file: Path | None = None,
        verbose: bool = False,
    ):
        super().__init__(file)
        self.verbose = verbose

    @property
    def valid_ext(self):
        return {".tif", ".tiff"}
    
    @property
    def ext(self):
        return ".tif"
    
    def shape(self, path: Path | None = None) -> tuple:
        # get the shape of the data in the tiff file without loading it
        if path is None:
            assert self.path is not None, "No path provided"
            path = self.path
        return tifffile.imread(path).shape

    def read(self, path: Path | None = None) -> np.ndarray:
        '''
        Return the data in the tiff file as a numpy array
        Args:
            path (Path): the path to the tiff file
        Returns:
            np.ndarray: the data in the tiff file
        '''
        p = self._get_optional_read_path(path)
        return tifffile.imread(p)
    
    def write(
        self,
        path: Path,
        data: np.ndarray,
        name: str | None = None
    ):
        '''
        Write the data to the tiff file
        Args:
            data (np.ndarray): the data to write
            path (Path): the path to the tiff file
        '''
        assert isinstance
        path = self._get_complete_path(path, name)
        tifffile.imwrite(path, data)

    