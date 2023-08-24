from jpfreq.kanji import is_character_kanji, all_kanji_in_string

import pytest

# hiragana unicode starts at ぁ ends at ゖ
hiraganas = [chr(x) for x in range(ord("ぁ"), ord("ゖ") + 1)]
katakanas = [chr(x) for x in range(ord("゠"), ord("ヿ") + 1)]

kanji_test = [
    ("日", True),
    ("本", True),
    ("語", True),
    ("畑", True),  # 和製漢字 Kanji made in Japan
    ("你", True),  # Chinese character (hanzi)
]

kanji_test.extend([(x, False) for x in hiraganas])
kanji_test.extend([(x, False) for x in katakanas])


@pytest.mark.parametrize("input_character,expected", kanji_test)
def test_is_character_kanji(input_character, expected):
    assert is_character_kanji(input_character) == expected


kanji_test_errors = [
    ("Hello!", TypeError),
    ("", TypeError),
    ("日本語", TypeError),
    ("ここ", TypeError),
]


@pytest.mark.parametrize("input_character,expected", kanji_test_errors)
def test_is_character_kanji_errors(input_character, expected):
    with pytest.raises(expected):
        is_character_kanji(input_character)


kanji_in_string_test = [
    ("日本語", ["日", "本", "語"]),
    ("ここ", []),
    ("この本は面白いです", ["本", "面", "白"]),
    ("ググれば、分かると思うよ", ["分", "思"]),
    ("ググってください", []),
    ("ググります", []),
    ("傘がパクられた", ["傘"]),
    ("你", ["你"]),  # Chinese character (hanzi)
    ("この畑は母のものです", ["畑", "母"]),  # 和製漢字 Kanji made in Japan
]


@pytest.mark.parametrize("input_string,expected", kanji_in_string_test)
def test_all_kanji_in_string(input_string, expected):
    assert all_kanji_in_string(input_string) == expected
