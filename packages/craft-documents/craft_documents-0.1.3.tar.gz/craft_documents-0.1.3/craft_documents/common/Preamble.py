from pathlib import Path

from craft_documents.common.TexTemplate import TexTemplate
from craft_documents.configuration.Configuration import Configuration


class Preamble(TexTemplate):
    """
    A class representing the preamble.

    This class customizes the loading function
    in order to strip the document environment
    from its contents.
    """

    def __init__(self, path: Path, configuration: Configuration):
        super().__init__(path, configuration)
        self.remove_document_body()

    def load(self):
        """
        Remove the document environment.
        """
        with self.path.open("r") as file:
            self._contents = file.read()
            self._disk_contents = self.contents
