import typer
from rich import print
from typing_extensions import Annotated

from craft_documents.configuration.Configuration import Configuration
from craft_documents.configuration.VerboseValidator import VerboseValidator
from craft_documents.new.Subcommands import Subcommands
from craft_documents.templates.TemplateManager import TemplateManager

app = typer.Typer()

configuration = Configuration()

subcommands = Subcommands(
    configuration,
    TemplateManager(configuration),
)

subcommands.add_subcommands(app)


@app.callback(invoke_without_command=True)
def callback(
    ctx: typer.Context,
    verbose: Annotated[
        bool, typer.Option(help="Output additional information.")
    ] = False,
):
    configuration[VerboseValidator().key] = verbose
    if ctx.invoked_subcommand is None:
        if configuration.header is not None:
            print("#TODO: Compiling document for `%s`." % configuration.header.name)
        else:
            ctx.get_help()
