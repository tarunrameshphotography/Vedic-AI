"""Globally unique identities for the corpus.

The single most dangerous property of the original single-book pipeline was that page
identifiers were unique only *within* a book. Every book has an "s001a", so a sidecar
file keyed on that identifier silently applies to the wrong book the moment a second
book exists. Every identifier below is therefore globally qualified.

    book_id   brihat-jataka                 slug, unique across the corpus
    page_id   brihat-jataka/p0007           book-qualified, opaque, densely numbered

`page_id` deliberately carries no information about scan layout. Brihat Jataka is
scanned two pages to a sheet and its old ids encoded that ("s004b" = spread 4, right
half); no other book is. Layout now lives in `source_ref`, which is provenance, not
identity.
"""
import re

BOOK_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PAGE_ID_RE = re.compile(r"^([a-z0-9]+(?:-[a-z0-9]+)*)/p(\d{4,})$")


class IdError(ValueError):
    pass


def check_book_id(book_id):
    if not BOOK_ID_RE.match(book_id or ""):
        raise IdError(f"invalid book_id {book_id!r}: expected a lowercase slug, "
                      f"e.g. 'brihat-jataka'")
    return book_id


def page_id(book_id, seq):
    """Build a globally unique page id. `seq` is 1-based and dense within the book."""
    check_book_id(book_id)
    if not isinstance(seq, int) or seq < 1:
        raise IdError(f"invalid page sequence {seq!r}: expected an integer >= 1")
    return f"{book_id}/p{seq:04d}"


def parse_page_id(pid):
    """Return (book_id, seq). Raises IdError on anything book-local or malformed."""
    m = PAGE_ID_RE.match(pid or "")
    if not m:
        raise IdError(
            f"invalid page_id {pid!r}: expected '<book-id>/pNNNN'. Bare page ids such "
            f"as 's001a' are book-local and are no longer accepted anywhere.")
    return m.group(1), int(m.group(2))


def page_book(pid):
    return parse_page_id(pid)[0]


def page_seq(pid):
    return parse_page_id(pid)[1]


def local_name(pid):
    """Filename stem for a page inside its own book directory."""
    return f"p{page_seq(pid):04d}"
