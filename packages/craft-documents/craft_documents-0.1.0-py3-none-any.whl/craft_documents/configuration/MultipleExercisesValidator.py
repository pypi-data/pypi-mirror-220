from craft_documents.configuration.Semantic import Semantic
from craft_documents.configuration.Validator import Validator


class MultipleExercisesValidator(Validator):
    """
    Boolean that defaults to True.
    """

    def __init__(self):
        self._key = "multiple-exercises"
        self._semantic = Semantic.REQUIRED

    def validate(self, value: bool) -> bool:
        if isinstance(value, bool):
            return True
        else:
            return False

    def default(self) -> bool:
        return True
