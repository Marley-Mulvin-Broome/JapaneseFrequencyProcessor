"""
.. include:: ../../documentation/word.md
"""

from enum import Enum
from dataclasses import dataclass
from fugashi import UnidicNode
from .util import parse_pos_node, word_rep


class WordType(Enum):
    """
    The different attributes of a word.

    Taken from: https://www.sketchengine.eu/tagset-jp-mecab/
    """

    # NOUNS
    NOUN: str = "名詞"
    COMMON_NOUN: str = "普通名詞"
    PRONOUN: str = "代名詞"
    PROPER_NOUN: str = "固有名詞"
    AUXILIARY_NOUN: str = "助動詞語幹"
    FIRST_NAME: str = "人名"
    FAMILY_NAME: str = "姓"
    PLACE_NAME: str = "地名"
    COUNTRY: str = "国"

    # VERBS
    VERB: str = "動詞"
    AUXILIARY_VERB: str = "助動詞"
    VERBAL_SURU: str = "サ変可能"
    ADVERB: str = "副詞"
    ADVERBIAL: str = "副詞可能"
    VERBAL: str = "動詞的"
    VERBAL_ADJECTIVAL: str = "サ変形状詞可能"

    # PARTICLES
    PARTICLE: str = "助詞"
    CASE_PARTICLE: str = "格助詞"
    BINDING_PARTICLE: str = "係助詞"
    ADVERBIAL_PARTICLE: str = "副助詞"
    CONJUNCTIVE_PARTICLE: str = "接続助詞"
    QUOTATIVE_PARTICLE: str = "引用助詞"
    NOMINAL_PARTICLE: str = "準体助詞"
    PHRASE_FINAL_PARTICLE: str = "終助詞"

    # ADJECTIVES
    NA_ADJECTIVE: str = "形状詞"  # Adjectival Noun
    I_ADJECTIVE: str = "形容詞"

    # NUMBERS
    NUMERAL: str = "数詞"
    COUNTER: str = "助数詞"
    POSSIBLE_COUNTER: str = "助数詞可能"

    # SUFFIX / PREFIX
    SUFFIX: str = "接尾辞"
    PREFIX: str = "接頭辞"

    # SUPPLEMENTARY
    SUPPLEMENTARY: str = "補助記号"
    ASCII_ART: str = "ＡＡ"
    EMOTICON: str = "顔文字"
    PERIOD: str = "句点"
    BRACKET_OPEN: str = "括弧開"
    BRACKET_CLOSE: str = "括弧閉"
    COMMA: str = "読点"
    CHARACTER: str = "文字"

    # OTHER
    GENERAL: str = "一般"
    FILLER: str = "フィラー"
    TARI: str = "タリ"
    SUPPLEMENTARY_SYMBOL: str = "補助記号"
    INTERJECTION: str = "感動詞"
    BLANK_SPACE: str = "空白"
    UNINDEPENDENT: str = "非自立可能"
    ADNOMINAL: str = "連体詞"


@dataclass()
class Word:
    representation: str
    surface: str
    types: list[WordType]
    frequency: int = 1

    @staticmethod
    def from_node(node: UnidicNode) -> "Word":
        """
        Creates a Word from a UnidicNode.
        Parameters
        ----------
        node : UnidicNode
            The node to create the word from.

        Returns
        -------
        Word
            The created word.

        """
        return Word(
            representation=word_rep(node),
            surface=node.surface,
            types=[WordType(word_type) for word_type in parse_pos_node(node.pos)],
            frequency=1,
        )

    def to_dict(self):
        """
        Converts the word to a dictionary.
        Returns
        -------
        dict
            The dictionary representation of the word.
        """
        return {
            "representation": self.representation,
            "surface": self.surface,
            "types": [word_type.value for word_type in self.types],
            "frequency": self.frequency,
        }
