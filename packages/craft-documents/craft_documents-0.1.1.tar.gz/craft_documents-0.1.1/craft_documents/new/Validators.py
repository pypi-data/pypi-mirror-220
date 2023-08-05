from pathlib import Path
from typing import Optional

from PyInquirer import ValidationError, Validator


class DocumentNamePromptValidator(Validator):
    @staticmethod
    def __validate__(text: str) -> Optional[ValidationError]:
        if not len(text) != 0:
            return ValidationError(
                message="The name of the file cannot be empty.",
                cursor_position=len(text),
            )
        path = Path(text if text.endswith(".tex") else text + ".tex")
        if path.exists():
            return ValidationError(
                message="A document with this name already exists.",
                cursor_position=len(text),
            )

    def validate(self, document):
        error = DocumentNamePromptValidator.__validate__(document.text)
        if error is not None:
            raise error


class ExerciseCountValidator(Validator):
    def validate(self, document):
        # TODO: Fix input: 0 being caught in except
        try:
            count = int(document.text)
            if count < 1:
                raise ValidationError(
                    message="Count should be at least 1!",
                    cursor_position=len(document.text),
                )
        except:
            raise ValidationError(
                message="Count should at least be 1.",
                cursor_position=len(document.text),
            )
