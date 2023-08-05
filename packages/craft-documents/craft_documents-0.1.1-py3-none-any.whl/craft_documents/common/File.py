import re
from abc import ABC
from pathlib import Path

from craft_documents.common.DiskRepresentable import DiskRepresentable


class File(ABC, DiskRepresentable):
    """
    Abstract class representing a file on the disk.

    Subclasses:
    - Template (ABC)

    Subclasses should remember to call `super().__init__()`
    if they implement their own initializer.
    """

    _contents: str
    _disk_contents: str

    @property
    def contents(self) -> str:
        return self._contents

    @property
    def disk_contents(self) -> str:
        """Should always return the contents on the disk."""
        return self._disk_contents

    @property
    def extension(self) -> str:
        return self.path.suffix

    @property
    def parent(self) -> Path:
        return self.path.parent

    def __init__(self, path: Path):
        self._path = path.resolve()
        self.load()

    def load(self):
        with self.path.open("r") as file:
            self._contents = file.read()
            self._disk_contents = self.contents

    def remove_lines(self, prefix: str):
        """
        Removes all lines starting with the given
        prefix from the contents of the file.

        General case:
        ```text
        Paragraph before... ──┐
                              |
        % This is a comment ──┤
                              │
                              │ this will be deleted
                              │
        Paragraph after...  ──┤
        ```

        Special case:
        ```text
        Paragraph one ...   ──┐
        % this is the end   ──┤
                              │ this will be deleted
                              │ and replaced with a
                              │ newline
        Paragraph after...  ──┤
        ```
        """
        # Handle `test_single_line_and_contents_condensed_leading` and
        # `test_multiple_lines_and_contents_condensed_leading` first
        pattern = re.compile(
            "(?<=[^\n]\n)(?:^%s.*?\n?)+(?:^\n)+(?=[^\n])" % prefix, re.MULTILINE
        )
        self._contents = re.sub(pattern, "\n", self.contents)

        # General cases
        pattern = re.compile("^%s.*\n*" % prefix, re.MULTILINE)
        self._contents = re.sub(pattern, "", self.contents)

    def remove_blocks(self, prefix: str, suffix: str):
        r"""
        Removes all blocks enclosed by the given
        prefix and suffix from the contents of the file.

        General case:
        ```text
        Paragraph before... ──┐
                              |
        \iffalse            ──┤
        This is a comment     │
        \fi                   │ this will be deleted
                              │
                              │
        Paragraph after...  ──┤
        ```

        Special case:
        ```text
        Paragraph one ...   ──┐
        \iffalse            ──┤
        This is a comment     │ this will be deleted
        \fi                   │ and replaced with a
                              │ newline
        Paragraph after...  ──┤
        ```
        """
        # Special case
        pattern = re.compile(
            "(?s)(?<=[^\n]\n)(%s(?:.*?)%s\n)+^\n+?(?=[^\n])" % (prefix, suffix),
            re.MULTILINE,
        )
        self._contents = re.sub(pattern, "\n", self.contents)

        # General case
        pattern = re.compile("(?s)^%s(.*?)%s\n*" % (prefix, suffix), re.MULTILINE)
        self._contents = re.sub(pattern, "", self.contents)
