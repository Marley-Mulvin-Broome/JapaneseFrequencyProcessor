from jpfreq.word import Word, WordType

import pytest

to_dict_data = [
    (
        Word("test", "test", [], 1),
        {"representation": "test", "surface": "test", "types": [], "frequency": 1},
    ),
    (
        Word("test", "test", [WordType.NOUN, WordType.GENERAL], 1),
        {
            "representation": "test",
            "surface": "test",
            "types": ["名詞", "一般"],
            "frequency": 1,
        },
    ),
    (
        Word("test", "test", [WordType.VERB], 2),
        {"representation": "test", "surface": "test", "types": ["動詞"], "frequency": 2},
    ),
]


@pytest.mark.parametrize("word, expected_dict", to_dict_data)
def test_to_dict(word, expected_dict):
    assert word.to_dict() == expected_dict
