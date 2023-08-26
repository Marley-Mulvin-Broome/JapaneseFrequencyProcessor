from json import dumps
from collections import OrderedDict
from typing import Generator
from ..jp_frequency_list import JapaneseFrequencyList
from .iexporter import IExporter


class JsonExporter(IExporter):
    def __init__(self):
        pass

    @staticmethod
    def _create_export_dictionary(frequency_list: JapaneseFrequencyList, limit: int = 100, combine: bool=False) -> dict:
        frequency = frequency_list.get_most_frequent(limit=limit)
        dictionary = OrderedDict()

        dictionary["text_info"] = frequency_list.generate_text_info().to_dict()
        dictionary["word_slots"] = [slot.to_dict(combine=combine) for slot in frequency]

        return dictionary

    def export(self, frequency_list: JapaneseFrequencyList, limit: int = 100, combine: bool=False) -> str:
        return dumps(self._create_export_dictionary(frequency_list, limit=limit), ensure_ascii=False, indent=4)
    
    def export_lazy(self, frequency_list: JapaneseFrequencyList, limit: int = 100, combine: bool=False) -> Generator[str, None, None]:
        return super().export_lazy(frequency_list, limit)