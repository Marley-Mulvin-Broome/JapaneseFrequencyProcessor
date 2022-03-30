from fugashi import UnidicNode
from dataclasses import dataclass
from typing import Iterable


@dataclass
class WordSlot:
    word: UnidicNode
    frequency: int


def sum_wordslots(word_slots: Iterable[WordSlot]) -> int:
    count: int = 0

    for slot in word_slots:
        count += slot.frequency

    return count


def get_wordslots_used_once(word_slots: Iterable[WordSlot]) -> int:
    count: int = 0

    for slot in word_slots:
        count += slot.frequency == 1

    return count
