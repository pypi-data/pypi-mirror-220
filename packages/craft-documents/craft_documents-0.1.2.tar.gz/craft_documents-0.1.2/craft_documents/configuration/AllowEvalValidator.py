from craft_documents.configuration.Semantic import Semantic
from craft_documents.configuration.Validator import Validator


class AllowEvalValidator(Validator):
    """
    Boolean that defaults to False.
    """

    def __init__(self):
        self._key = "allow_eval"
        self._semantic = Semantic.REQUIRED

    def validate(self, value: bool) -> bool:
        if isinstance(value, bool):
            return True
        else:
            return False

    def default(self) -> bool:
        return False
