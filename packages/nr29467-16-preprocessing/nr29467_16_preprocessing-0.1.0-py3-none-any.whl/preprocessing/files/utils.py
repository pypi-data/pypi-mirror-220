from pathlib import Path

from preprocessing.files.hdf5 import H5Handler
from preprocessing.files.npy import NPYHandler
from preprocessing.files.tif import TiffHandler
from preprocessing.files.file_handler import FileHandler

def get_handler(path: Path, *args, **kwargs) -> FileHandler:
    for handler in [H5Handler, NPYHandler, TiffHandler]:
        if handler().check_ext(path):
            return handler(*args, **kwargs)
    raise ValueError(f'No handler found for {path}')