import re
from pathlib import Path

from rich import print

from craft_documents.common.helpers import create_list
from craft_documents.common.Prompter import Prompter
from craft_documents.common.Template import Template
from craft_documents.common.TexTemplate import TexTemplate
from craft_documents.configuration.Configuration import Configuration
from craft_documents.configuration.CraftExercisesValidator import (
    CraftExercisesValidator,
)


class Exercise(TexTemplate):
    """
    A class representing an exercise template.

    Exercise templates are stored in `.config/craft/exercises/`.
    They are always latex documents.
    """

    @property
    def contents(self) -> str:
        """
        Returns the entire contents.

        Use the properties `.body` and
        `.declarations` to return the parts
        that need to be included into the
        compiled document.
        """
        return super().contents

    @property
    def supplements(self) -> list[Template]:
        return self._supplements

    @property
    def unique_placeholder_values(self) -> dict[str, str]:
        return self._unique_placeholder_values

    @property
    def unique_placeholders(self) -> list[str]:
        return self._unique_placeholders

    @property
    def disambiguation_suffix(self) -> int | None:
        return self._disambiguation_suffix

    @disambiguation_suffix.setter
    def disambiguation_suffix(self, newValue: int):
        self._disambiguation_suffix = newValue

    @property
    def disambiguated_name(self) -> str:
        if self.disambiguation_suffix is None:
            return self.name
        else:
            return self.name + "-" + str(self.disambiguation_suffix)

    def __init__(self, path: Path, configuration: Configuration):
        """
        Initialize `self` as the tex-template.

        Initialize any additional supplemental template
        files. They are declared in a yaml block in the
        tex-template under the key `supplements`.
        """
        super().__init__(path, configuration)

        self._disambiguation_suffix = None

        self._supplements: list[Template] = []
        for path in create_list(self.yaml.get("supplements", [])):
            self._supplements.append(
                Template(self.configuration, self.path.parent / path)
            )

        self._unique_placeholder_values: dict[str, str] = {}
        self._unique_placeholders = create_list(
            self.yaml.get("unique-placeholders", [])
        )

        self.remove_documentclass()
        self.remove_include_preamble()

    def load(self):
        """
        Load the contents of the exercise template.
        """
        with self.path.open() as file:
            self._contents = file.read()
            self._disk_contents = self.contents

    def resolve_placeholders(self):
        if self.configuration.unique_exercise_placeholders:
            prompter = Prompter(self.unique_placeholder_values)
            prompter.ask(self.prompts)
            self.set_placeholders(self.unique_placeholder_values)
        else:
            # unique placeholders should always be prompted for
            for placeholder in self.unique_placeholders:
                self.configuration.pop(placeholder, None)

            prompter = Prompter(self.configuration)
            prompter.ask(self.prompts)
            self.set_placeholders(self.configuration)

    def clean_resolve_placeholders(self):
        if self.configuration.unique_exercise_placeholders:
            self._unique_placeholder_values = {}
        else:
            for placeholder in self.unique_placeholders:
                self.configuration.pop(placeholder, None)

    def rename_supplements(self):
        """
        Rename the supplements that are included in the template.

        This ensures disambiguation in case more than exercise of
        the same type is used.
        """
        for supplement in self.supplements:
            pattern = re.compile(supplement.name + supplement.extension)
            self._contents = re.sub(
                pattern, self.disambiguate_supplement(supplement), self.contents
            )

    def disambiguate_supplement(self, supplement: Template) -> str:
        """
        Create a disambiguated name for the given supplement.
        """
        if self.name != self.disambiguated_name:
            return (
                supplement.name
                + "-"
                + str(self.disambiguation_suffix)
                + supplement.extension
            )
        else:
            return supplement.name + supplement.extension
