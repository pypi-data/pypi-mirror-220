from abc import ABC, abstractmethod
from typing import Set, List
import logging
from pathlib import Path
from os import PathLike
import os

import numpy as np


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class FileException(Exception):
    def __init__(self, message: str, path: str | PathLike):
        self.message = message
        self.path = Path(path)

    def __str__(self) -> str:
        return self.message


class FileHandler(ABC):
    path: Path | None

    def __init__(self, file: Path | None = None):
        self.path = file

    def check_ext(self, path: Path) -> bool:
        """check that the file extension is valid for this handler"""
        return path.suffix in self.valid_ext

    @property
    @abstractmethod
    def valid_ext(self) -> Set:
        pass

    @property
    @abstractmethod
    def ext(self) -> str:
        """Define the extension to use when saving files"""
        pass

    @abstractmethod
    def shape(self, path: PathLike) -> tuple:
        """get the shape of the data in the file"""
        pass

    @abstractmethod
    def read(self, path: PathLike | None = None) -> np.ndarray:
        pass

    @abstractmethod
    def write(
        self, path: PathLike, data: np.ndarray, name: str | None = None
    ) -> PathLike:
        """write the data to a file at the specified path. Specify the absolute path or path to a directory
        and a filename. In this case the default extension for the filetype will be used
            Args:
                path: path to save the file to
                data: data to save
                name (optional): if the path provided is a directory, the filename can be specified here and the default
                    ext for that exporter will be applied
        """
        pass

    def get_readable_files(self, dir: Path, strict: bool = False) -> List[Path]:
        """
        create a list of all the files in a directory that this handler is capable of reading.
        if the path is not a valid directory, an empty list is returned
        Args:
            dir: the path to the directory to search
            strict ? use only self.ext : use self.valid_ext
        """
        files = []
        if strict:
            target_ext = set([self.ext])
        else:
            target_ext = self.valid_ext
        if dir.exists():
            for ext in target_ext:
                ext_files = [f for f in dir.iterdir() if f.suffix == ext]
                files += ext_files
            logger.info(f"found {len(files)} readable files in {dir}")
        return files

    def _check_path(self, path: Path) -> bool:
        """checks the type of path and checks that the file extension is correct for import"""
        if not isinstance(path, Path):
            logger.warning(f"not pathlike, is instance of {type(path)}")
            return False
        if os.path.isfile(path) & (path.suffix in self.valid_ext):
            return True
        else:
            logger.warning(f"filetype should be one of {self.valid_ext}")
        return False

    def _get_complete_path(self, path: Path, name: str | None) -> Path:
        """constructs and validates the entire path to the file location for export"""
        if name is not None:
            """if a filename is specified then we will combine it with the path and use the default extension"""
            path = path / Path(name).with_suffix(self.ext)
        if not path.parent.absolute().exists():
            os.makedirs(path.parent.absolute(), exist_ok=True)
        return path

    def _get_optional_read_path(self, arg_path: Path | None) -> Path:
        """if the path is a directory, use the default extension for this file type"""
        if isinstance(arg_path, Path):
            return arg_path
        else:
            if self.path is None:
                raise ValueError("No path provided")
            return self.path
