from fugashi import Tagger

from jp_frequency_list import JapaneseFrequencyList, WordSlot
import unicodedata


def main():
    file_path = r"/novels/無職転生　- 異世界行ったら本気だす -/1 - 無職転生　- 異世界行ったら本気だす -.txt"

    freq_list = JapaneseFrequencyList()

    freq_list.process_file(file_path)

    txt_info = freq_list.generate_text_info()

    print(txt_info)

    none_count = 0

    duplicates = 0

    previous_words = []

    for frequency_word in freq_list.get_most_frequent(limit=1000):
        if frequency_word:
            print(f"Word: {frequency_word.word.feature.lemma}\tFrequency: {frequency_word.frequency}")
            duplicates += frequency_word.word.feature.lemma in previous_words
            previous_words.append(frequency_word)
            continue
        none_count += 1

    print(f"Duplicates count: {duplicates}")
    print(f"None count: {none_count}\nAmount meant to be none: {1000 - txt_info.unique_words}")


if __name__ == '__main__':
    main()
