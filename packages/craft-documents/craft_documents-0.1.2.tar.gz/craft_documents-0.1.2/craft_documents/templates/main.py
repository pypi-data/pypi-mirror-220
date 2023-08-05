import typer
from rich import print as rprint
from typing_extensions import Annotated

from craft_documents.configuration.Configuration import Configuration
from craft_documents.templates.fetch import fetch_implementation
from craft_documents.templates.list import list_implementation
from craft_documents.templates.new.main import app as new
from craft_documents.templates.TemplateManager import TemplateManager

app = typer.Typer(no_args_is_help=True)

app.add_typer(new, name="new", help="Create a new template.")

configuration = Configuration()
templates_manager = TemplateManager(configuration)


@app.command(name="path", help="Reveal the location of the templates folder.")
def path():
    print(templates_manager.folder.path)


@app.command(name="open", help="Open the directory of the templates.")
def open():
    templates_manager.folder.open()


@app.command(name="fetch", help="Fetch templates from GitHub")
def fetch(
    verbose: Annotated[
        bool, typer.Option(help="Don't overwrite any local templates.")
    ] = False
):
    fetch_implementation(verbose, templates_manager, app)


@app.command(name="list", help="List the available templates.")
def list_function():
    list_implementation(templates_manager)
