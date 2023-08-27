"""
.. include:: ../../documentation/word_slot.md
"""

from dataclasses import dataclass
from typing import Iterable

from .word import Word


@dataclass
class WordSlot:
    words: list[Word]

    def __contains__(self, item: [Word | str]):
        """
        Checks if the word slot contains the item.

        Compares the item to the words directly if the item is of type Word.
        Compares the item to the word surfaces if the item is of type str.
        Parameters
        ----------
        item : Word | str
            The item to check.

        Returns
        -------
        bool
            Whether the word slot contains the item or not.
        """
        if isinstance(item, Word):
            return item in self.words

        if isinstance(item, str):
            return item in [word.surface for word in self.words]

    def __len__(self):
        """
        Returns the frequency of the word slot.
        Returns
        -------
        int
            The frequency of the word slot.
        """
        return self.frequency

    @property
    def frequency(self) -> int:
        """
        The frequency of the word slot.

        This is the sum of the frequencies of all words in the word slot.
        Returns
        -------
        int
            The frequency of the word slot.
        """
        return sum(word.frequency for word in self.words)

    def to_dict(self, combine: bool = False) -> dict:
        """
        Converts the word slot to a dictionary.
        Parameters
        ----------
        combine : bool
            Whether to combine the words in the word slot or not. If True, a single word is returned with the combined
            frequency of all words in the word slot. The surface becomes the representation of the first word in the
            word slot. If False, a list of words is returned.

        Returns
        -------
        dict
            The dictionary representation of the word slot.
        """
        if not self.words:
            return {}

        if combine:
            word = Word(
                representation=self.words[0].representation,
                surface=self.words[0].representation,
                types=self.words[0].types,
                frequency=self.frequency,
            )

            for word in self.words[1:]:
                word.frequency += word.frequency

            return word.to_dict()

        words_array = []

        [words_array.append(word.to_dict()) for word in self.words]

        return {"words": words_array}

    def add_word(self, word: Word) -> None:
        """
        Adds a word to the word slot.
        Parameters
        ----------
        word : Word
            The word to add to the word slot.
        """
        for old_word in self.words:
            if old_word.surface == word.surface:
                old_word.frequency += 1
                return

        self.words.append(word)


def get_unique_wordslots(word_slots: Iterable[WordSlot]) -> list[WordSlot]:
    """
    Gets the unique word slots from a list of word slots.
    Parameters
    ----------
    word_slots : Iterable[WordSlot]
        The word slots to get the unique word slots from.

    Returns
    -------
    list[WordSlot]
        The unique word slots.
    """
    return [slot for slot in word_slots if slot.frequency == 1]
