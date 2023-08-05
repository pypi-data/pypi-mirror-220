from abc import abstractmethod
from pathlib import Path
from typing import Protocol


class DiskRepresentable(Protocol):
    """
    A protocol representing a file or folder on the disk.

    Conforming types:
    - Folder (ABC)
    - File (ABC)
    """

    _path: Path

    @property
    def path(self) -> Path:
        return self._path

    @property
    def name(self) -> str:
        return self.path.stem

    @abstractmethod
    def load(self):
        """
        Loads data from the disk.

        Override this endpoint in tests to load the data from
        a folder in this directory or to instantiate the type
        with mock data.

        Usually, implementations would want to call `self.load()`
        as the last action in their initializer.
        """
        raise NotImplementedError
