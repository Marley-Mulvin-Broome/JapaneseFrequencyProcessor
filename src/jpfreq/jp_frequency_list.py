from fugashi import Tagger, UnidicNode
from typing import Callable
from os.path import isfile as file_exists

from .word_slot import WordSlot, get_unique_wordslots
from .text_info import TextInfo
from .frequency_exporter import FrequencyExporter
from .word_types import WordType
from .kanji import all_kanji_in_string
from .util import percent_of

EXCLUDED_WORD_TYPES: list[str] = [
    WordType.PARTICLE.value,
    WordType.AUXILIARY_VERB.value,
    WordType.SUPPLEMENTARY_SYMBOL.value,
    WordType.BLANK_SPACE.value,
    WordType.NUMERAL.value,
]


def pos_same_at_index(pos_1: str, pos_2: str, index: int) -> bool:
    split_pos_1: list[str] = pos_1.split(",")
    split_pos_2: list[str] = pos_2.split(",")

    if len(split_pos_1) <= index or len(split_pos_2) <= index:
        return False

    return split_pos_1[index] == split_pos_2[index]


def parse_pos_node(pos: str) -> list[str]:
    split_pos: list[str] = pos.split(",")
    new_pos: list[str] = []

    for pos_value in split_pos:
        if pos_value == "*":
            break

        new_pos.append(pos_value)

    return new_pos


def word_validator_exclude_by_type(input_word: UnidicNode, excluded_word_types: list[str] = EXCLUDED_WORD_TYPES) -> bool:
    """
    Validates a word by excluding it if it is of a certain type lists in `excluded_word_types`.

    Parameters
    ----------
    input_word : UnidicNode
        The word to validate.
    excluded_word_types : list[str]
        A list of word types to exclude.
    
    Returns
    -------
    bool
        Whether the word is valid or not.
    """
    word_classes = parse_pos_node(input_word.pos)

    excluded_word_types = [
        word_type 
        for word_type in excluded_word_types 
        if word_type in word_classes
    ]

    return excluded_word_types == []


def word_rep(word: UnidicNode):
    """
    Gets the string representation of a word.
    This is the lemma of the word.

    Parameters
    ----------
    word : UnidicNode
        The word to get the representation of.

    Returns
    -------
    str
        The string representation of the word.
    """
    return f"{word.feature.lemma}"


