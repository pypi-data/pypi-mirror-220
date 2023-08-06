import os.path
from collections import defaultdict

from regex import regex


def count_words(
    file_or_string: str | bytes,
    encoding: str = "utf-8",
    errors: str = "ignore",
    chunk_size: int = 8192,
    words_with_hyphen: bool = True,
    include_numbers: bool = False,
    mode: str = "r",
    ignore_case: bool = True,
    min_len: int | None = None,
    max_len: int | None = None,
) -> defaultdict:
    r"""
    Count the occurrences of words in a text file or a given string.

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
    """

    def _get_words():
        nonlocal data
        nonlocal dataold
        data = dataold + data
        datasplit = nonword.split(data)
        if not allword.match(data[-1:]):
            dataold = datasplit[-1]
            datasplit = datasplit[:-1]

        else:
            dataold = newdataold
        for datas in datasplit:
            if not include_numbers:
                if renumbers.match(datas):
                    continue
                if max_len:
                    if len(datas) > max_len:
                        continue
                if min_len:
                    if len(datas) < min_len:
                        continue
            if datas:
                if ignore_case:
                    datas = datas.lower()
                d[datas] += 1
        return dataold

    d = defaultdict(int)

    kwa = {}
    if "b" not in mode:
        kwa["encoding"] = encoding
        kwa["errors"] = errors
        newdataold = ""
        dataold = ""
        if words_with_hyphen:
            allword = regex.compile(r"[\p{L}\p{N}-]")
            nonword = regex.compile(r"[^\p{L}\p{N}-]")
        else:
            allword = regex.compile(r"[\p{L}\p{N}]")
            nonword = regex.compile(r"[^\p{L}\p{N}]")
        renumbers = regex.compile(r"^\d+$")
    else:
        newdataold = b""
        dataold = b""
        if words_with_hyphen:
            allword = regex.compile(rb"[\p{L}\p{N}-]")
            nonword = regex.compile(rb"[^\p{L}\p{N}-]")
        else:
            allword = regex.compile(rb"[\p{L}\p{N}]")
            nonword = regex.compile(rb"[^\p{L}\p{N}]")
        renumbers = regex.compile(rb"^\d+$")
    if isinstance(file_or_string, str):
        if os.path.exists(file_or_string):
            with open(file_or_string, mode=mode, **kwa) as f:
                while data := f.read(chunk_size):
                    dataold = _get_words()
        else:
            data = file_or_string
            dataold = _get_words()
    else:
        data = file_or_string
        dataold = _get_words()
    return d
