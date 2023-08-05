from craft_documents.configuration.Semantic import Semantic
from craft_documents.configuration.Validator import Validator


class UniqueExercisePlaceholdersValidator(Validator):
    """
    Required, defaults to `False`.

    Controls whether the placeholders in an exercise template
    should be sandbox to one template or added to the global
    configuration.
    """

    def __init__(self):
        self._key = "unique_exercise_placeholders"
        self._semantic = Semantic.REQUIRED

    def validate(self, value: bool) -> bool:
        if isinstance(value, bool):
            return True
        else:
            return False

    def default(self) -> bool:
        return False
