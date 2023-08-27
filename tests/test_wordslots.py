from jpfreq.word_slot import WordSlot, get_unique_wordslots
from jpfreq.word import Word, WordType

import pytest


get_unique_wordslots_data = [
    (
        [WordSlot([Word("test", "test", [], 1)])],
        [WordSlot([Word("test", "test", [], 1)])],
    ),
    ([WordSlot([Word("test", "test", [], 2)])], []),
    ([WordSlot([Word("test", "test", [], 1000)])], []),
    (
        [
            WordSlot([Word("test", "test", [], 1)]),
            WordSlot([Word("test", "test", [], 2)]),
        ],
        [WordSlot([Word("test", "test", [], 1)])],
    ),
    (
        [
            WordSlot([Word("test", "test", [], 1)]),
            WordSlot([Word("test", "test", [], 1)]),
        ],
        [
            WordSlot([Word("test", "test", [], 1)]),
            WordSlot([Word("test", "test", [], 1)]),
        ],
    ),
]


@pytest.mark.parametrize("word_slots,expected", get_unique_wordslots_data)
def test_get_unique_wordslots(word_slots, expected):
    assert get_unique_wordslots(word_slots) == expected


def test_wordslot_contains():
    word_slot = WordSlot([Word("test", "test", [], 1)])

    assert Word("test", "test", [], 1) in word_slot
    assert "test" in word_slot
    assert Word("test", "test", [], 2) not in word_slot
    assert "test2" not in word_slot


def test_wordslot_len():
    word_slot = WordSlot([Word("test", "test", [], 1)])

    assert len(word_slot) == 1
    assert word_slot.frequency == 1
    assert word_slot.frequency == len(word_slot)


wordslot_to_dict_data = [
    (
        WordSlot([Word("test", "test", [], 1)]),
        False,
        {
            "words": [
                {
                    "representation": "test",
                    "surface": "test",
                    "types": [],
                    "frequency": 1,
                }
            ]
        },
    ),
    (
        WordSlot([Word("test", "test", [], 1)]),
        True,
        {"representation": "test", "surface": "test", "types": [], "frequency": 1},
    ),
    (
        WordSlot([Word("test", "test", [WordType.NOUN, WordType.GENERAL], 1)]),
        False,
        {
            "words": [
                {
                    "representation": "test",
                    "surface": "test",
                    "types": ["名詞", "一般"],
                    "frequency": 1,
                }
            ]
        },
    ),
    (
        WordSlot([Word("test", "test", [WordType.NOUN, WordType.GENERAL], 1)]),
        True,
        {
            "representation": "test",
            "surface": "test",
            "types": ["名詞", "一般"],
            "frequency": 1,
        },
    ),
    (
        WordSlot(
            [
                Word("test", "test", [WordType.NOUN, WordType.GENERAL], 1),
                Word("test2", "test", [WordType.NOUN, WordType.GENERAL], 1),
            ]
        ),
        False,
        {
            "words": [
                {
                    "representation": "test",
                    "surface": "test",
                    "types": ["名詞", "一般"],
                    "frequency": 1,
                },
                {
                    "representation": "test2",
                    "surface": "test",
                    "types": ["名詞", "一般"],
                    "frequency": 1,
                },
            ]
        },
    ),
    (
        WordSlot(
            [
                Word("test2", "test", [WordType.NOUN, WordType.GENERAL], 1),
                Word("test", "test", [WordType.NOUN, WordType.GENERAL], 1),
            ]
        ),
        True,
        {
            "representation": "test",
            "surface": "test",
            "types": ["名詞", "一般"],
            "frequency": 2,
        },
    ),
    (
        WordSlot(
            [
                Word("test", "test", [WordType.NOUN, WordType.GENERAL], 1),
                Word("test", "test2", [WordType.NOUN, WordType.GENERAL], 1),
            ]
        ),
        False,
        {
            "words": [
                {
                    "representation": "test",
                    "surface": "test",
                    "types": ["名詞", "一般"],
                    "frequency": 1,
                },
                {
                    "representation": "test",
                    "surface": "test2",
                    "types": ["名詞", "一般"],
                    "frequency": 1,
                },
            ]
        },
    ),
    (
        WordSlot(
            [
                Word(
                    representation="test",
                    surface="test2",
                    types=[WordType.NOUN, WordType.GENERAL],
                    frequency=1,
                ),
                Word(
                    representation="test",
                    surface="test",
                    types=[WordType.NOUN, WordType.GENERAL],
                    frequency=1,
                ),
            ]
        ),
        True,
        {
            "representation": "test",
            "surface": "test",
            "types": ["名詞", "一般"],
            "frequency": 2,
        },
    ),
]


def wordslot_idfn(val):
    if isinstance(val, WordSlot):
        return f"WordSlot({val.words})"
    if isinstance(val, bool):
        return f"combined={val}"
    return val


@pytest.mark.parametrize(
    "word_slot,combined,expected", wordslot_to_dict_data, ids=wordslot_idfn
)
def test_wordslot_to_dict(word_slot, combined, expected):
    assert word_slot.to_dict(combine=combined) == expected


def test_wordslot_to_dict_empty():
    word_slot = WordSlot([])

    assert word_slot.to_dict() == {}
    assert word_slot.to_dict(combine=True) == {}
