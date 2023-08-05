"""Module for updating versions.

This module provides a class for updating versions in a list of files.
"""

import re
from dataclasses import dataclass
from typing import Any


@dataclass
class VersionUpdater:
    """Class for updating versions in a list of files.

    Attributes:
        files_path (list): List of paths of files to update.
        version_regex_pattern (str, optional): Regular expression
            pattern for the version, defaults to '\d+\.\d+\.\d+'.

    """

    files_path: list
    version_regex_pattern: str = '\d+\.\d+\.\d+'
    

    def open_file(self, path: str) -> Any:
        """Open a file and return its contents.

        Args:
            path (str): Path of the file to open.

        Returns:
            Any: Contents of the file.

        """
        with open(path, 'r') as f:
            contents = f.read()

        return contents


    def save_file(self, path: str, contents: Any) -> None:
        """Save contents to a file.

        Args:
            path (str): Path of the file to save.
            contents (Any): Contents to save in the file.

        """
        with open(path, 'w') as f:
            f.write(contents)


    def get_last_version(self, contents: Any) -> str:
        """Return the last version in the contents of a file.

        Args:
            contents (Any): Contents of the file.

        Returns:
            str: Last version in the contents of the file.

        """
        version_pattern = re.compile(self.version_regex_pattern)
        last_version = re.search(version_pattern, contents).group()

        return last_version


    def update(self, last_version, next_version) -> None:
        """Update versions in a list of files.

        Args:
            last_version (str): Version to replace.
            next_version (str): Version to replace with.

        """
        for path in self.files_path:
            contents = self.open_file(path=path)
            contents = contents.replace(last_version, next_version)
            self.save_file(path=path, contents=contents)
