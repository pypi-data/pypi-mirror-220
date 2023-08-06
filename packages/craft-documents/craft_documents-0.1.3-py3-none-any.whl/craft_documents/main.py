import typer

from craft_documents.debug.main import app as debug
from craft_documents.new.main import app as new
from craft_documents.templates.main import app as templates

app = typer.Typer(no_args_is_help=True)


app.add_typer(new, name="new", help="Create a new document.")
app.add_typer(
    debug,
    name="debug",
    help="Output the configuration in with which the tool would run.",
)
app.add_typer(templates, name="templates", help="Manage the templates directory.")
