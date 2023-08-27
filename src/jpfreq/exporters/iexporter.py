"""
.. include:: ../../../documentation/exporters/iexporter.md
"""

import abc
from typing import Generator

from ..jp_frequency_list import JapaneseFrequencyList


class IExporter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def export(self, frequency_list: JapaneseFrequencyList, limit: int=100, combine: bool=True) -> str:
        raise NotImplementedError
    
    @abc.abstractmethod
    def export_lazy(self, frequency_list: JapaneseFrequencyList, limit: int=100, combine: bool=True) -> Generator[str, None, None]:
        raise NotImplementedError
