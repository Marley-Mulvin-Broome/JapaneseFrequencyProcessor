from jpfreq.exporters.json import JsonExporter
from jpfreq.jp_frequency_list import JapaneseFrequencyList
from json import dumps

import pytest


@pytest.fixture()
def exporter():
    return JsonExporter()


@pytest.fixture()
def freq_list():
    return JapaneseFrequencyList()


test_to_dict_keys_data = [
    ("", ["text_info", "word_slots"], False, 100),
    ("あ", ["text_info", "word_slots"], False, 100),
    ("あ", ["text_info", "word_slots"], False, 1),
    ("あ", ["text_info", "word_slots"], False, -1),
    ("", ["text_info", "word_slots"], False, 100),
    ("あ", ["text_info", "word_slots"], True, 100),
    ("あ", ["text_info", "word_slots"], True, 1),
    ("あ", ["text_info", "word_slots"], True, -1),
]


@pytest.mark.parametrize("text, expected_keys, combine, limit", test_to_dict_keys_data)
def test_to_dict_keys(
    exporter, freq_list: JapaneseFrequencyList, text, expected_keys, combine, limit
):
    freq_list.process_text(text)
    result = exporter._create_export_dictionary(freq_list, combine=combine, limit=limit)

    for key in expected_keys:
        assert key in result.keys()


test_to_dict_word_slots_count_data = [
    ("", 0, False, 100),
    ("あ", 1, False, 100),
    ("あ", 1, False, 1),
    ("あ", 1, False, -1),
    ("猫が好き", 2, False, 100),
    ("猫が好き", 1, False, 1),
    ("猫が好き", 2, False, -1),
    ("猫が猫", 1, False, 100),
    ("猫が猫", 1, False, 1),
    ("猫が猫", 1, False, -1),
    ("あ", 1, True, 100),
    ("あ", 1, True, 1),
    ("あ", 1, True, -1),
    ("猫が好き", 2, True, 100),
    ("猫が好き", 1, True, 1),
    ("猫が好き", 2, True, -1),
    ("猫が猫", 1, True, 100),
    ("猫が猫", 1, True, 1),
    ("猫が猫", 1, True, -1),
]


@pytest.mark.parametrize(
    "text, expected_count, combine, limit", test_to_dict_word_slots_count_data
)
def test_to_dict_word_slots_count(
    exporter, freq_list: JapaneseFrequencyList, text, expected_count, combine, limit
):
    freq_list.process_text(text)
    result = exporter._create_export_dictionary(freq_list, combine=combine, limit=limit)

    assert len(result["word_slots"]) == expected_count


test_export_data = [
    ("", False, 100),
    ("あ", False, 100),
    ("あ", False, 1),
    ("あ", False, -1),
    ("猫が好き", False, 100),
    ("猫が好き", False, 1),
    ("猫が好き", False, -1),
    ("", True, 100),
    ("あ", True, 100),
    ("あ", True, 1),
    ("あ", True, -1),
    ("猫が好き", True, 100),
    ("猫が好き", True, 1),
    ("猫が好き", True, -1),
]


@pytest.mark.parametrize("text, combine, limit", test_export_data)
def test_export_string(exporter, freq_list, text, combine, limit):
    freq_list.process_text(text)
    result = exporter.export(freq_list, combine=combine, limit=limit)

    assert isinstance(result, str)
    assert result == dumps(
        exporter._create_export_dictionary(freq_list, combine=combine, limit=limit),
        ensure_ascii=False,
        indent=4,
    )


@pytest.mark.parametrize("text, combine, limit", test_export_data)
def test_export_dict(exporter, freq_list, text, combine, limit):
    freq_list.process_text(text)
    result = exporter.export(freq_list, combine=combine, limit=limit, as_dict=True)

    assert isinstance(result, dict)
    assert result == exporter._create_export_dictionary(
        freq_list, combine=combine, limit=limit
    )
