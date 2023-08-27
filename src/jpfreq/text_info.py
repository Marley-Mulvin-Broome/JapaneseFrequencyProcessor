"""
.. include:: ../../documentation/text_info.md
"""

from dataclasses import dataclass


@dataclass(eq=False)
class TextInfo:
    word_count: int = 0
    unique_words: int = 0
    unique_words_used_once: int = 0
    unique_words_used_once_percentage: float = 0
    unique_kanji: int = 0
    unique_kanji_used_once: int = 0
    unique_kanji_used_once_percentage: float = 0

    def __eq__(self, __value: object) -> bool:
        """
        Equals operator for TextInfo class.

        Needs to be implemented as sometimes in testing comparison doesn't work as
        intended.
        """
        if not isinstance(__value, TextInfo):
            raise TypeError

        return (
            self.word_count == __value.word_count
            and self.unique_words == __value.unique_words
            and self.unique_words_used_once == __value.unique_words_used_once
            and self.unique_words_used_once_percentage
            == __value.unique_words_used_once_percentage
            and self.unique_kanji == __value.unique_kanji
            and self.unique_kanji_used_once == __value.unique_kanji_used_once
            and self.unique_kanji_used_once_percentage
            == __value.unique_kanji_used_once_percentage
        )

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the TextInfo object.
        Returns
        -------
        dict
            A dictionary representation of the TextInfo object.
        """
        return {
            "word_count": self.word_count,
            "unique_words": self.unique_words,
            "unique_words_used_once": self.unique_words_used_once,
            "unique_words_used_once_percentage": self.unique_words_used_once_percentage,
            "unique_kanji": self.unique_kanji,
            "unique_kanji_used_once": self.unique_kanji_used_once,
            "unique_kanji_used_once_percentage": self.unique_kanji_used_once_percentage,
        }
