#!/usr/bin/env python3

from .jp_frequency_list import JapaneseFrequencyList


def main():
    freq_list = JapaneseFrequencyList()

    freq_list.process_text("ググってください。ググらない。ググります。ググりません。食べてください。食べない。食べます。食べません。")

    txt_info = freq_list.generate_text_info()

    print(txt_info)

    none_count = 0

    duplicates = 0

    previous_words = []

    from pprint import pprint
    pprint(freq_list._unique_words)

    for frequency_word in freq_list.get_most_frequent(limit=1000):
        if frequency_word:
            print(
                f"Word: {frequency_word.word.feature.lemma}\tFrequency: {frequency_word.frequency}"
            )
            duplicates += frequency_word.word.feature.lemma in previous_words
            previous_words.append(frequency_word)
            continue
        none_count += 1

    print(f"Duplicates count: {duplicates}")
    print(
        f"None count: {none_count}\nAmount meant to be none: {1000 - txt_info.unique_words}"
    )


if __name__ == "__main__":
    main()
