from jpfreq.jp_frequency_list import JapaneseFrequencyList
from jpfreq.text_info import TextInfo

import pytest

def in_range(number: float, a: float, b: float) -> bool:
    return a <= number <= b

def compare_text_infos(actual: TextInfo, expected: TextInfo):
    assert actual.word_count == expected.word_count
    assert actual.unique_words == expected.unique_words
    assert actual.unique_words_used_once == expected.unique_words_used_once
    assert in_range(actual.unique_words_used_once_percentage, expected.unique_words_used_once_percentage - 0.1, expected.unique_words_used_once_percentage + 0.1)
    assert actual.unique_kanji == expected.unique_kanji
    assert actual.unique_kanji_used_once == expected.unique_kanji_used_once
    assert in_range(actual.unique_kanji_used_once_percentage, expected.unique_kanji_used_once_percentage - 0.1, expected.unique_kanji_used_once_percentage + 0.1)



@pytest.fixture
def freq_list():
    return JapaneseFrequencyList()


test_data_text = [
        (
            "これ",
            TextInfo(
                word_count=1,
                unique_words=1,
                unique_words_used_once=1,
                unique_words_used_once_percentage=100,
                unique_kanji=0,
                unique_kanji_used_once=0,
                unique_kanji_used_once_percentage=0,
            ),
        ),
        (
            "日",
            TextInfo(
                word_count=1,
                unique_words=1,
                unique_words_used_once=1,
                unique_words_used_once_percentage=100,
                unique_kanji=1,
                unique_kanji_used_once=1,
                unique_kanji_used_once_percentage=100,
            ),
        ),
        (
            "日本",
            TextInfo(
                word_count=1,
                unique_words=1,
                unique_words_used_once=1,
                unique_words_used_once_percentage=100,
                unique_kanji=2,
                unique_kanji_used_once=2,
                unique_kanji_used_once_percentage=100,
            ),
        ),
        (
            "これは日本語です",
            TextInfo(
                unique_words=2,
                word_count=2,
                unique_words_used_once=2,
                unique_words_used_once_percentage=100,
                unique_kanji=3,
                unique_kanji_used_once=3,
                unique_kanji_used_once_percentage=100,
            ),
        ),
        (
            "これは日本語です。",
            TextInfo(
                unique_words=2,
                word_count=2,
                unique_words_used_once=2,
                unique_words_used_once_percentage=100,
                unique_kanji=3,
                unique_kanji_used_once=3,
                unique_kanji_used_once_percentage=100,
            ),
        ),
        (
            "これは日本語です。これは日本語です。",
            TextInfo(
                unique_words=0,
                word_count=4,
                unique_words_used_once=0,
                unique_words_used_once_percentage=0,
                unique_kanji=0,
                unique_kanji_used_once=0,
                unique_kanji_used_once_percentage=0,
            ),
        ),
        (
            "この文章はダミーです。文字の大きさ、量、字間、行間等を確認するために入れています。",
            TextInfo(
                unique_words=14,
                word_count=14,
                unique_words_used_once=14,
                unique_words_used_once_percentage=100,
                unique_kanji=14,
                unique_kanji_used_once=11,
                unique_kanji_used_once_percentage=(11 / 14) * 100,
            ),
        ),
        (
            "本は本は本は本は本は本は本は本は本は本は本は本は",
            TextInfo(
                unique_words=0,
                word_count=12,
                unique_words_used_once=0,
                unique_words_used_once_percentage=0,
                unique_kanji=0,
                unique_kanji_used_once=0,
                unique_kanji_used_once_percentage=0,
            ),
        ),
        (
            "これはこれはこれはこれはこれはこれはこれはこれはこれはこれはこれはこれは",
            TextInfo(
                unique_words=0,
                word_count=12,
                unique_words_used_once=0,
                unique_words_used_once_percentage=0,
                unique_kanji=0,
                unique_kanji_used_once=0,
                unique_kanji_used_once_percentage=0,
            ),
        ),
        (
            "新しい本は面白いです",
            TextInfo(
                unique_words=3,
                word_count=3,
                unique_words_used_once=3,
                unique_words_used_once_percentage=100,
                unique_kanji=4,
                unique_kanji_used_once=4,
                unique_kanji_used_once_percentage=100,
            ),
        ),
        (
            "郵便番号",
            TextInfo(
                unique_words=1,
                word_count=1,
                unique_words_used_once=1,
                unique_words_used_once_percentage=100,
                unique_kanji=4,
                unique_kanji_used_once=4,
                unique_kanji_used_once_percentage=100,
            ),
        ),
        (
            "郵便番号は123-4567です",
            TextInfo(
                unique_words=1,
                word_count=1,
                unique_words_used_once=1,
                unique_words_used_once_percentage=100,
                unique_kanji=4,
                unique_kanji_used_once=4,
                unique_kanji_used_once_percentage=100,
            ),
        ),
        (
            "西暦2021年",
            TextInfo(
                unique_words=2,
                word_count=2,
                unique_words_used_once=2,
                unique_words_used_once_percentage=100,
                unique_kanji=3,
                unique_kanji_used_once=3,
                unique_kanji_used_once_percentage=100,
            ),
        ),
        (
            "クール",
            TextInfo(
                unique_words=1,
                word_count=1,
                unique_words_used_once=1,
                unique_words_used_once_percentage=100,
                unique_kanji=0,
                unique_kanji_used_once=0,
                unique_kanji_used_once_percentage=0,
            ),
        ),
        (
            "ググってください",
            TextInfo(
                unique_words=1,
                word_count=1,
                unique_words_used_once=1,
                unique_words_used_once_percentage=100,
                unique_kanji=0,
                unique_kanji_used_once=0,
                unique_kanji_used_once_percentage=0,
            ),
        ),
        (
            "ググります",
            TextInfo(
                unique_words=1,
                word_count=1,
                unique_words_used_once=1,
                unique_words_used_once_percentage=100,
                unique_kanji=0,
                unique_kanji_used_once=0,
                unique_kanji_used_once_percentage=0,
            ),
        ),
        (
            "傘がパクられた",
            TextInfo(
                unique_words=2,
                word_count=2,
                unique_words_used_once=2,
                unique_words_used_once_percentage=100,
                unique_kanji=1,
                unique_kanji_used_once=1,
                unique_kanji_used_once_percentage=100,
            ),
        ),
    ]

