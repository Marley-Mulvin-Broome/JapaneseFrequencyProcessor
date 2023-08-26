from jpfreq.jp_frequency_list import (
    JapaneseFrequencyList,
    word_validator_exclude_by_type,
)
from jpfreq.text_info import TextInfo
from jpfreq.word import WordType, Word
from fugashi import Tagger

import pytest


def in_range(number: float, a: float, b: float) -> bool:
    return a <= number <= b


def compare_text_infos(actual: TextInfo, expected: TextInfo):
    assert actual.word_count == expected.word_count
    assert actual.unique_words == expected.unique_words
    assert actual.unique_words_used_once == expected.unique_words_used_once
    assert in_range(
        actual.unique_words_used_once_percentage,
        expected.unique_words_used_once_percentage - 0.1,
        expected.unique_words_used_once_percentage + 0.1,
    )
    assert actual.unique_kanji == expected.unique_kanji
    assert actual.unique_kanji_used_once == expected.unique_kanji_used_once
    assert in_range(
        actual.unique_kanji_used_once_percentage,
        expected.unique_kanji_used_once_percentage - 0.1,
        expected.unique_kanji_used_once_percentage + 0.1,
    )


@pytest.fixture
def freq_list(scope="global"):
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
        "これは日本語です",  # count '語' as a word
        TextInfo(
            unique_words=3,
            word_count=3,
            unique_words_used_once=3,
            unique_words_used_once_percentage=100,
            unique_kanji=3,
            unique_kanji_used_once=3,
            unique_kanji_used_once_percentage=100,
        ),
    ),
    (
        "これは日本語です。",
        TextInfo(
            unique_words=3,
            word_count=3,
            unique_words_used_once=3,
            unique_words_used_once_percentage=100,
            unique_kanji=3,
            unique_kanji_used_once=3,
            unique_kanji_used_once_percentage=100,
        ),
    ),
    (
        "これは日本語です。これは日本語です。",
        TextInfo(
            unique_words=3,
            word_count=6,
            unique_words_used_once=0,
            unique_words_used_once_percentage=0,
            unique_kanji=3,
            unique_kanji_used_once=0,
            unique_kanji_used_once_percentage=0,
        ),
    ),
    (
        "この人は誰ですか",
        TextInfo(
            unique_words=3,
            word_count=3,
            unique_words_used_once=3,
            unique_words_used_once_percentage=100,
            unique_kanji=2,
            unique_kanji_used_once=2,
            unique_kanji_used_once_percentage=100,
        ),
    ),
    (
        "本は本は本は本は本は本は本は本は本は本は本は本は",
        TextInfo(
            unique_words=1,
            word_count=12,
            unique_words_used_once=0,
            unique_words_used_once_percentage=0,
            unique_kanji=1,
            unique_kanji_used_once=0,
            unique_kanji_used_once_percentage=0,
        ),
    ),
    (
        "これはこれはこれはこれはこれはこれはこれはこれはこれはこれはこれはこれは",
        TextInfo(
            unique_words=1,
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
            unique_words=2,
            word_count=2,
            unique_words_used_once=2,
            unique_words_used_once_percentage=100,
            unique_kanji=4,
            unique_kanji_used_once=4,
            unique_kanji_used_once_percentage=100,
        ),
    ),
    (
        "郵便番号は123-4567です",
        TextInfo(
            unique_words=2,
            word_count=2,
            unique_words_used_once=2,
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
            unique_words=2,
            word_count=2,
            unique_words_used_once=2,
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
        ["日本", "学校"],
        TextInfo(
            unique_words=2,
            word_count=2,
            unique_words_used_once=2,
            unique_words_used_once_percentage=100,
            unique_kanji=4,
            unique_kanji_used_once=4,
            unique_kanji_used_once_percentage=100,
        ),
    ),
    (
        ["日本", "学校", "日本", "学校"],
        TextInfo(
            unique_words=2,
            word_count=4,
            unique_words_used_once=0,
            unique_kanji=4,
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
            unique_words=1,
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
    freq_list.process_file(str(file_path))
    text_info = freq_list.generate_text_info()

    compare_text_infos(text_info, expected_text_info)
    assert text_info == expected_text_info


def test_file_not_found(freq_list):
    with pytest.raises(FileExistsError):
        freq_list.process_file("not_found.txt")


def test_freq_provided_tagger():
    j = JapaneseFrequencyList(Tagger("-Owakati"))

    assert j._tagger is not None


def test_freq_provided_tagger_incorrect():
    with pytest.raises(TypeError):
        JapaneseFrequencyList(tagger_instance="String!")


def test_freq_text_to_analyse():
    j = JapaneseFrequencyList(text_to_analyse=["これはテストです"])

    assert len(j) == 2


def test_freq_len(freq_list):
    freq_list.process_text("これはテストです")

    assert len(freq_list) == 2


def test_freq_contains(freq_list):
    freq_list.process_text("これはテストです")

    assert "此れ" in freq_list


def test_freq_contains_not(freq_list):
    freq_list.process_text("これはテストです")

    assert "これ" not in freq_list  # will be kanji representation


def test_freq_getitem(freq_list):
    freq_list.process_text("これはテストです")

    assert len(freq_list["此れ"]) == 1


def test_freq_getitem_not(freq_list):
    freq_list.process_text("これはテストです")

    with pytest.raises(KeyError):
        freq_list["此れは"]


def test_freq_clear(freq_list):
    freq_list.process_text("これはテストです")

    assert len(freq_list) == 2

    freq_list.clear()

    assert len(freq_list) == 0


most_freq_data = [
    ("此れは此れはポテトです", "此れ", 2),
    ("此れは此れはポテトです", "ポテト", 1),
]


@pytest.mark.parametrize("text,word,expected", most_freq_data)
def test_freq_most_freq(text, word, expected, freq_list):
    freq_list.process_text(text)

    frequent_list = freq_list.get_most_frequent()

    for word_slot in frequent_list:
        if word in word_slot:
            assert word_slot.frequency == expected
            return

    assert False


def test_freq_most_freq_limit(freq_list):
    freq_list.process_text("此れは此れはポテトです")

    frequent_list = freq_list.get_most_frequent(limit=1)

    assert len(frequent_list) == 1


def test_freq_most_freq_limit_0(freq_list):
    freq_list.process_text("此れは此れはポテトです")

    frequent_list = freq_list.get_most_frequent(limit=0)

    assert len(frequent_list) == 0


def test_freq_most_freq_limit_negative_one(freq_list):
    freq_list.process_text("此れは此れはポテトです")

    frequent_list = freq_list.get_most_frequent(limit=-1)

    assert len(frequent_list) == len(freq_list)


def test_freq_most_freq_limit_gt_len(freq_list):
    freq_list.process_text("此れは此れはポテトです")

    frequent_list = freq_list.get_most_frequent(limit=100)

    assert len(frequent_list) == len(freq_list)


def test_freq_with_custom_tagger():
    JapaneseFrequencyList(tagger_instance=Tagger("-Owakati"))


word_validator_type_test_data = [
    (Word("wow", "wow", []), True, []),
    (Word("wow", "wow", [WordType.VERB]), False, [WordType.VERB]),
    (Word("wow", "wow", [WordType.I_ADJECTIVE]), True, [WordType.VERB]),
    (
        Word("wow", "wow", [WordType.I_ADJECTIVE]),
        False,
        [WordType.VERB, WordType.I_ADJECTIVE],
    ),
    (Word("wow", "wow", [WordType.I_ADJECTIVE]), True, []),
]


@pytest.mark.parametrize("word,expected,excluded_types", word_validator_type_test_data)
def test_word_validator_type(word, expected, excluded_types):
    assert word_validator_exclude_by_type(word, excluded_types) == expected


def test_word_validator_type_default():
    assert word_validator_exclude_by_type(Word("wow", "wow", [WordType.VERB]))


def test_word_validator_type_default_false():
    assert not (word_validator_exclude_by_type(Word("wow", "wow", [WordType.PARTICLE])))


get_representation_test_data = [
    ("俺", "俺"),
    ("おれ", "俺"),
    ("行かない", "行く"),
    ("これ", "此れ"),
    ("行かれる", "行く"),
]


@pytest.mark.parametrize("word,expected", get_representation_test_data)
def test_get_representation(word, expected, freq_list):
    assert freq_list.get_representation(word) == expected


def test_get_representation_invalid(freq_list):
    with pytest.raises(ValueError):
        freq_list.get_representation("")
