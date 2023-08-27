"""
.. include:: ../../documentation/main.md
"""

from .jp_frequency_list import JapaneseFrequencyList
from .exporters.iexporter import IExporter
from .exporters.json import JsonExporter

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


def get_exporter(exporter_name: str) -> IExporter:
    exporter_name = exporter_name.lower().strip()

    if exporter_name == "json":
        return JsonExporter()

    raise ValueError(f"Unknown exporter '{exporter_name}'")


def main():
    freq_list = JapaneseFrequencyList()

    while True:
        input_text = ""

        try:
            input_text = input("Command> ")
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
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

        elif input_text.startswith("e "):
            exporter_name = input_text.split(" ")[1]

            exporter = None

            try:
                exporter = get_exporter(exporter_name)
            except ValueError as e:
                print(e)
                continue

            print(exporter.export(freq_list))

        elif input_text.startswith("i "):
            input_text = input_text[2:]
            for word in freq_list.parse_line(input_text):
                print(word)

        else:
            freq_list.process_line(input_text)


if __name__ == "__main__":
    main()
