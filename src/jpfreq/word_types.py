from enum import Enum


class WordType(Enum):
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
