# Fast count of the occurrences of words in a text file or a given string - low memory consumption

## pip install lowmemorywordcount 

#### Tested against Windows 10 / Python 3.10 / Anaconda 

The count_words function provides a powerful and customizable tool for counting word occurrences in both files and strings, making it valuable for a wide range of professionals dealing with textual data

### Customization: 

The function allows users to customize word counting by providing several optional parameters. Users can specify the encoding, error handling, chunk size for file reading, inclusion of hyphens in words, inclusion of words containing numbers, file mode, ignoring case sensitivity, and setting minimum and maximum word lengths. This level of customization allows users to tailor the word counting process to their specific requirements.

### Efficiency: 

The function reads the input file in chunks, which is memory-efficient for large files. By processing data in chunks, it reduces memory consumption and is suitable for handling large text files without running into memory-related issues.

### Unicode Support: 

The function leverages the regex library, which provides excellent support for Unicode characters. This means it can handle words from various languages and character sets, making it suitable for analyzing text data in diverse contexts.

### Word Frequency Counting: 

The function utilizes a defaultdict to store word frequencies, which provides a convenient way to count occurrences of words. Users can access the counts directly by using the word as a key without needing to initialize the count for each word manually.

### Flexibility: 

The function can work with both file paths and strings as inputs. This flexibility allows users to analyze text from different sources, whether it's from a file on disk or a dynamically generated string.


```python

    Parameters:
        file_or_string (str | bytes): The path to the text file or the input string.
        encoding (str, optional): The encoding to use for reading the file (default is "utf-8").
        errors (str, optional): How to handle encoding errors while reading the file (default is "ignore").
        chunk_size (int, optional): The size of the data chunk to read from the file (default is 8192 bytes).
        words_with_hyphen (bool, optional): Set to True to include hyphens as part of words (default is True).
        include_numbers (bool, optional): Set to True to include numbers like "111", strings like: "70s" are always included (default is False).
        mode (str, optional): The file mode to open the file (default is "r").
        ignore_case (bool, optional): Set to True to ignore the case when counting words (default is True).
        min_len (int | None, optional): The minimum length of words to include (default is None, which means no minimum).
        max_len (int | None, optional): The maximum length of words to include (default is None, which means no maximum).

    Returns:
        defaultdict: A defaultdict with words as keys and their occurrences as values.

    Example:
        from lowmemorywordcount import count_words
        # Count words in a text file
        di = count_words(
            file_or_string=r"F:\textfile.txt",
            encoding="utf-8",
            errors="ignore",
            chunk_size=8192,
            words_with_hyphen=False,
            include_numbers=False,
            mode="r",
            ignore_case=True,
            min_len=None,
            max_len=None,
        )

        from lowmemorywordcount import count_words
        # Count words in a string or file
        di = count_words(
            file_or_string=b"This is a sample text. It contains some words, including words like 'apple' and 'orange'.",
            encoding="utf-8",
            words_with_hyphen=False,
            include_numbers=False,
            ignore_case=True,
            min_len=3,
            max_len=10,
            mode='rb'
        )

        Out[6]:
        defaultdict(int,
                    {b'this': 1,
                     b'sample': 1,
                     b'text': 1,
                     b'contains': 1,
                     b'some': 1,
                     b'words': 2,
                     b'including': 1,
                     b'like': 1,
                     b'apple': 1,
                     b'and': 1,
                     b'orange': 1})

        from lowmemorywordcount import count_words
        di = count_words(
            file_or_string="This is a sample text. It contains some words, including words like 'apple' and 'orange'.",
            encoding="utf-8",
            words_with_hyphen=False,
            include_numbers=False,
            ignore_case=True,
            min_len=3,
            max_len=10,
            mode='r'
        )
        Out[8]:
        defaultdict(int,
                    {'this': 1,
                     'sample': 1,
                     'text': 1,
                     'contains': 1,
                     'some': 1,
                     'words': 2,
                     'including': 1,
                     'like': 1,
                     'apple': 1,
                     'and': 1,
                     'orange': 1})
```