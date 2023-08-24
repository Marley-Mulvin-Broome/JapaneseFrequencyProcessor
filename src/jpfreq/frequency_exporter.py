from dataclasses import dataclass, asdict
from enum import Enum

from typing import Any
import re


class FrequencyExportTypes(Enum):
    plain_text = 0
    json = 1
    xml = 2
    html = 3


@dataclass
class ExportWord:
    kanji: str
    kana: str
    frequency: int

    def export_as_plain_text(self):
        return ""

    def export_as_json(self):
        return ""

    def export_as_xml(self):
        return ""

    def export_as_html(self):
        return f"<span>{self.kanji}</span>"

    def export_as_type(self, export_type: FrequencyExportTypes) -> Any:
        if export_type == FrequencyExportTypes.plain_text:
            return self.export_as_plain_text()
        elif export_type == FrequencyExportTypes.json:
            return self.export_as_json()
        elif export_type == FrequencyExportTypes.xml:
            return self.export_as_xml()
        elif export_type == FrequencyExportTypes.html:
            return self.export_as_html()

        raise TypeError(
            f"export_as_type: invalid FrequencyExportTypes passed ({export_type})"
        )


WORD_ORDER_REGEX = re.compile(r"(?<=%)(.*?)(?=%)")
WORD_ORDER_REGEX_WITHOUT_PERCENTAGE = re.compile(r"(?<=%)(.*?)(?=%)")


class WordOrder:
    _order: str  # example value: %kanji%,%kana%,%frequency%

    def __init__(self, order_string):
        self.set_order_string(order_string)

    def set_order_string(self, value):
        self._order = value

    def format_export_word(self, word: ExportWord) -> str:
        dict_version = asdict(word)

        formatted_string: str = self._order

        variables_to_replace = []

        for variable_match in WORD_ORDER_REGEX_WITHOUT_PERCENTAGE.findall(
            formatted_string
        ):
            variables_to_replace.append(variable_match)

        for variable_to_replace in variables_to_replace:
            formatted_string = WORD_ORDER_REGEX.sub(
                dict_version[variable_to_replace], formatted_string
            )

        return formatted_string


@dataclass
class FrequencyExportSettings:
    word_order: str
    export_type: FrequencyExportTypes


class FrequencyExporter:
    def __init__(self):
        pass
