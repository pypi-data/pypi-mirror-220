from rich import print
from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from rich.pretty import Pretty

from craft_documents.configuration.Configuration import Configuration


class Debugger:
    """
    Class that manages outputting of common debug information.
    """

    @property
    def configuration(self) -> Configuration:
        return self._configuration

    def __init__(self, configuration: Configuration):
        self._configuration = configuration

    def run(self):
        print(Panel(Pretty(self.configuration), title="[bold red]Configuration"))
