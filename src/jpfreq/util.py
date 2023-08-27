"""
.. include:: ../../documentation/util.md
"""

from fugashi import UnidicNode


def percent_of(part: [int | float], total: [int | float]) -> float:
    """
    Gets the part of the total as a percentage.
    Parameters
    ----------
    part : [int | float]
        Fraction of the total.

    total : [int | float]
        Total value.

    Returns
    -------
    float
        Part percent of total.
    """
    if total == 0:
        return 0

    return (part / total) * 100


def parse_pos_node(pos: str) -> list[str]:
    """
    Parses a POS node from fugashi into a list of POS values.
    This is essentially a wrapper around str.split(",") that gets the `WordType`(s) from the POS value.
    Parameters
    ----------
    pos : str
        The POS node to parse. This is a comma separated string of POS values. e.g. "名詞,一般,*,*"
    Returns
    -------
    list[str]
        A list of POS values.

    """
    split_pos: list[str] = pos.split(",")

    if len(split_pos) == 1 and split_pos[0] == "":
        return []

    return [pos_value for pos_value in split_pos if pos_value != "*"]


def word_rep(word: UnidicNode):
    """
    Gets the string representation of a UnidicNode.
    This is the lemma of the word.

    Parameters
    ----------
    word : UnidicNode
        The word to get the representation of.

    Returns
    -------
    str
        The string representation of the word.
    """

    if word.feature.lemma is None:
        return word.surface

    return f"{word.feature.lemma.split('-')[0]}"
