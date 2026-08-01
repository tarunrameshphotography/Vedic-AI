"""Per-book layout profile.

The original assembler hardcoded one book's page anatomy: chapter openers matched a
Devanagari "...अध्यायः" title, colophons started "इति", and -- most dangerously -- *any*
line containing Devanagari was treated as a verse line. That last rule holds in Brihat
Jataka because Sanskrit appears there only as set-off verses. In BPHS and Jataka Parijata
Devanagari terms appear inline inside English prose, where the same rule would promote
ordinary paragraph lines to blockquoted verse and shred the surrounding text -- while the
verse audit, which only checks numbering, still passed.

Layout rules therefore live per book, in profiles/<book_id>.json, and the assembler is a
generic engine over them.
"""
import json
import os
import re

DEFAULTS = {
    "title": None,
    "script": "devanagari",
    # a verse line must look like verse, not merely contain the script
    "verse_requires_danda": True,
    "chapter_title_re": None,
    "colophon_re": r"^इति\s",
    "heading_max_len": 70,
    "running_header_min_pages": 4,
    "indent_min_offset": 25,
    "indent_max_offset": 130,
    "gutter_margin": 60,
    "page_number_max_digits": 3,
    # Where the printed page number sits. Brihat Jataka prints it at the head of the
    # page; Phaladeepika prints it at the foot. Getting this wrong leaves bare numerals
    # embedded in the prose ("Second house — the face 10").
    "page_number_position": "top",          # "top" | "bottom" | "both"
    # Figure-detection geometry. These are in the same units as the producer's bboxes:
    # image pixels for OCR (~300 dpi), PDF points for text extraction (~72/inch). A
    # band taller than one printed line makes every page look tabular.
    "figure_band_height": 40,
    "figure_narrow_width": 420,
}


class ProfileError(Exception):
    pass


class Profile:
    def __init__(self, book_id, data):
        self.book_id = book_id
        self.data = dict(DEFAULTS)
        self.data.update(data)
        for key in ("title", "chapter_title_re"):
            if not self.data.get(key):
                raise ProfileError(f"profile for {book_id}: {key!r} is required")
        self.chapter_title = re.compile(self.data["chapter_title_re"])
        self.colophon = re.compile(self.data["colophon_re"])

    def __getitem__(self, k):
        return self.data[k]

    @property
    def title(self):
        return self.data["title"]


def load(root, book_id):
    path = os.path.join(root, "profiles", book_id + ".json")
    if not os.path.exists(path):
        raise ProfileError(
            f"{path} missing. Every book needs a layout profile; the assembler no "
            f"longer carries any book's page anatomy as a default.")
    with open(path, encoding="utf-8") as f:
        return Profile(book_id, json.load(f))
