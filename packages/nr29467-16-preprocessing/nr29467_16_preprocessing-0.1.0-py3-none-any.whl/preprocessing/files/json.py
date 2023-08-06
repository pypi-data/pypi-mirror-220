import json
from os import PathLike
from pathlib import Path
from typing import Set, Optional

from preprocessing.files.file_handler import FileHandler


class JSONHandler(FileHandler):
    def __init__(self, file: Path | None = None):
        super().__init__(file)

    def shape(self, path: Path) -> tuple:
        """get the shape of the data in the json file"""
        return ()

    def read(self, path: Path | None = None) -> dict:
        p = self._get_optional_read_path(path)
        with open(p, "r") as f:
            return json.load(f)

    def write(self, path: Path, data: dict, name: str | None = None) -> PathLike:
        path = self._get_complete_path(path, name)
        with open(path, "w") as f:
            json.dump(data, f)
        return path

    @property
    def valid_ext(self) -> Set:
        return {".json"}

    @property
    def ext(self) -> str:
        return ".json"
