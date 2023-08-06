from pathlib import Path

from craft_documents.configuration.Semantic import Semantic
from craft_documents.configuration.Validator import Validator


class HeaderValidator(Validator):
    """
    Accepts an absolute or relative path to a tex-file.
    Relative paths will be interpreted as being inside
    `~/.config/craft/headers/`.

    Optional
    """

    def __init__(self):
        self._key = "header"
        self._semantic = Semantic.OPTIONAL

    def lint(self, value: str | Path) -> Path:
        match value:
            case str():
                path = Path(value) if value.endswith(".tex") else Path(value + ".tex")
            case Path():
                path = value

        if path.is_absolute():
            return path.resolve()
        else:
            return (self.configuration.main.parent / "headers/" / path).resolve()

    def validate(self, value: str) -> bool:
        path = Path(value)
        if path.is_file():
            return True
        else:
            self.configuration.pop(self.key, None)
            return False

    def default(self):
        """
        Return the default preamble.
        """
        pass