class JapaneseFrequencyList:
    _unique_words: dict[str, list[WordSlot]]
    _unique_kanji: dict[str, WordSlot]
    _word_count: int
    _tagger: Tagger
    _exporter: FrequencyExporter
    _word_validator: Callable[[UnidicNode], bool]

    def __init__(
        self,
        word_validator: Callable[[UnidicNode], bool] = word_validator_exclude_by_type,
        text_to_analyse: list = None,
        tagger_instance=None,
    ):
        self._unique_words = {}
        self._unique_kanji = {}
        self._word_count = 0
        self._exporter = FrequencyExporter()

        self._word_validator = word_validator

        self._tagger = tagger_instance
        if not self._tagger:
            self._tagger = Tagger("-Owakati")

        if text_to_analyse is not None:
            self.process_texts(text_to_analyse)

    def __len__(self) -> int:
        return len(self.wordslots)

    def __repr__(self) -> str:
        text_info = self.generate_text_info()
        return f"JapaneseFrequencyList(\ntext_info={text_info!r}\n)"
    
    def __contains__(self, word: str) -> bool:
        return word in self._unique_words.keys()
    
    def __getitem__(self, word: str) -> list[WordSlot]:
        return self._unique_words[word]

    def _update_kanji(self, word: UnidicNode) -> None:
        for kanji in all_kanji_in_string(str(word.surface)):
            if kanji not in self._unique_kanji:
                self._unique_kanji[kanji] = WordSlot(word, 1)
                continue

            self._unique_kanji[kanji].frequency += 1

    def _append_representation(self, word: UnidicNode) -> None:
        """
        Appends the word to the list of unique words if it doesn't already exist.
        Otherwise, it increments the frequency of the word.

        This will add frequency to the specific conjugation of the word.
        
        e.g.
        adding ある into [(ある, 1)] will result in [(ある, 2)]
        but adding あった into [(ある, 1)] will result in [(ある, 1), (あった, 1)]
        """
        word_list = self._unique_words[word.feature.lemma]

        for word_slot in word_list:
            if pos_same_at_index(word_slot.word.pos, word.pos, 0):
                word_slot.frequency += 1
                return

        # otherwise, we need to add another word to the list
        word_list.append(WordSlot(word, 1))

    def _loop_wordslots(self, loop_function: Callable[[WordSlot], None] = None) -> None:
        for word_list in self._unique_words.values():
            for word_slot in word_list:
                if loop_function:
                    loop_function(word_slot)

    def clear(self) -> None:
        """
        Clears the frequency list of all words and kanji.
        """
        self._word_count = 0

        self._unique_words.clear()
        self._unique_kanji.clear()

    def get_most_frequent(self, limit: int = 100) -> list[WordSlot]:
        """
        Returns a list of the most frequent words in the text with the specified limit.
        If limit is -1, then all words are returned.
        """
        item_array: list[WordSlot] = sorted(self.wordslots, key=lambda x: x.frequency, reverse=True)

        if limit == -1 or limit > len(item_array):
            return item_array

        return item_array[:limit]

    @property
    def wordslots(self) -> list[WordSlot]:
        slots: list[WordSlot] = []

        def add_slot(s):
            slots.append(s)

        self._loop_wordslots(add_slot)

        return slots

    @property
    def word_count(self) -> int:
        return self._word_count

    @property
    def unique_words(self) -> int:
        return len(self.wordslots)

    @property
    def unique_words_used_once(self) -> int:
        return len(get_unique_wordslots(self.wordslots))

    @property
    def unique_words_all(self) -> tuple[int, int, float]:
        unique_words: int = self.unique_words
        unique_words_used_once: int = self.unique_words_used_once

        unique_word_percentage: float = percent_of(unique_words_used_once, unique_words)

        return unique_words, unique_words_used_once, unique_word_percentage

    @property
    def unique_kanji(self) -> int:
        return len(self._unique_kanji)

    @property
    def unique_kanji_used_once(self) -> int:
        return len(get_unique_wordslots(self._unique_kanji.values()))

    @property
    def unique_kanji_all(self) -> tuple[int, int, float]:
        unique_kanji: int = self.unique_kanji
        unique_kanji_used_once: int = self.unique_kanji_used_once

        unique_kanji_percentage: float = percent_of(unique_kanji_used_once, unique_kanji)

        return unique_kanji, unique_kanji_used_once, unique_kanji_percentage

    def generate_text_info(self) -> TextInfo:
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

    def add_word(self, word: UnidicNode) -> None:
        """
        Adds a word to the frequency list.

        If the word is already in the list, then the frequency is increased by 1.
        Otherwise, the word is added to the list with a frequency of 1.

        Note: This method assumes the word is valid.
        """
        self._word_count += 1

        self._update_kanji(word)

        representation = word.feature.lemma

        if not representation:
            return

        if representation in self._unique_words.keys():
            self._append_representation(word)
            return

        # if there is no representation of this word then we must add one
        self._unique_words[representation] = [WordSlot(word, 1)]

    def parse_line(self, line: str) -> list[UnidicNode]:
        """
        Parses a line of text into a list of UnidicNodes.
        """
        return self._tagger(line)

    def process_line(self, line_to_process: str) -> None:
        """
        Parses a line, adding the valid words to the frequency list.
        """
        words = self.parse_line(line_to_process)

        [self.add_word(word) for word in words if self._word_validator(word)]

    def process_text(self, text_to_process: str) -> None:
        """
        Parses a text, adding the valid words to the frequency list.
        """
        [self.process_line(line) for line in text_to_process.split("\n")]

    def process_texts(self, texts_to_process: list) -> None:
        """
        Parses a list of texts, adding the valid words to the frequency list.
        """
        [self.process_text(text) for text in texts_to_process]

    def process_file(self, file_path: str) -> None:
        """
        
        """
        if not file_exists(file_path):
            raise FileExistsError(
                f"process_file: File path passed doesn't exist ({file_path})"
            )

        with open(file_path, "r", encoding="utf-8") as fs:
            [self.process_line(line) for line in fs]
