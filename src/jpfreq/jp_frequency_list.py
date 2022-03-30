from fugashi import Tagger, UnidicNode
from typing import Callable
from unicodedata import name as u_name
from os.path import isfile as file_exists

from word_slot import WordSlot, sum_wordslots, get_wordslots_used_once
from text_info import TextInfo
from frequency_exporter import FrequencyExporter

SUPPLEMENTARY_SYMBOL: str = "補助記号"
PARTICLE: str = "助詞"
NOUN: str = "名詞"
PRONOUN: str = "代名詞"
VERB: str = "動詞"
SUFFIX: str = "接尾辞"
AUXILIARY_VERB: str = "助動詞"
NA_ADJECTIVE: str = "形状詞"
I_ADJECTIVE: str = "形容詞"
ADVERB: str = "福祉"
INTERJECTION: str = "感動詞"
BLANK_SPACE: str = "空白"
UNINDEPENDENT: str = "非自立可能"
NUMERAL: str = "数詞"

DEFAULT_INVALID_WORD_CLASSES: list[str] = [PARTICLE, AUXILIARY_VERB, SUPPLEMENTARY_SYMBOL, BLANK_SPACE, UNINDEPENDENT,
                                           NUMERAL]

KANJI_UNICODE_NAME = "CJK UNIFIED IDEOGRAPH"


def first_pos_same(pos_1: str, pos_2) -> bool:
    word_class_1: str = pos_1.split(',')[0]
    word_class_2: str = pos_2.split(',')[0]

    return word_class_1 == word_class_2


def parse_pos_node(pos: str) -> list[str]:
    split_pos: list[str] = pos.split(',')
    new_pos: list[str] = []

    for pos_value in split_pos:
        if pos_value == "*":
            break

        new_pos.append(pos_value)

    return new_pos


def default_word_validator(input_word: UnidicNode) -> bool:
    valid = True

    word_classes = parse_pos_node(input_word.pos)

    for word_class in word_classes:
        if word_class in DEFAULT_INVALID_WORD_CLASSES:
            return False

    return valid


def is_character_kanji(input_character: str):
    if len(input_character) > 1:
        raise TypeError(f"is_character_kanji: Expected str of length 1, got length of {len(input_character)} instead")

    return KANJI_UNICODE_NAME in u_name(input_character)


def all_kanji_in_string(input_string: str) -> list[str]:
    kanji: list[str] = []

    for character in input_string:

        if is_character_kanji(character):
            kanji.append(character)

    return kanji


def word_rep(word: UnidicNode):
    return f"{word.feature.lemma}"


class JapaneseFrequencyList:
    _unique_words: dict[str, list[WordSlot]]
    _unique_kanji: dict[str, WordSlot]
    _word_count: int
    _tagger: Tagger
    _exporter: FrequencyExporter
    _word_validator: Callable[[UnidicNode], bool]

    def __init__(self, word_validator: Callable[[UnidicNode], bool] = default_word_validator,
                 text_to_analyse: list = None, tagger_instance=None):
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

    def _update_kanji(self, word: UnidicNode) -> None:
        for kanji in all_kanji_in_string(str(word.surface)):
            if kanji not in self._unique_kanji:
                self._unique_kanji[kanji] = WordSlot(word, 1)
                continue

            self._unique_kanji[kanji].frequency += 1

    def _append_representation(self, word: UnidicNode) -> None:
        word_list = self._unique_words[word.feature.lemma]

        for word_slot in word_list:
            if first_pos_same(word_slot.word.pos, word.pos):
                word_slot.frequency += 1
                return

        # otherwise, we need to add another word to the list
        self._unique_words[word.feature.lemma].append(WordSlot(word, 1))

    def _loop_wordslots(self, loop_function: Callable[[WordSlot], None] = None) -> None:
        for word_list in self._unique_words.values():
            for word_slot in word_list:
                if loop_function:
                    loop_function(word_slot)

    def _get_wordslots(self) -> list[WordSlot]:
        slots: list[WordSlot] = []

        def add_slot(s):
            slots.append(s)

        self._loop_wordslots(add_slot)

        return slots

    def clear(self) -> None:
        self._word_count = 0

        self._unique_words.clear()
        self._unique_kanji.clear()

    def get_most_frequent(self, limit: int = 100) -> list[WordSlot]:
        item_array: list[WordSlot] = [None] * limit

        def frequency_function(word_slot: WordSlot) -> None:
            for index, current_item in enumerate(item_array):
                if current_item is None:
                    item_array[index] = word_slot
                    break
                if current_item.frequency < word_slot.frequency:
                    item_array.insert(index, word_slot)
                    item_array.pop(limit)
                    break

        self._loop_wordslots(frequency_function)

        return item_array

    def calculate_word_count(self) -> int:
        self._word_count = sum_wordslots(self._get_wordslots())

        return self._word_count

    def get_word_count(self) -> int:
        return self._word_count

    def get_unique_words(self) -> int:
        return len(self._get_wordslots())

    def get_unique_words_used_once(self) -> int:
        return get_wordslots_used_once(self._get_wordslots())

    def get_unique_words_all(self) -> tuple[int, int, float]:
        unique_words: int = self.get_unique_words()
        unique_words_used_once: int = self.get_unique_words_used_once()

        unique_word_percentage: float = (unique_words_used_once / unique_words) * 100

        return unique_words, unique_words_used_once, unique_word_percentage

    def get_unique_kanji(self) -> int:
        return len(self._unique_kanji)

    def get_unique_kanji_used_once(self) -> int:
        return get_wordslots_used_once(self._unique_kanji.values())

    def get_unique_kanji_all(self) -> tuple[int, int, float]:
        unique_kanji: int = self.get_unique_kanji()
        unique_kanji_used_once: int = self.get_unique_kanji_used_once()

        unique_kanji_percentage: float = (unique_kanji_used_once / unique_kanji) * 100

        return unique_kanji, unique_kanji_used_once, unique_kanji_percentage

    def generate_text_info(self) -> TextInfo:
        unique_words, unique_words_used_once, unique_word_percentage = self.get_unique_words_all()
        unique_kanji, unique_kanji_used_once, unique_kanji_percentage = self.get_unique_kanji_all()

        return TextInfo(self._word_count, unique_words, unique_words_used_once, unique_word_percentage, unique_kanji,
                        unique_kanji_used_once, unique_kanji_percentage)

    def add_word(self, word: UnidicNode) -> None:
        self._word_count += 1

        self._update_kanji(word)

        representation = word.feature.lemma

        if not representation:
            return

        print(type(representation))

        if representation in self._unique_words.keys():
            self._append_representation(word)
            return

        # if there is no representation of this word then we must add one
        self._unique_words[representation] = [WordSlot(word, 1)]

    def parse_line(self, line: str) -> list:
        return self._tagger(line)

    def process_line(self, line_to_process: str) -> None:
        words = self.parse_line(line_to_process)

        for word in words:
            is_valid = self._word_validator(word)
            if not is_valid:
                continue

            self.add_word(word)

    def process_text(self, text_to_process: str) -> None:
        for line in text_to_process.split('\n'):
            self.process_line(line)

    def process_texts(self, texts_to_process: list) -> None:
        for text_to_process in texts_to_process:
            self.process_text(text_to_process)

    def process_file(self, file_path: str) -> None:
        if not file_exists(file_path):
            raise FileExistsError(f"process_file: File path passed doesn't exist ({file_path})")

        with open(file_path, "r", encoding="utf-8") as fs:
            for line in fs:
                self.process_line(line)
