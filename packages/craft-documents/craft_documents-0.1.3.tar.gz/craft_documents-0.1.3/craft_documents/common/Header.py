import re
from pathlib import Path

from craft_documents.common.TexTemplate import TexTemplate
from craft_documents.configuration.Configuration import Configuration
from craft_documents.configuration.CraftExercisesValidator import (
    CraftExercisesValidator,
)


class Header(TexTemplate):
    """
    A class representing a header template.

    Header templates are stored in `.config/craft/headers/`.
    They are always latex documents.
    """

    def __init__(self, path: Path, configuration: Configuration):
        super().__init__(path, configuration)

        self.remove_documentclass()
        self.remove_include_preamble()

    def load(self):
        """
        Remove the input statement of the preamble from the contents.
        """
        with self.path.open("r") as file:
            self._contents = file.read()
            self._disk_contents = self.contents

    def set_craft_exercises(self, value: str):
        pattern = re.compile(
            r"%s%s%s"
            % (
                self.placeholder_prefix,
                CraftExercisesValidator().key,
                self.placeholder_suffix,
            )
        )

        # escape `\`
        value = re.sub("\\\\", "\\\\\\\\", value)
        self._contents = re.sub(pattern, value, self.contents)
