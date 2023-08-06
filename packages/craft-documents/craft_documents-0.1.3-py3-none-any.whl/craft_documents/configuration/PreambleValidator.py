from pathlib import Path

import typer
from rich import print

from craft_documents.configuration.Semantic import Semantic
from craft_documents.configuration.Validator import Validator


class PreambleValidator(Validator):
    """
    Accepts an absolute or relative path to a tex-file.
    Relative paths will be interpreted as being inside
    `~/.config/craft/preambles/`.

    Defaults to an absolute path to a tex-file.
    """

    def __init__(self):
        self._key = "preamble"
        self._semantic = Semantic.REQUIRED

    def lint(self, value: str | Path) -> Path:
        match value:
            case str():
                path = Path(value) if value.endswith(".tex") else Path(value + ".tex")
            case Path():
                path = value
        if path.is_absolute():
            return path.resolve()
        else:
            return (self.configuration.main.parent / "preambles/" / path).resolve()

    def validate(self, value: str) -> bool:
        path = Path(value)
        if path.is_file():
            return True
        else:
            return False

    def default(self) -> Path:
        """
        Return the default preamble.
        """
        default = "default.tex"

        path: Path = self.configuration.main.parent / ("preambles/" + default)
        if path.is_file():
            return path.resolve()
        else:
            print(
                "[blue]==>[/blue] Created the default preamble at '%s' :sparkles:\n"
                % path
            )
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch(exist_ok=True)
            path.write_text(r"\documentclass{scrreport}")
            print(
                "Run 'craft templates fetch --verbose' to fetch more templates from GitHub.\n"
            )
            return path
