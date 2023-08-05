import typer
from rich import print

from tests.common.test_common_Configuration import Configuration
from craft_documents.debug.Debugger import Debugger

app = typer.Typer()


@app.callback(invoke_without_command=True)
def callback(ctx: typer.Context):
    Debugger(Configuration()).run()
