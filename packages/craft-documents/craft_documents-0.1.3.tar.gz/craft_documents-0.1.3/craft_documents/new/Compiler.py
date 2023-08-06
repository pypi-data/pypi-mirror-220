import collections.abc
from pathlib import Path

from rich import print
from rich.console import Console

from craft_documents.configuration.DocumentNameValidator import DocumentNameValidator

collections.Mapping = collections.abc.Mapping  # type: ignore
from PyInquirer import prompt  # bugfix collections

from craft_documents.common.Exercise import Exercise
from craft_documents.common.Folder import Folder
from craft_documents.common.Header import Header
from craft_documents.common.Preamble import Preamble
from craft_documents.common.Prompt import Checkbox, Input
from craft_documents.configuration.Configuration import Configuration
from craft_documents.configuration.CraftExercisesValidator import (
    CraftExercisesValidator,
    ExerciseConfiguration,
)
from craft_documents.configuration.MultipleExercisesValidator import (
    MultipleExercisesValidator,
)
from craft_documents.new.Validators import (
    DocumentNamePromptValidator,
    ExerciseCountValidator,
)
from craft_documents.templates.TemplateManager import TemplateManager


class Compiler:
    """
    Class that handles compiling a document.
    """

    @property
    def configuration(self) -> Configuration:
        return self._configuration

    @property
    def preamble(self) -> Preamble:
        return self._preamble

    @property
    def header(self) -> Header:
        return self._header

    @property
    def exercises(self) -> list[Exercise]:
        """
        The exercises to be included in the compiled document.
        The order cannot be guaranteed.
        """
        return self._exercises

    @property
    def template_manager(self) -> TemplateManager:
        return self._template_manager

    @property
    def jobs(self) -> dict[Path, str]:
        """
        A dictionary of documents to create in the current
        working directory.
        """
        return self._jobs

    @property
    def document(self) -> str:
        """The compiled document."""
        if self.configuration.document_name is not None:
            return self.jobs.get(Path(self.configuration.document_name), "")
        else:
            return ""

    @document.setter
    def document(self, newValue: str):
        """
        Will only set the newValue if
        `self.configuration.document_name` is not None.
        """
        if self.configuration.document_name is not None:
            self.jobs[Path(self.configuration.document_name)] = newValue

    def __init__(self, configuration: Configuration):
        """
        You should guarantee values for `preamble` and `header` in the
        configuration when creating an instance of a Compiler.
        """

        self._configuration = configuration
        self._preamble = Preamble(configuration.preamble, configuration)
        self._template_manager = TemplateManager(self.configuration)
        self._jobs = {}

        if configuration.header is not None:
            self._header = Header(configuration.header, configuration)
        else:
            raise Exception("Unexpectedly found `None` at `configuration.header`.")
            # TODO: Handle Exception

        # Prompt for exercises if they are not defined in a configuration file
        if CraftExercisesValidator().key not in self.configuration:
            self.configuration[
                CraftExercisesValidator().key
            ] = self.prompt_for_exercises()

        self._exercises: list[Exercise] = []
        for config in self.configuration[CraftExercisesValidator().key].values():
            self._exercises += [
                Exercise(config["path"], self.configuration)
                for _ in range(config["count"])
            ]
        self.disambiguate_exercises()

        if DocumentNameValidator().key not in self.configuration:
            self.configuration[
                DocumentNameValidator().key
            ] = self.prompt_for_document_name()
            DocumentNameValidator().run(self.configuration)

    def compile(self):
        """
        Compile the document.
        """
        console = Console()
        print(
            "Drafting new [bold orange1]%s[/bold orange1] with [bold orange1]%s[/bold orange1] preamble...\n"
            % (self.header.name, self.preamble.name)
        )

        # preamble
        if self.preamble.will_prompt():
            print("")
            console.rule("[bold red]preamble")
        self.preamble.resolve_placeholders(self.configuration)
        print("[blue]==>[/blue] [bold]Compiled preamble :sparkles:")

        # header
        if self.header.will_prompt():
            print("")
            console.rule("[bold red]header")
        self.header.resolve_placeholders(self.configuration)
        print("[blue]==>[/blue] [bold]Compiled header :sparkles:")

        # exercises
        print("")
        console.rule("[bold red]exercises")
        for exercise in self.exercises:
            print(
                "[bold red]%s%s[/bold red]" % (exercise.name, exercise.extension)
                + " (%s)" % exercise.disambiguated_name
                if exercise.name != exercise.disambiguated_name
                else ""
            )
            exercise.resolve_placeholders()
            exercise.rename_supplements()
            print("[blue]==>[/blue] [bold]Compiled exercise :sparkles:\n")

            # handle the supplemental files for the exercise
            for supplement in exercise.supplements:
                print(
                    "[bold red]%s%s[/bold red]"
                    % (exercise.disambiguated_name, supplement.extension)
                )

                supplement.resolve_placeholders(
                    exercise.unique_placeholder_values
                    if self.configuration.unique_exercise_placeholders
                    else self.configuration
                )
                print("[blue]==>[/blue] [bold]Compiled supplemental file :sparkles:")

                supplement_file = Path(exercise.disambiguate_supplement(supplement))
                self.jobs[supplement_file] = supplement.contents
                print("[blue]==>[/blue] [bold]Copied to current directory :printer:\n")

            exercise.clean_resolve_placeholders()

        # Glue together the compiled document.

        # Preamble
        self.document += "% Preamble " + "-" * 66 + " %\n"
        self.document += self.preamble.contents  # preamble

        # Header
        if len(self.header.declarations) != 0:
            self.document += "\n% Header " + "-" * 67 + " %\n"
        self.document += self.header.declarations  # declarations in header

        # Exercises
        extracted_declarations = set()
        body_exercises = ""
        for exercise in self.exercises:
            if (
                len(exercise.declarations) != 0
                and exercise.name not in extracted_declarations
            ):
                self.document += (
                    "% "
                    + exercise.name
                    + " "
                    + "-" * (79 - 5 - len(exercise.name))
                    + " %\n"
                )
                self.document += exercise.declarations  # declarations in exercises
                extracted_declarations.add(exercise.name)
            if len(exercise.body) != 0:
                body_exercises += (
                    "% "
                    + exercise.disambiguated_name
                    + " "
                    + "-" * (79 - 5 - len(exercise.disambiguated_name))
                    + " %\n"
                )
                body_exercises += exercise.body
                if not exercise.body.endswith("\n\n"):
                    body_exercises += "\n"

        self.header.set_craft_exercises(body_exercises)
        self.document += "\\begin{document}\n"
        self.document += self.header.body
        self.document += "\\end{document}\n"

        self.work_jobs()

    def work_jobs(self):
        """
        Create the files.

        This is overridden in the test_implementation to instead print
        to the console.
        """
        for path, contents in self.jobs.items():
            path.write_text(contents)

    def prompt_for_document_name(self) -> str:
        """
        Prompt the user what the compiled document should be called.
        """
        key = DocumentNameValidator().key
        question = Input(
            key,
            message="What the compiled document be called?",
            default=self.header.name,
            validate=DocumentNamePromptValidator,
        )
        answer = prompt(question)
        return answer[key]

    def prompt_for_exercises(self) -> dict:
        """
        Prompt the user which exercises should be included.
        """
        key = CraftExercisesValidator().key
        question = Checkbox(
            CraftExercisesValidator().key,
            [
                Checkbox.Choice(name=exercise.name)
                for exercise in self.template_manager.exercises
            ],
            "Which exercises should be included?",
            when=lambda _: key not in self.configuration,
        )

        # answer = ['intervals']
        answer = prompt(question)[key]
        # answer = {'intervals': {'count': ..., 'path': ... }}
        answer = {
            exercise_name: ExerciseConfiguration(self.configuration, exercise_name)
            for exercise_name in answer
        }

        # multiple exercises
        if self.configuration[MultipleExercisesValidator().key]:
            for exercise_name, config in answer.items():
                question = Input(
                    "count",
                    message="How many '%s'?" % exercise_name,
                    default=str(config["count"]),
                    validate=ExerciseCountValidator,
                )
                count = prompt(question)["count"]
                config["count"] = int(count)

        return answer

    def disambiguate_exercises(self):
        count = {}
        for exercise in self.exercises:
            if self.configuration["craft-exercises"][exercise.name]["count"] > 1:
                add = count.get(exercise.name, 1)
                exercise.disambiguation_suffix = add
                count[exercise.name] = count.get(exercise.name, 1) + 1
