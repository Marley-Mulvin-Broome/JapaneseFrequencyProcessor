from fugashi import UnidicNode


def percent_of(part: [int | float], total: [int | float]) -> float:
    if total == 0:
        return 0

    return (part / total) * 100


def pos_same_at_index(pos_1: str, pos_2: str, index: int) -> bool:
    split_pos_1: list[str] = pos_1.split(",")
    split_pos_2: list[str] = pos_2.split(",")

    if len(split_pos_1) <= index or len(split_pos_2) <= index:
        return False

    return split_pos_1[index] == split_pos_2[index]


def parse_pos_node(pos: str) -> list[str]:
    split_pos: list[str] = pos.split(",")

    if len(split_pos) == 1 and split_pos[0] == "":
        return []

    return [pos_value for pos_value in split_pos if pos_value != "*"]


def word_rep(word: UnidicNode):
    """
    Gets the string representation of a word.
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
