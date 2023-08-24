from jpfreq.word_slot import WordSlot, sum_wordslots, get_unique_wordslots

import pytest

sum_wordslots_data = [
    ([WordSlot("ワード", 1)], 1),
    ([WordSlot("ワード", 1), WordSlot("ワード", 1)], 2),
    ([WordSlot("ワード", 2), WordSlot("ワード", 1)], 3),
    ([WordSlot("ワード", 1), WordSlot("ワード", 2)], 3),
    ([WordSlot("ワード", 2), WordSlot("ワード", 2)], 4),
    ([WordSlot("行かれる", 1), WordSlot("行く", 1)], 2),
    ([], 0),
]


@pytest.mark.parametrize("word_slots,expected", sum_wordslots_data)
def test_sum_wordslots(word_slots, expected):
    assert sum_wordslots(word_slots) == expected


get_unique_wordslots_data = [
    ([WordSlot("ワード", 1)], [WordSlot("ワード", 1)]),
    (
        [WordSlot("ワード", 1), WordSlot("ワード", 1)],
        [WordSlot("ワード", 1), WordSlot("ワード", 1)],
    ),
    ([WordSlot("ワード", 2), WordSlot("ワード", 1)], [WordSlot("ワード", 1)]),
    ([WordSlot("ワード", 1), WordSlot("ワード", 2)], [WordSlot("ワード", 1)]),
    ([WordSlot("ワード", 2), WordSlot("ワード", 2)], []),
]


@pytest.mark.parametrize("word_slots,expected", get_unique_wordslots_data)
def test_get_unique_wordslots(word_slots, expected):
    assert get_unique_wordslots(word_slots) == expected
