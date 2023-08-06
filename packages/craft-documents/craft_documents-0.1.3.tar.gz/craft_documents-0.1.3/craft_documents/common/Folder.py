import os
from abc import ABC
from pathlib import Path
from typing import List

from craft_documents.common.DiskRepresentable import DiskRepresentable


class Folder(ABC, DiskRepresentable):
    """
    Abstract class representing a folder on the disk.

    Conforming types:
    - Configuration
    """

    @property
    def subfiles(self) -> List[Path]:
        return self._subfiles

    @property
    def subfolders(self) -> List[Path]:
        return self._subfolders

    def __init__(self, path: Path):
        self._path = path.resolve()
        self.load()

    def load(self):
        """
        Populate self._subfiles with a list holding
        Path objects to all the files in the folder.

        Populate self._subfolders with a list holding
        Path obhjects to all the folder in the folder.

        Subtypes overwriting this method, must make sure
        to create those properties or best call
        `super().load()`.
        """
        self._subfiles: List[Path] = []
        self._subfolders: List[Path] = []

        for subpath in self.path.iterdir():
            if subpath.is_file():
                self._subfiles.append(subpath)
            elif subpath.is_dir():
                self._subfolders.append(subpath)

    def open(self):
        """`open <self.path>`"""
        os.system("open '%s'" % self.path)
