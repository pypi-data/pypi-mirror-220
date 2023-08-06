from pathlib import Path

from craft_documents.common.Exercise import Exercise
from craft_documents.common.Folder import Folder
from craft_documents.common.Header import Header
from craft_documents.common.Preamble import Preamble
from craft_documents.configuration.Configuration import Configuration


class TemplateManager:
    """
    A class that manages the templates installed on the system.
    """

    @property
    def folder(self) -> Folder:
        """The folder of the templates: `~/.config/craft/`."""
        return self._folder

    @property
    def headers(self) -> list[Header]:
        """List of all Headers."""
        return self._headers

    @property
    def headers_path(self) -> Path:
        return self.folder.path / "headers/"

    @property
    def exercises(self) -> list[Exercise]:
        """List of all Exercises."""
        return self._exercises

    @property
    def exercises_path(self) -> Path:
        return self.folder.path / "exercises/"

    @property
    def preambles(self) -> list[Preamble]:
        """List of all Preambles."""
        return self._preambles

    @property
    def preambles_path(self) -> Path:
        return self.folder.path / "preambles/"

    def __init__(self, configuration: Configuration):
        self._folder = Folder(configuration.main.parent)

        self._headers = [
            Header(path, configuration)
            for headers in self.folder.subfolders
            for path in Folder(headers).subfiles
            if headers.name == "headers"
            if path.suffix == ".tex"
        ]

        self._exercises = [
            Exercise(path, configuration)
            for exercises in self.folder.subfolders
            for path in Folder(exercises).subfiles
            if exercises.name == "exercises"
            if path.suffix == ".tex"
        ]

        self._preambles = [
            Preamble(path, configuration)
            for preambles in self.folder.subfolders
            for path in Folder(preambles).subfiles
            if preambles.name == "preambles"
            if path.suffix == ".tex"
        ]

    def new_preamble(self, name: str, contents: str):
        self.preambles_path.mkdir(parents=True, exist_ok=True)
        path = self.preambles_path / name
        path.write_text(contents)

    def new_header(self, name: str, contents: str):
        self.headers_path.mkdir(parents=True, exist_ok=True)
        path = self.headers_path / name
        path.write_text(contents)

    def new_exercise(self, name: str, contents: str):
        self.exercises_path.mkdir(parents=True, exist_ok=True)
        path = self.exercises_path / name
        path.write_text(contents)
