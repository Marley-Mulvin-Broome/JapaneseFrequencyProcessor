"""
.. include:: ../../documentation/jp_frequency_list.md
"""

from fugashi import Tagger
from typing import Callable
from os.path import isfile as file_exists

from .word_slot import WordSlot, get_unique_wordslots
from .text_info import TextInfo
from .kanji import all_kanji_in_string, Kanji
from .util import percent_of
from .word import Word, WordType

EXCLUDED_WORD_TYPES: list[WordType] = [
    WordType.PARTICLE,
    WordType.AUXILIARY_VERB,
    WordType.SUPPLEMENTARY_SYMBOL,
    WordType.BLANK_SPACE,
    WordType.NUMERAL,
]


def word_validator_exclude_by_type(input_word: Word, excluded_word_types=None) -> bool:
    """
    Validates a word by excluding it if it is of a certain type lists in `excluded_word_types`.

    Parameters
    ----------
    input_word : UnidicNode
        The word to validate.
    excluded_word_types : list[str]
        A list of word types to exclude. Defaults to `EXCLUDED_WORD_TYPES`.

    Returns
    -------
    bool
        Whether the word is valid or not.
    """
    if excluded_word_types is None:
        excluded_word_types = EXCLUDED_WORD_TYPES
    for word_type in input_word.types:
        if word_type in excluded_word_types:
            return False

    return True


