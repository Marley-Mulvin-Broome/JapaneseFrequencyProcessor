from fugashi import UnidicNode
from dataclasses import dataclass
from typing import Iterable


@dataclass
class WordSlot:
    word: UnidicNode
    frequency: int


def sum_wordslots(word_slots: Iterable[WordSlot]) -> int:
    return sum(slot.frequency for slot in word_slots)


def get_unique_wordslots(word_slots: Iterable[WordSlot]) -> int:
    return [slot for slot in word_slots if slot.frequency == 1]
