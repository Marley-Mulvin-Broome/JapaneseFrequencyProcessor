# JPFreq

<!-- TOC -->
* [JPFreq](#jpfreq)
  * [Installation](#installation)
  * [Usage](#usage)
    * [Getting the most frequent words](#getting-the-most-frequent-words)
    * [Reading from a file](#reading-from-a-file)
<!-- TOC -->

![Tests](https://github.com/Marley-Mulvin-Broome/JapaneseFrequencyProcessor/actions/workflows/test.yaml/badge.svg)
![Docs](https://github.com/Marley-Mulvin-Broome/JapaneseFrequencyProcessor/actions/workflows/docs.yaml/badge.svg)
![Code Style: Black](https://camo.githubusercontent.com/d91ed7ac7abbd5a6102cbe988dd8e9ac21bde0a73d97be7603b891ad08ce3479/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f636f64652532307374796c652d626c61636b2d3030303030302e737667)

JPFreq is a frequency processor for Japanese text. It counts the words in Japanese text

## Installation

1. Install Fugashi and Unidic
    ```bash
   pip install fugashi[unidic]
   python3 -m unidic download
    ```
2. Install JPFreq
    ```bash
    pip install jpfreq
    ```

## Usage

For detailed usage, see the [documentation](https://marley-mulvin-broome.github.io/JapaneseFrequencyProcessor).

### Getting the most frequent words

```python
from jpfreq.jp_frequency_list import JapaneseFrequencyList

freq_list = JapaneseFrequencyList()
freq_list.process_line("私は猫です。")

print(freq_list.get_most_frequent())
```

### Reading from a file

```python
from jpfreq.jp_frequency_list import JapaneseFrequencyList

freq_list = JapaneseFrequencyList()
freq_list.process_file("path/to/file.txt")

print(freq_list.get_most_frequent())
```
