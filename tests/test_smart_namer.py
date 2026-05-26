import pytest
from cbz_merger import SmartNamer


def test_range_from_typical_chapter_names():
    namer = SmartNamer()
    assert namer.suggest(["A 1", "A 2", "A asdfasdf 3"], ".cbz") == "A 1-3.cbz"


def test_single_file_uses_original_name():
    namer = SmartNamer()
    assert namer.suggest(["Chapter 5"], ".cbz") == "Chapter 5.cbz"


def test_no_numbers_falls_back_to_merged_suffix():
    namer = SmartNamer()
    assert namer.suggest(["Alpha", "Beta", "Gamma"], ".cbz") == "Alpha_Merged.cbz"


def test_non_sequential_numbers_use_min_max():
    namer = SmartNamer()
    assert namer.suggest(["A 1", "A 3", "A 7"], ".cbz") == "A 1-7.cbz"


def test_empty_common_prefix_uses_numbers_only():
    namer = SmartNamer()
    assert namer.suggest(["1", "2", "3"], ".cbz") == "1-3.cbz"


def test_empty_list_returns_merged():
    namer = SmartNamer()
    assert namer.suggest([], ".cbz") == "Merged.cbz"


def test_all_same_number_no_range():
    namer = SmartNamer()
    assert namer.suggest(["Vol 5", "Vol 5"], ".cbz") == "Vol 5.cbz"


def test_pdf_extension_preserved():
    namer = SmartNamer()
    assert namer.suggest(["Book 1", "Book 2"], ".pdf") == "Book 1-2.pdf"


def test_two_files_simple_range():
    namer = SmartNamer()
    assert namer.suggest(["Manga 10", "Manga 20"], ".cbz") == "Manga 10-20.cbz"
