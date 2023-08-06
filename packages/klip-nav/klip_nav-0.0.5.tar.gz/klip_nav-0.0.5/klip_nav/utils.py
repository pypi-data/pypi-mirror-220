from dataclasses import field, dataclass
from collections import defaultdict
import re
from typing import Union


@dataclass
class Highlight:
    location: str
    time: str
    content: str


@dataclass
class Note:
    location: str
    time: str
    content: str


@dataclass
class Book:
    notes: list[Union[Note, Highlight]] = field(default_factory=list)


class SortedClippings:
    def __init__(self, clippings_filename: str) -> None:
        with open(clippings_filename, "r") as f:
            self.books = self.get_book_clippings(f.read())

    def get_book_clippings(self, raw_inp: str) -> defaultdict[str, Book]:
        """clippings file as input (str) and then parse it book-to-book"""
        X = [[i for i in j.split("\n") if i] for j in raw_inp.split("=" * 10)]
        res = defaultdict(Book)

        for i in X:
            if len(i) != 3:  # since bookmarks lack inherent content
                continue

            title = i[0]

            loc = re.search(r"(?<=location )((\d+-\d+)|\d+)", i[1])
            if loc is None:
                continue
            else:
                loc = loc.group(0)

            time = re.search(
                r"(?<=Added on )\w+, \d* \w+ \d+ \d+:\d+\d+:\d*", i[1]
            )
            if time is None:
                continue
            else:
                time = time.group(0)

            content = i[2]

            note_type = "hi" if "Your Highlight" in i[1] else "pn"
            if note_type == "pn":
                res[title].notes.append(Note(loc, time, content))
            elif note_type == "hi":
                res[title].notes.append(Highlight(loc, time, content))
        return res