class JapaneseFrequencyList:
    """
    A class for storing the frequency of words in a Japanese text.
    """

    _unique_words: dict[str, WordSlot]
    _unique_kanji: dict[str, Kanji]
    _word_count: int
    _tagger: Tagger
    _word_validator: Callable[[Word], bool]

    def __init__(
        self,
        word_validator: Callable[[Word], bool] = word_validator_exclude_by_type,
        text_to_analyse: list = None,
        tagger_instance=None,
    ):
        self._unique_words = {}
        self._unique_kanji = {}
        self._word_count = 0

        self._word_validator = word_validator

        self._tagger = tagger_instance
        if not self._tagger:
            self._tagger = Tagger("-Owakati")
        elif not isinstance(self._tagger, Tagger):
            raise TypeError(
                f"JapaneseFrequencyList: tagger_instance must be of type fugashi.Tagger, not {type(self._tagger)}"
            )

        if text_to_analyse is not None:
            self.process_texts(text_to_analyse)

    def __len__(self) -> int:
        """
        The number of unique words in the frequency list.
        Returns
        -------
        int
            The number of unique words in the frequency list.
        """
        return len(self.wordslots)

    def __repr__(self) -> str:  # pragma: no cover
        """
        A string representation of the frequency list in the form: 'JapaneseFrequencyList(text_info=TextInfo(...))'
        Returns
        -------

        """
        text_info = self.generate_text_info()
        return f"JapaneseFrequencyList(\ntext_info={text_info!r}\n)"

    def __contains__(self, word: str) -> bool:
        """
        Whether the representation of a word is in the frequency list.
        Parameters
        ----------
        word : str
            The word to check for.

        Returns
        -------
        bool
            Whether the word is in the frequency list.
        """
        return word in self._unique_words.keys()

    def __getitem__(self, word: str) -> WordSlot:
        """
        Returns the WordSlot for the specified word.
        This will search using the word's representation, not its surface.
        This means that if you pass "これ", it will fail, as the representation is "此れ".
        Please see the function `get_representation` in this class to get the representation of a word.
        Parameters
        ----------
        word

        Returns
        -------

        """
        if word not in self._unique_words.keys():
            raise KeyError(f"Word '{word}' not found in frequency list")

        return self._unique_words[word]

    @property
    def wordslots(self) -> list[WordSlot]:
        """
        Returns a list of all the wordslots.
        Returns
        -------
        list[WordSlot]
            A list of all the wordslots.
        """
        return list(self._unique_words.values())

    @property
    def word_count(self) -> int:
        """
        Returns the number of words.
        Returns
        -------
        int
            The number of words.
        """
        return self._word_count

    @property
    def unique_words(self) -> int:
        """
        Returns the number of unique words.
        Returns
        -------
        int
            The number of unique words.
        """
        return len(self.wordslots)

    @property
    def unique_words_used_once(self) -> int:
        """
        Returns the number of unique words used once.
        Returns
        -------
        int
            The number of unique words used once.
        """
        return len(get_unique_wordslots(self.wordslots))

    @property
    def unique_words_all(self) -> tuple[int, int, float]:
        """
        Returns the number of unique words, the number of unique words used once, and the percentage of unique words used once.
        Returns
        -------
        tuple[int, int, float]
            unique_words, unique_words_used_once, unique_words_used_once_percentage
        """
        unique_words: int = self.unique_words
        unique_words_used_once: int = self.unique_words_used_once

        unique_word_percentage: float = percent_of(unique_words_used_once, unique_words)

        return unique_words, unique_words_used_once, unique_word_percentage

    @property
    def unique_kanji(self) -> int:
        """
        Returns the number of unique kanji.
        Returns
        -------
        int
            The number of unique kanji.
        """
        return len(self._unique_kanji)

    @property
    def unique_kanji_used_once(self) -> int:
        """
        Returns the number of unique kanji used once.
        Returns
        -------
        int
            The number of unique kanji used once.
        """
        return len(
            [kanji for kanji in self._unique_kanji.values() if kanji.frequency == 1]
        )

    @property
    def unique_kanji_all(self) -> tuple[int, int, float]:
        """
        Returns the number of unique kanji, the number of unique kanji used once, and the percentage of unique kanji used once.
        Returns
        -------
        tuple[int, int, float]
            unique_kanji, unique_kanji_used_once, unique_kanji_used_once_percentage
        """
        unique_kanji: int = self.unique_kanji
        unique_kanji_used_once: int = self.unique_kanji_used_once

        unique_kanji_percentage: float = percent_of(
            unique_kanji_used_once, unique_kanji
        )

        return unique_kanji, unique_kanji_used_once, unique_kanji_percentage

    def clear(self) -> None:
        """
        Clears the frequency list of all words and kanji, reverting it to its initial state.
        """
        self._word_count = 0

        self._unique_words.clear()
        self._unique_kanji.clear()

    def get_most_frequent(self, limit: int = 100) -> list[WordSlot]:
        """
        Returns a list of the most frequent words in the text with the specified limit.
        If limit is -1, then all words are returned.
        Parameters
        ----------
        limit : int
            The number of words to return.
        Returns
        -------
        list[WordSlot]
            A list of the most frequent words in the text with the specified limit, sorted by frequency.
        """
        item_array: list[WordSlot] = sorted(
            self.wordslots, key=lambda x: x.frequency, reverse=True
        )

        if limit == -1 or limit > len(item_array):
            return item_array

        return item_array[:limit]

    def generate_text_info(self) -> TextInfo:
        """
        Generates a TextInfo object from the frequency list.
        Returns
        -------
        TextInfo
            A TextInfo object containing information about the text.
        """
        (
            unique_words,
            unique_words_used_once,
            unique_word_percentage,
        ) = self.unique_words_all
        (
            unique_kanji,
            unique_kanji_used_once,
            unique_kanji_percentage,
        ) = self.unique_kanji_all

        return TextInfo(
            self.word_count,
            unique_words,
            unique_words_used_once,
            unique_word_percentage,
            unique_kanji,
            unique_kanji_used_once,
            unique_kanji_percentage,
        )

    def add_kanji(self, kanji: Kanji) -> None:
        """
        Adds a kanji to the frequency list.
        Parameters
        ----------
        kanji : Kanji
            The kanji to add.
        """
        if kanji.representation in self._unique_kanji:
            self._unique_kanji[kanji.representation].frequency += 1
            return

        self._unique_kanji[kanji.representation] = kanji

    def add_word(self, word: Word) -> None:
        """
        Adds a word to the frequency list.

        If the word is already in the list, then the frequency is increased by 1.
        Otherwise, the word is added to the list with a frequency of 1.

        Note: This method assumes the word is valid.

        Parameters
        ----------
        word : Word
            The word to add.
        """
        self._word_count += 1

        if word.representation in self._unique_words.keys():
            self._unique_words[word.representation].add_word(word)
            return

        # if there is no representation of this word then we must add one
        self._unique_words[word.representation] = WordSlot([word])

    def get_representation(self, word: str) -> str:
        """
        Returns the representation of a word.
        This is the word without any inflections.
        For example, the representation of "これ" is "此れ".
        The representation of "行った" is "行く".
        Parameters
        ----------
        word : str
            The word to get the representation of.
        Returns
        -------
        str
            The representation of the word.
        """
        processed_word = self.parse_line(word)[0]

        if len(processed_word) < 1:
            raise ValueError(f"Word '{word}' is not a valid word")

        return processed_word[0].representation

    def parse_line(self, line: str) -> tuple[list[Word], list[Kanji]]:
        """
        Parses a line of text into a list of Words and a list of Kanji.
        Backbone of all parsing.

        Parameters
        ----------
        line : str
            The line to parse.

        Returns
        -------
        tuple[list[Word], list[Kanji]]
            A tuple containing the list of Words and the list of Kanji.
        """
        words = self._tagger(line)

        return [Word.from_node(word) for word in words], all_kanji_in_string(line)

    def process_line(self, line_to_process: str) -> None:
        """
        Parses a line, adding the valid words and all kanji to the frequency list.
        All other processing functions boil down to this.

        Parameters
        ----------
        line_to_process : str
            The line to process.
        """
        line_to_process = line_to_process.replace("\n", "")
        words, kanji = self.parse_line(line_to_process)

        [self.add_kanji(kanji) for kanji in kanji]
        [self.add_word(word) for word in words if self._word_validator(word)]

    def process_text(self, text_to_process: str) -> None:
        """
        Parses a string split by the newline character, adding the valid words to the frequency list.

        Parameters
        ----------
        text_to_process : str
            Text potentially containing multiple lines.
        """
        [self.process_line(line) for line in text_to_process.split("\n")]

    def process_texts(self, texts_to_process: list) -> None:
        """
        Parses a list of texts, adding the valid words to the frequency list.

        Parameters
        ----------
        texts_to_process : list
            A list of texts to process.
        """
        [self.process_text(text) for text in texts_to_process]

    def process_file(self, file_path: str) -> None:
        """
        Parses a file, adding the valid words to the frequency list.
        Parameters
        ----------
        file_path : str
            The path to the file to process.
        """
        if not file_exists(file_path):
            raise FileExistsError(
                f"process_file: File path passed doesn't exist ({file_path})"
            )

        with open(file_path, "r", encoding="utf-8") as fs:
            [self.process_line(line) for line in fs]
