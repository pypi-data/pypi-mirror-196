"""Module for serializing numbers.

This module provides a class for serializing numbers and generating
series of serialized numbers.
"""

from dataclasses import dataclass


@dataclass
class NumberSerializer:
    """Class for serializing numbers.

    Attributes:
        characters (int): Number of characters to fill the serialized
            number.
        start_from (int, optional): Number to start serializing from,
            defaults to 0.
        prefix (str, optional): Prefix for the serialized number,
            defaults to ''.
        suffix (str, optional): Suffix for the serialized number,
            defaults to ''.
        step (int, optional): Step to increase the serialized number,
            defaults to 1.
        series_length (int, optional): Length of the series to generate,
            defaults to None.

    """

    characters: int
    start_from: int = 0
    prefix: str = ''
    suffix: str = ''
    step: int = 1
    series_length: int = None
    

    def serialize(self) -> str:
        """Return the next serialized number in the series.

        Returns:
            str: Next serialized number.

        """
        if self.characters:
            number = self.start_from + self.step
            filled_number = str(number).zfill(self.characters)
            serialized_number = f'{self.prefix}{filled_number}{self.suffix}'
            self.start_from = number

            return serialized_number


    def series_generator(self):
        """Generator for generating a series of serialized numbers.

        Yields:
            str: Next serialized number in the series.

        """
        n = 0
        while n != self.series_length:
            n += 1
            yield self.serialize()