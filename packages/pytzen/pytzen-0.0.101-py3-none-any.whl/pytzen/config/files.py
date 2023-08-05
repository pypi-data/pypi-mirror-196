"""Module for parsing configuration files in JSON, YAML, or TOML format.

This module provides a `ConfigFile` class that can be used to parse
configuration files in JSON, YAML, or TOML format and return a
dictionary representation of the file's content.
"""

from dataclasses import dataclass
import json
import yaml
import toml


@dataclass
class ConfigFile:
    """Parses a configuration file in JSON, YAML, or TOML format and
    returns a dictionary.

    Attributes:
        file_path (str): Path to the configuration file.

    """
    file_path: str

    def to_dict(self):
        """Parses the configuration file and returns a dictionary.

        Returns:
            dict: A dictionary representation of the configuration file.

        Raises:
            ValueError: If the file format is not supported (not JSON,
                YAML, or TOML).

        """
        if self.file_path.endswith('.json'):
            with open(self.file_path) as f:
                return json.load(f)
        elif (self.file_path.endswith('.yaml')
              or self.file_path.endswith('.yml')):
            with open(self.file_path) as f:
                return yaml.safe_load(f)
        elif self.file_path.endswith('.toml'):
            with open(self.file_path) as f:
                return toml.load(f)
        else:
            raise ValueError("Unsupported file format")
