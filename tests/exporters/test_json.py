from jpfreq.exporters.json import JsonExporter
from jpfreq.jp_frequency_list import JapaneseFrequencyList
from jpfreq.word import WordType

import pytest


@pytest.fixture()
def exporter():
    return JsonExporter()


@pytest.fixture()
def freq_list():
    return JapaneseFrequencyList()


# test_to_dict_data = [
#     ("", {}),
#     ("あ", {"words": [{"surface": "あ", "types": [WordType.VERB], "frequency": 1}]}),
# ]
#
#
# @pytest.mark.parametrize("text, expected", test_to_dict_data)
# def test_to_dict(exporter, freq_list: JapaneseFrequencyList, text, expected):
#     freq_list.process_text(text)
#     assert exporter._create_export_dictionary(freq_list) == expected
#

#
# @pytest.mark.parametrize("text, expected", test_export_data)
# def test_export(exporter, freq_list: JapaneseFrequencyList, text, expected):
#     freq_list.process_text(text)
#     assert exporter.export(freq_list).strip() == expected.strip()
