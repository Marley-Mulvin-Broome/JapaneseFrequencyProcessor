from jpfreq.text_info import TextInfo


def test_invalid_eq():
    text_info = TextInfo()

    try:
        text_info == "Hello!"
        assert False
    except TypeError:
        assert True


def test_basic_eq():
    text_info = TextInfo()

    assert text_info == TextInfo()


def test_word_count_eq():
    text_info = TextInfo(word_count=1)

    assert text_info == TextInfo(word_count=1)


def test_unique_words_eq():
    text_info = TextInfo(unique_words=1)

    assert text_info == TextInfo(unique_words=1)


def test_unique_words_used_once_eq():
    text_info = TextInfo(unique_words_used_once=1)

    assert text_info == TextInfo(unique_words_used_once=1)


def test_unique_words_used_once_percentage_eq():
    text_info = TextInfo(unique_words_used_once_percentage=1)

    assert text_info == TextInfo(unique_words_used_once_percentage=1)


def test_unique_kanji_eq():
    text_info = TextInfo(unique_kanji=1)

    assert text_info == TextInfo(unique_kanji=1)


def test_unique_kanji_used_once_eq():
    text_info = TextInfo(unique_kanji_used_once=1)

    assert text_info == TextInfo(unique_kanji_used_once=1)


def test_unique_kanji_used_once_percentage_eq():
    text_info = TextInfo(unique_kanji_used_once_percentage=1)

    assert text_info == TextInfo(unique_kanji_used_once_percentage=1)


def test_word_count_ne():
    text_info = TextInfo(word_count=1)

    assert text_info != TextInfo()


def test_unique_words_ne():
    text_info = TextInfo(unique_words=1)

    assert text_info != TextInfo()


def test_unique_words_used_once_ne():
    text_info = TextInfo(unique_words_used_once=1)

    assert text_info != TextInfo()


def test_unique_words_used_once_percentage_ne():
    text_info = TextInfo(unique_words_used_once_percentage=1)

    assert text_info != TextInfo()


def test_unique_kanji_ne():
    text_info = TextInfo(unique_kanji=1)

    assert text_info != TextInfo()


def test_unique_kanji_used_once_ne():
    text_info = TextInfo(unique_kanji_used_once=1)

    assert text_info != TextInfo()


def test_unique_kanji_used_once_percentage_ne():
    text_info = TextInfo(unique_kanji_used_once_percentage=1)

    assert text_info != TextInfo()


def test_multiple_eq():
    text_info = TextInfo(
        word_count=1,
        unique_words=1,
        unique_words_used_once=1,
        unique_words_used_once_percentage=1,
        unique_kanji=1,
        unique_kanji_used_once=1,
        unique_kanji_used_once_percentage=1,
    )

    assert text_info == TextInfo(
        word_count=1,
        unique_words=1,
        unique_words_used_once=1,
        unique_words_used_once_percentage=1,
        unique_kanji=1,
        unique_kanji_used_once=1,
        unique_kanji_used_once_percentage=1,
    )


def test_multiple_ne():
    text_info = TextInfo(
        word_count=3,
        unique_words=3,
        unique_words_used_once=3,
        unique_words_used_once_percentage=3,
        unique_kanji=3,
        unique_kanji_used_once=3,
        unique_kanji_used_once_percentage=3,
    )

    assert text_info != TextInfo(
        word_count=2,
        unique_words=2,
        unique_words_used_once=2,
        unique_words_used_once_percentage=2,
        unique_kanji=2,
        unique_kanji_used_once=2,
        unique_kanji_used_once_percentage=2,
    )