def idfn(val):
    return str(val[0], encoding="utf-8") if isinstance(val, tuple) else None

@pytest.mark.parametrize("text,expected_text_info", test_data_text, ids=idfn)
def test_text(text, expected_text_info, freq_list):
    freq_list.process_text(text)
    text_info = freq_list.generate_text_info()

    compare_text_infos(text_info, expected_text_info)
    assert text_info == expected_text_info

test_data_texts = [
        (
            ["日本語", "学校"],
            TextInfo(
                unique_words=2,
                word_count=2,
                unique_words_used_once=2,
                unique_words_used_once_percentage=100,
                unique_kanji=5,
                unique_kanji_used_once=5,
                unique_kanji_used_once_percentage=100,
            ),
        ),
        (
            ["日本語", "学校", "日本語", "学校"],
            TextInfo(
                unique_words=0,
                word_count=4,
                unique_words_used_once=0,
                unique_kanji=0,
                unique_kanji_used_once=0,
                unique_kanji_used_once_percentage=0,
            ),
        ),
        (
            ["学校に行きます", "家に帰ります"],
            TextInfo(
                unique_words=4,
                word_count=4,
                unique_words_used_once=4,
                unique_words_used_once_percentage=100,
                unique_kanji=5,
                unique_kanji_used_once=5,
                unique_kanji_used_once_percentage=100,
            ),
        ),
        (
            ["学校に行きます！", "家に帰ります。"],
            TextInfo(
                unique_words=4,
                word_count=4,
                unique_words_used_once=4,
                unique_words_used_once_percentage=100,
                unique_kanji=5,
                unique_kanji_used_once=5,
                unique_kanji_used_once_percentage=100,
            ),
        ),
        (
            ["これは", "これは", "これは"],
            TextInfo(
                unique_words=0,
                word_count=3,
                unique_words_used_once=0,
                unique_words_used_once_percentage=0,
                unique_kanji=0,
                unique_kanji_used_once=0,
                unique_kanji_used_once_percentage=0,
            ),
        ),
    ]

@pytest.mark.parametrize("texts,expected_text_info", test_data_texts)
def test_texts(texts, expected_text_info, freq_list):
    freq_list.process_texts(texts)
    text_info = freq_list.generate_text_info()

    compare_text_infos(text_info, expected_text_info)
    assert text_info == expected_text_info

@pytest.mark.parametrize("texts,expected_text_info", test_data_texts)
def test_file(texts, expected_text_info, tmp_path, freq_list):
    file_path = tmp_path / "test.txt"
    file_path.write_text("\n".join(texts), encoding="utf-8")
    freq_list.process_file(file_path)
    text_info = freq_list.generate_text_info()

    compare_text_infos(text_info, expected_text_info)
    assert text_info == expected_text_info
