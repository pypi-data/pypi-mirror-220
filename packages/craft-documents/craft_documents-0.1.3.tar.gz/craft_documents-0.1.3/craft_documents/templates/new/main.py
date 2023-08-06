from pathlib import Path

import typer
from rich import print
from typing_extensions import Annotated

from craft_documents.templates.TemplateManager import TemplateManager
from craft_documents.configuration.Configuration import Configuration

app = typer.Typer(no_args_is_help=True)

configuration = Configuration()
template_manager = TemplateManager(configuration)

import os
import subprocess

DEFAULT_EDITOR = "/usr/bin/vim"  # backup, if not defined in environment vars


@app.command(name="preamble", help="Create a new preamble.")
def create_template_preamble(
    name: Annotated[str, typer.Argument(help="Specify the name of the new preamble.")]
):
    path = template_manager.preambles_path / (name.removesuffix(".tex") + ".tex")

    # Early out if a header with this name already exists.
    if path.is_file():
        print(":police_car_light: [red]A preamble '%s' already exists." % path.stem)
        exit(1)

    contents = r"""
\documentclass{scrreport}

% Keep this package import
\usepackage{subfiles} 

% Add your declarations

% Test the look of your preamble. This won't be included in the compiled document
\begin{document}
Hello, world!
\end{document}
"""
    path.write_text(contents)

    # Open in default editor
    editor = os.environ.get("EDITOR", DEFAULT_EDITOR)
    subprocess.call([editor, path])


@app.command(name="header", help="Create a new header.")
def create_template_header(
    name: Annotated[str, typer.Argument(help="Specify the name of the new header.")]
):
    path = template_manager.headers_path / (name.removesuffix(".tex") + ".tex")

    # Early out if a header with this name already exists.
    if path.is_file():
        print(":police_car_light: [red]A header '%s' already exists." % path.stem)
        exit(1)

    contents = r"""
% Configure to use one of your preambles
\documentclass[../preambles/default.tex]{subfiles}

% Configure what's printed in the document header
\usepackage{scrlayer-scrpage}

\ohead{}  % outer
\chead{}  % center
\ihead{}  % inner

% Add your declarations

% Add content to the document-body
\begin{document}

% This placeholder will be replaced with exercises
<<craft-exercises>> 

\end{document}
"""
    path.write_text(contents)

    editor = os.environ.get("EDITOR", DEFAULT_EDITOR)
    subprocess.call([editor, path])


@app.command(name="exercise", help="Create a new exercise.")
def create_template_exercise(
    name: Annotated[str, typer.Argument(help="Specify the name of the new exercise.")]
):
    if Path(name).suffix != ".tex" and Path(name).suffix != "":
        print("You can only create tex-templates at the moment.")
        exit(1)

    path = template_manager.exercises_path / (name.removesuffix(".tex") + ".tex")

    # Early out if a header with this name already exists.
    if path.is_file():
        print(":police_car_light: [red]An exercise '%s' already exists." % path.stem)
        exit(1)

    contents = r"""
% Configure to use one of your preambles
\documentclass[../preambles/default.tex]{subfiles}

\iffalse
# Declare any supplemental files here (with their extension)
# supplements:

# Declare any placeholder only for this exercise in here
# unique-placeholders:
\fi

% Add any additional declarations

% Add what your exercise should look like. Use <<placeholders>> for 
% any data that should be filled in at compile time.
\begin{document}

\end{document}
"""
    path.write_text(contents)

    editor = os.environ.get("EDITOR", DEFAULT_EDITOR)
    subprocess.call([editor, path])
