from pathlib import Path

from craft_documents.configuration.Semantic import Semantic
from craft_documents.configuration.Validator import Validator


class DocumentNameValidator(Validator):
    """
    Accepts a str as the name of the compiled document.
    Should not be an absolute or relative path.

    Optional
    """

    def __init__(self):
        self._key = "document-name"
        self._semantic = Semantic.OPTIONAL

    def lint(self, value: str | Path) -> str:
        """Append `.tex` if necessary"""
        match value:
            case str():
                return value.split("/")[-1].removesuffix(".tex") + ".tex"
            case Path():
                return value.name + value.suffix

    def validate(self, value: str) -> bool:
        """Check if the name exists in the current directory."""
        if Path(value).is_file():
            self.configuration.pop(self.key, None)
            return False
        else:
            return True
