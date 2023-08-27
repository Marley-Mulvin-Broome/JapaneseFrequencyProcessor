from dataclasses import dataclass
from typing import Iterable

from .word import Word


@dataclass
class WordSlot:
    words: list[Word]

    def __contains__(self, item):
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

    def to_dict(self, combine: bool = False) -> dict:
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
        for old_word in self.words:
            if old_word.surface == word.surface:
                old_word.frequency += 1
                return

        self.words.append(word)

    @property
    def frequency(self) -> int:
        return sum(word.frequency for word in self.words)


def get_unique_wordslots(word_slots: Iterable[WordSlot]) -> list[WordSlot]:
    return [slot for slot in word_slots if slot.frequency == 1]
