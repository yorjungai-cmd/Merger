import os
import zipfile
import pytest
from pathlib import Path
from cbz_merger import CBZMerger


def test_natural_sort_orders_numerically():
    merger = CBZMerger()
    names = ["img10.jpg", "img2.jpg", "img1.jpg"]
    result = sorted(names, key=merger.natural_sort_key)
    assert result == ["img1.jpg", "img2.jpg", "img10.jpg"]


def test_natural_sort_handles_no_digits():
    merger = CBZMerger()
    names = ["banana.jpg", "apple.jpg", "cherry.jpg"]
    result = sorted(names, key=merger.natural_sort_key)
    assert result == ["apple.jpg", "banana.jpg", "cherry.jpg"]


def test_is_image_file_accepts_common_formats():
    merger = CBZMerger()
    assert merger.is_image_file("page.jpg") is True
    assert merger.is_image_file("page.JPG") is True
    assert merger.is_image_file("page.png") is True
    assert merger.is_image_file("page.webp") is True
    assert merger.is_image_file("readme.txt") is False
    assert merger.is_image_file("archive.cbz") is False


def test_is_supported_file_accepts_archives():
    merger = CBZMerger()
    assert merger.is_supported_file("vol.cbz") is True
    assert merger.is_supported_file("vol.CBZ") is True
    assert merger.is_supported_file("vol.cbr") is True
    assert merger.is_supported_file("vol.zip") is True
    assert merger.is_supported_file("vol.rar") is True
    assert merger.is_supported_file("vol.pdf") is False


def test_extract_cbz_returns_true_and_extracts(tmp_path):
    cbz = tmp_path / "test.cbz"
    with zipfile.ZipFile(cbz, "w") as zf:
        zf.writestr("001.jpg", b"x" * 100)
        zf.writestr("002.jpg", b"x" * 100)
    out = tmp_path / "out"
    out.mkdir()
    merger = CBZMerger()
    assert merger.extract_archive(str(cbz), str(out)) is True
    assert (out / "001.jpg").exists()
    assert (out / "002.jpg").exists()


def test_extract_missing_file_returns_false(tmp_path):
    merger = CBZMerger()
    assert merger.extract_archive(str(tmp_path / "nope.cbz"), str(tmp_path)) is False


def test_collect_images_sorted_naturally(tmp_path):
    for name in ["img010.jpg", "img002.jpg", "img001.jpg"]:
        (tmp_path / name).write_bytes(b"x")
    merger = CBZMerger()
    result = merger.collect_images_by_subfolder(str(tmp_path))
    names = [Path(img).name for _, img in result]
    assert names == ["img001.jpg", "img002.jpg", "img010.jpg"]


def test_merge_produces_valid_cbz(tmp_path):
    src = tmp_path / "input.cbz"
    with zipfile.ZipFile(src, "w") as zf:
        zf.writestr("001.jpg", b"x" * 200)
        zf.writestr("002.jpg", b"x" * 200)
    out = str(tmp_path / "output.cbz")
    merger = CBZMerger()
    assert merger.merge_archives([str(src)], out) is True
    assert os.path.exists(out)
    with zipfile.ZipFile(out) as zf:
        assert len(zf.namelist()) == 2


def test_merge_empty_input_returns_false(tmp_path):
    merger = CBZMerger()
    assert merger.merge_archives([], str(tmp_path / "out.cbz")) is False


def test_extract_unsupported_extension_returns_false(tmp_path):
    f = tmp_path / "archive.tar"
    f.write_bytes(b"fake")
    merger = CBZMerger()
    assert merger.extract_archive(str(f), str(tmp_path)) is False


def test_find_archives_in_folder_returns_sorted_archives(tmp_path):
    for name in ["vol003.cbz", "vol001.cbz", "vol002.zip", "readme.txt"]:
        (tmp_path / name).write_bytes(b"x")
    merger = CBZMerger()
    result = merger.find_archives_in_folder(str(tmp_path))
    names = [Path(p).name for p in result]
    assert names == ["vol001.cbz", "vol002.zip", "vol003.cbz"]


def test_find_archives_in_folder_empty_when_no_archives(tmp_path):
    (tmp_path / "image.jpg").write_bytes(b"x")
    merger = CBZMerger()
    assert merger.find_archives_in_folder(str(tmp_path)) == []


def test_find_archives_in_folder_non_recursive(tmp_path):
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "nested.cbz").write_bytes(b"x")
    merger = CBZMerger()
    assert merger.find_archives_in_folder(str(tmp_path)) == []
