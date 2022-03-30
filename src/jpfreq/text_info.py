from dataclasses import dataclass


@dataclass
class TextInfo:
    word_count: int = 0
    unique_words: int = 0
    unique_words_used_once: int = 0
    unique_words_used_once_percentage: float = 0
    unique_kanji: int = 0
    unique_kanji_used_once: int = 0
    unique_kanji_used_once_percentage: float = 0
