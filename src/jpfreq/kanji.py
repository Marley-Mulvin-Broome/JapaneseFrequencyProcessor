from unicodedata import name as u_name
from dataclasses import dataclass

KANJI_UNICODE_NAME = "CJK UNIFIED IDEOGRAPH"


@dataclass
class Kanji:
    representation: str
    frequency: int


def is_character_kanji(input_character: str):
    if len(input_character) != 1:
        raise TypeError(
            f"is_character_kanji: Expected str of length 1, got length of {len(input_character)} instead"
        )

    return KANJI_UNICODE_NAME in u_name(input_character)


def all_kanji_in_string(input_string: str) -> list[Kanji]:
    kanji: list[Kanji] = []

    for character in input_string:
        if is_character_kanji(character):
            kanji.append(Kanji(character, 1))

    return kanji
