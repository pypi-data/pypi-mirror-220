import collections.abc

import typer

from craft_documents.templates.TemplateManager import TemplateManager

collections.Mapping = collections.abc.Mapping  # type: ignore
from pathlib import Path

from PyInquirer import prompt
from rich import print as rprint

from craft_documents.common.helpers import fetch_github_directory
from craft_documents.common.Prompt import Confirm


def fetch_implementation(
    verbose: bool, templates_manager: TemplateManager, app: typer.Typer
):
    print("Fetching templates from GitHub...")

    templates_are_uptodate = True

    owner = "tobiashauser"
    repo = "42.43-draft"
    path = "config.draft/"

    preambles = fetch_github_directory(owner, repo, path + "preambles/")
    headers = fetch_github_directory(owner, repo, path + "headers/")
    exercises = fetch_github_directory(owner, repo, path + "exercises")

    def resolve_templates(dict, type, creator, path: Path):
        for name, contents in dict.items():
            match = False
            if not path.is_dir():
                path.mkdir(parents=True, exist_ok=True)
            for file in path.iterdir():
                if file.name == name:
                    match = True

            if not match:
                creator(name, contents)
                templates_are_uptodate = False
                rprint("[blue]==>[/blue] [bold white]Created '%s' :sparkles:" % name)
            else:
                if verbose:
                    question = Confirm(
                        "confirmation",
                        message="A %s called '%s' already exists in your templates. Do you want to overwrite it with the version from GitHub?"
                        % (type, name),
                        default=False,
                    )
                    answer = prompt(question).get("confirmation", False)
                    if answer:
                        creator(name, contents)
                        templates_are_uptodate = False
                        rprint(
                            "[blue]==>[/blue] [bold white]Overwritten '%s' :sparkles:"
                            % name
                        )

    # Preambles
    if preambles is not None:
        resolve_templates(
            preambles,
            "preamble",
            templates_manager.new_preamble,
            templates_manager.preambles_path,
        )

    # Headers
    if headers is not None:
        resolve_templates(
            headers,
            "header",
            templates_manager.new_header,
            templates_manager.headers_path,
        )

    # Exercises
    if exercises is not None:
        resolve_templates(
            exercises,
            "exercise",
            templates_manager.new_exercise,
            templates_manager.exercises_path,
        )

    if templates_are_uptodate:
        rprint("No new templates on GitHub.")
