#!/usr/bin/env python3

from .jp_frequency_list import JapaneseFrequencyList


# UniDic word contains:
# char_type
# feature
# feature_raw
# is_unk
# length
# pos
# posid
# rlength
# stat
# surface
# white_space

def main():
    freq_list = JapaneseFrequencyList()

    while True:
        input_text = ""

        try:
            input_text = input("Command> ")
        except KeyboardInterrupt and EOFError:
            print()
            break

        if input_text == "q":
            break
        elif input_text == "c":
            print(f"Cleared frequency list with {len(freq_list)} entries")
            freq_list.clear()
        elif input_text == "p":
            print(freq_list)
        elif input_text == "s":
            for word in freq_list.get_most_frequent():
                print(word)
        elif input_text.startswith("s "):
            word = input_text[2:]

            if word in freq_list:
                words = freq_list[word]

                for word in words:
                    print(word)
                    print(word.word.feature)
                    print(word.word.pos)
            else:
                print(f"Word '{word}' not found in frequency list")

        else:
            freq_list.process_line(input_text)


if __name__ == "__main__":
    main()
