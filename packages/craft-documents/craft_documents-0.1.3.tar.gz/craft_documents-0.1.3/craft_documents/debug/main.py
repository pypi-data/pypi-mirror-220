import typer
from rich import print

from craft_documents.configuration.Configuration import Configuration
from craft_documents.debug.Debugger import Debugger

app = typer.Typer()


@app.callback(invoke_without_command=True)
def callback(ctx: typer.Context):
    Debugger(Configuration()).run()
