"""
.. include:: ../../documentation/kanji.md
"""

from unicodedata import name as u_name
from dataclasses import dataclass

KANJI_UNICODE_NAME = "CJK UNIFIED IDEOGRAPH"
"""The unicode name of a kanji character. 
Used with the `u_name` function to determine if a code point is a kanji character."""


@dataclass
class Kanji:
    """
    A dataclass representing a kanji character.
    """

    representation: str
    """The text representation of the kanji character."""
    frequency: int
    """The frequency of the kanji character."""


def is_character_kanji(input_character: str) -> bool:
    """
    Checks if the input character is a kanji character.
    Parameters
    ----------
    input_character : str
        The character to check.

    Returns
    -------
    bool
        Whether the character is a kanji character or not.
    """
    if len(input_character) != 1:
        raise TypeError(
            f"is_character_kanji: Expected str of length 1, got length of {len(input_character)} instead"
        )

    return KANJI_UNICODE_NAME in u_name(input_character)


def all_kanji_in_string(input_string: str) -> list[Kanji]:
    """
    Returns all kanji characters in the input string.
    Parameters
    ----------
    input_string : str
        The string to check.

    Returns
    -------
    list[Kanji]
        A list of all kanji characters in the input string.
    """
    kanji: list[Kanji] = []

    for character in input_string:
        if is_character_kanji(character):
            kanji.append(Kanji(character, 1))

    return kanji
