from jpfreq.util import percent_of, parse_pos_node, word_rep
from fugashi import Tagger

import pytest

percent_of_data = [
    (1, 1, 100),
    (1, 2, 50),
    (2, 1, 200),
    (0, 1, 0),
    (1, 0, 0),
]


@pytest.mark.parametrize("part,total,expected", percent_of_data)
def test_percent_of(part, total, expected):
    assert percent_of(part, total) == expected


parse_pos_node_data = [
    ("名詞,一般,*,*", ["名詞", "一般"]),
    ("名詞", ["名詞"]),
    ("名詞,一般", ["名詞", "一般"]),
    ("", []),
]


@pytest.mark.parametrize("pos,expected", parse_pos_node_data)
def test_parse_pos_node(pos, expected):
    assert parse_pos_node(pos) == expected


def test_word_rep():
    tagger = Tagger()
    word = tagger("行かれる")[0]

    assert word_rep(word) == "行く"
