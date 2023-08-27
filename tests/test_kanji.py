from jpfreq.kanji import is_character_kanji, all_kanji_in_string, Kanji

import pytest

# hiragana unicode starts at ぁ ends at ゖ
hiragana = [chr(x) for x in range(ord("ぁ"), ord("ゖ") + 1)]
katakana = [chr(x) for x in range(ord("゠"), ord("ヿ") + 1)]

kanji_test = [
    ("日", True),
    ("本", True),
    ("語", True),
    ("畑", True),  # 和製漢字 Kanji made in Japan
    ("你", True),  # Chinese character (hanzi)
]

kanji_test.extend([(x, False) for x in hiragana])
kanji_test.extend([(x, False) for x in katakana])


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
    ("日本語", [Kanji("日", 1), Kanji("本", 1), Kanji("語", 1)]),
    ("ここ", []),
    ("この本は面白いです", [Kanji("本", 1), Kanji("面", 1), Kanji("白", 1)]),
    ("ググれば、分かると思うよ", [Kanji("分", 1), Kanji("思", 1)]),
    ("ググってください", []),
    ("ググります", []),
    ("傘がパクられた", [Kanji("傘", 1)]),
    ("你", [Kanji("你", 1)]),  # Chinese character (hanzi)
    ("この畑は母のものです", [Kanji("畑", 1), Kanji("母", 1)]),  # 和製漢字 Kanji made in Japan
]


@pytest.mark.parametrize("input_string,expected", kanji_in_string_test)
def test_all_kanji_in_string(input_string, expected):
    assert all_kanji_in_string(input_string) == expected
