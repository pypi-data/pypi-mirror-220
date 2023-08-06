from __future__ import annotations

from pathlib import Path
from typing import Any, List

import yaml
from rich import print

from craft_documents.configuration.AllowEvalValidator import AllowEvalValidator
from craft_documents.configuration.DocumentNameValidator import DocumentNameValidator
from craft_documents.configuration.CraftExercisesValidator import (
    CraftExercisesValidator,
)
from craft_documents.configuration.HeaderValidator import HeaderValidator
from craft_documents.configuration.MultipleExercisesValidator import (
    MultipleExercisesValidator,
)
from craft_documents.configuration.PreambleValidator import PreambleValidator
from craft_documents.configuration.RemoveCommentsValidator import (
    RemoveCommentsValidator,
)
from craft_documents.configuration.TokensValidator import TokensValidator
from craft_documents.configuration.UniqueExercisePlaceholdersValidator import (
    UniqueExercisePlaceholdersValidator,
)
from craft_documents.configuration.Validator import Validator
from craft_documents.configuration.VerboseValidator import VerboseValidator


class Configuration(dict):
    """
    A dictionary like class that represents the configuration
    of the user.

    ### Settings

    - `preamble`: required, defaults to `default.tex`
    - `allow_eval`: required, defaults to `False`
    - `remove_comments`: required, defaults to `False`
    - `craft-exercises`: optional
    - `multiple-exercises`: required, defaults to `True`
    - `tokens`: required, loads defaults for `.tex` and `.ly`
    """

    @property
    def validators(self) -> list[Validator]:
        return self._validators

    @property
    def main(self) -> Path:
        return self._main

    @property
    def root(self) -> Path:
        return self._root

    @property
    def cwd(self) -> Path:
        return self._cwd

    @property
    def preamble(self) -> Path:
        return self[PreambleValidator().key]

    @property
    def header(self) -> Path | None:
        return self.get(HeaderValidator().key, None)

    @header.setter
    def header(self, name: str | Path):
        """
        Set this property with the name of the header. It can optionally have the suffix
        `.tex`.

        #TODO: Settings with a relative path is not supported.
        """
        v = HeaderValidator()
        old_value = self.header

        self[v.key] = name
        v.run(self)
        if self.header is None:
            self[v.key] = old_value
            if self.header is None:
                self.pop(v.key)

    @property
    def allow_eval(self) -> bool:
        return self[AllowEvalValidator().key]

    @property
    def verbose(self) -> bool:
        return self[VerboseValidator().key]

    @property
    def remove_comments(self) -> bool:
        return self[RemoveCommentsValidator().key]

    @property
    def craft_exercises(self) -> dict[str, dict[str, Any]] | None:
        return self.get(CraftExercisesValidator().key, None)

    @property
    def multiple_exercises(self) -> bool:
        return self[AllowEvalValidator().key]

    @property
    def unique_exercise_placeholders(self) -> bool:
        return self[UniqueExercisePlaceholdersValidator().key]

    @property
    def document_name(self) -> str:
        return self.get(DocumentNameValidator().key, None)

    def __init__(
        self,
        main: Path = Path.home() / ".config/craft/craftrc",
        root: Path = Path.home(),
        cwd: Path = Path.cwd(),
        *args,
        **kwargs,
    ):
        self._main = main
        self._root = root
        self._cwd = cwd

        self.update(*args, **kwargs)
        self.load()
        self.validate()

    def load(self):
        """
        Load the configuration from the disk.

        The user can configure craft in yaml-formatted
        configuration files: `craftrc`, `.craftrc`.

        Draft will read all configuration files from
        the current working directory to home and
        accumulate their values. Files closer to
        the current working directory take
        precedence.

        Additionally there is one configuration file
        at `~/.config/craft/craftrc` which stores
        gets read last. It stores global configuration
        such as prefixes for single-line-comments for
        a specific file extension. Make sure to escape
        them correctly.
        """
        files: List[str] = ["craftrc", ".craftrc"]
        directory: Path = self.cwd

        while True:
            for file in files:
                file_path: Path = directory / file
                if not file_path.is_file():
                    continue
                try:
                    data = yaml.safe_load(file_path.open())
                    # Insert any new values
                    for key, value in data.items():
                        if key not in self:
                            self[key] = value
                except:
                    continue
            # Exit if the root directory has been reached
            if directory == self.root:
                break

            # Move up to the parent directory
            directory = directory.parent

        # read file at `~/.config/craft/craftrc`
        try:
            data = yaml.safe_load(self.main.open())
            for key, value in data.items():
                if key not in self:
                    self[key] = value
        except:
            pass

    def validate(self):
        """
        Validate the configuration and employ resolving strategies if
        necessary. This is done by setting and running every validator in
        `self.validators`.
        """
        # Create the configuration if it doesn't exists
        if (
            not self.main.parent.is_dir()
            or not (self.main.parent / "preambles/").is_dir()
            or not (self.main.parent / "headers/").is_dir()
            or not (self.main.parent / "exercises/").is_dir()
        ):
            self.main.parent.mkdir(parents=True, exist_ok=True)
            (self.main.parent / "preambles/").mkdir(parents=True, exist_ok=True)
            (self.main.parent / "headers/").mkdir(parents=True, exist_ok=True)
            (self.main.parent / "exercises/").mkdir(parents=True, exist_ok=True)
            print(
                "[blue]==>[/blue] Created the templates folder at '%s' :sparkles:"
                % self.main.parent
            )

        self._validators = [
            PreambleValidator(),
            AllowEvalValidator(),
            RemoveCommentsValidator(),
            AllowEvalValidator(),
            CraftExercisesValidator(),
            MultipleExercisesValidator(),
            TokensValidator(),
            HeaderValidator(),
            UniqueExercisePlaceholdersValidator(),
            DocumentNameValidator(),
            VerboseValidator(),
        ]
        for validator in self.validators:
            validator.run(self)
