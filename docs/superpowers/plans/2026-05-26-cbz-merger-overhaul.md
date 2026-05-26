# CBZ Merger Full Overhaul — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite `cbz_merger.py` from tkinter to PyQt6 with Modern Clean UI, SmartNamer auto-naming, auto-clear after merge, and 3 bug fixes, distributable as source or `.exe`.

**Architecture:** Single file `cbz_merger.py` — four classes: `CBZMerger` (bug-fixed core), `SmartNamer` (filename analysis), `FileListWidget(QWidget)` (list + drag-and-drop), `MainWindow(QMainWindow)` (full app). Merge runs in `MergeWorker(QThread)` with Qt signals for thread-safe UI updates. Two QSS stylesheets (light/dark) toggled at runtime and persisted via `QSettings`.

**Tech Stack:** Python 3.10+, PyQt6 ≥ 6.6, rarfile (optional), img2pdf (optional), Pillow (optional), PyInstaller (build only)

---

## File Map

| File | Action | Purpose |
|---|---|---|
| `cbz_merger.py` | Rewrite | Single-file app — all classes |
| `requirements.txt` | Create | Pinned dependencies |
| `tests/__init__.py` | Create | Make tests a package |
| `tests/test_core.py` | Create | Unit tests for CBZMerger |
| `tests/test_smart_namer.py` | Create | Unit tests for SmartNamer |
| `build.bat` | Create | PyInstaller one-liner |

---

## Task 1: Project Setup

**Files:**
- Create: `requirements.txt`
- Create: `tests/__init__.py`

- [ ] **Step 1: Create `requirements.txt`**

```
PyQt6>=6.6.0
rarfile>=4.0
img2pdf>=0.4.0
Pillow>=10.0.0
pytest>=8.0.0
```

- [ ] **Step 2: Install core dependency**

```
pip install PyQt6
```

Expected output ends with: `Successfully installed PyQt6-...`

- [ ] **Step 3: Verify PyQt6 import**

```
python -c "from PyQt6.QtWidgets import QApplication; print('PyQt6 OK')"
```

Expected: `PyQt6 OK`

- [ ] **Step 4: Create `tests/__init__.py`**

Empty file — just `touch tests/__init__.py` (or create with no content).

- [ ] **Step 5: Commit**

```bash
git add requirements.txt tests/__init__.py
git commit -m "chore: add requirements and tests scaffold"
```

---

## Task 2: CBZMerger Core — Bug Fixes + Unit Tests

**Files:**
- Create: `tests/test_core.py`
- Create: `cbz_merger.py` (core only, no GUI yet)

Write the fixed `CBZMerger` class into a fresh `cbz_merger.py`. The file at this stage contains only imports, feature flags, and `CBZMerger`. No GUI code yet.

- [ ] **Step 1: Write failing tests**

Create `tests/test_core.py`:

```python
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
```

- [ ] **Step 2: Run tests — expect ImportError (file doesn't exist yet)**

```
pytest tests/test_core.py -v
```

Expected: `ERROR` — `ModuleNotFoundError: No module named 'cbz_merger'`

- [ ] **Step 3: Write `cbz_merger.py` — imports, feature flags, CBZMerger**

```python
#!/usr/bin/env python3
"""
Yor CBZ Merger v3.0 — Comic Book Archive Merger Tool
Combines CBZ, CBR, ZIP, RAR files and image folders into a single CBZ or PDF.
Modern Clean UI · Light/Dark theme · PyQt6
"""

import os
import sys
import re
import zipfile
import tempfile
import threading
from pathlib import Path
from typing import Optional

# Optional dependency detection
try:
    import rarfile
    RAR_SUPPORT = True
except ImportError:
    RAR_SUPPORT = False

try:
    import img2pdf
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False


class CBZMerger:
    """Core logic for merging comic book archives."""

    SUPPORTED_EXTENSIONS = {'.cbz', '.cbr', '.zip', '.rar'}
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff'}

    def __init__(self, progress_callback=None, log_callback=None):
        self.progress_callback = progress_callback
        self.log_callback = log_callback

    def log(self, message: str):
        if self.log_callback:
            self.log_callback(message)
        print(message)

    def update_progress(self, value: float, status: str = ""):
        if self.progress_callback:
            self.progress_callback(value, status)

    def is_supported_file(self, filepath: str) -> bool:
        return Path(filepath).suffix.lower() in self.SUPPORTED_EXTENSIONS

    def is_image_file(self, filename: str) -> bool:
        return Path(filename).suffix.lower() in self.IMAGE_EXTENSIONS

    def is_image_folder(self, folderpath: str) -> bool:
        if not os.path.isdir(folderpath):
            return False
        for root, dirs, files in os.walk(folderpath):
            for f in files:
                if self.is_image_file(f):
                    return True
        return False

    def extract_archive(self, archive_path: str, extract_to: str) -> bool:
        ext = Path(archive_path).suffix.lower()
        archive_name = Path(archive_path).stem
        try:
            if ext in {'.cbz', '.zip'}:
                with zipfile.ZipFile(archive_path, 'r') as zf:
                    zf.extractall(extract_to)
                return True
            elif ext in {'.cbr', '.rar'}:
                if not RAR_SUPPORT:
                    self.log("⚠️ RAR support not available. Install 'rarfile'.")
                    return False
                with rarfile.RarFile(archive_path, 'r') as rf:
                    rf.extractall(extract_to)
                return True
        except Exception as e:
            self.log(f"❌ Error extracting {archive_name}: {e}")
        return False  # covers unsupported ext and exception paths

    def natural_sort_key(self, path: str):
        name = Path(path).name if isinstance(path, str) else str(path)
        parts = re.split(r'(\d+)', name)
        return [int(p) if p.isdigit() else p.lower() for p in parts]

    def collect_images_by_subfolder(self, directory: str):
        subfolder_images: dict[str, list[str]] = {}
        for root, dirs, files in os.walk(directory):
            rel_path = os.path.relpath(root, directory)
            subfolder_name = "" if rel_path == "." else rel_path.split(os.sep)[0]
            for file in files:
                if self.is_image_file(file):
                    full_path = os.path.join(root, file)
                    subfolder_images.setdefault(subfolder_name, []).append(full_path)

        result = []
        for subfolder in sorted(subfolder_images.keys(), key=self.natural_sort_key):
            images = sorted(subfolder_images[subfolder], key=self.natural_sort_key)
            for img in images:
                result.append((subfolder, img))
        return result

    def merge_archives(self, input_items: list, output_path: str, output_pdf: bool = False) -> bool:
        if not input_items:
            self.log("❌ No input files/folders provided.")
            return False

        if output_pdf:
            if not PDF_SUPPORT:
                self.log("❌ PDF support not available. Install 'img2pdf'.")
                return False
            if not output_path.lower().endswith('.pdf'):
                output_path = output_path.rsplit('.', 1)[0] + '.pdf'
        else:
            if not output_path.lower().endswith('.cbz'):
                output_path = output_path.rsplit('.', 1)[0] + '.cbz'

        with tempfile.TemporaryDirectory() as temp_dir:
            all_images = []
            total = len(input_items)
            self.log(f"📚 Processing {total} item(s)...")
            self.update_progress(0, "Starting...")

            for idx, item_path in enumerate(input_items):
                item_name = Path(item_path).stem if os.path.isfile(item_path) else Path(item_path).name
                is_folder = os.path.isdir(item_path)

                if is_folder:
                    self.log(f"📁 [{idx + 1}/{total}] {Path(item_path).name}")
                    self.update_progress((idx / total) * 50, f"Processing {idx + 1}/{total}")
                    images = self.collect_images_by_subfolder(item_path)
                else:
                    ext = Path(item_path).suffix.lower()
                    icon = "📘" if ext == ".cbz" else "📕" if ext == ".cbr" else "📦"
                    self.log(f"{icon} [{idx + 1}/{total}] {Path(item_path).name}")
                    self.update_progress((idx / total) * 50, f"Extracting {idx + 1}/{total}")
                    extract_dir = os.path.join(temp_dir, f"{idx:04d}_{item_name}")
                    os.makedirs(extract_dir, exist_ok=True)
                    if not self.extract_archive(item_path, extract_dir):
                        continue
                    images = self.collect_images_by_subfolder(extract_dir)

                for subfolder, img_path in images:
                    all_images.append((idx, item_name, subfolder, img_path))
                self.log(f"   ✓ {len(images)} images")

            if not all_images:
                self.log("❌ No images found.")
                return False

            fmt = "PDF" if output_pdf else "CBZ"
            self.log(f"\n📦 Creating {fmt} ({len(all_images)} images)...")
            self.update_progress(50, f"Creating {fmt}...")

            try:
                if output_pdf:
                    image_paths = []
                    for i, (_, _, _, img_path) in enumerate(all_images):
                        ext = Path(img_path).suffix.lower()
                        if ext in {'.jpg', '.jpeg', '.png'}:
                            image_paths.append(img_path)
                        else:
                            try:
                                from PIL import Image
                                img = Image.open(img_path)
                                converted = os.path.join(temp_dir, f"{i:05d}.png")
                                img.save(converted, 'PNG')
                                image_paths.append(converted)
                            except ImportError:
                                self.log(f"   ⚠️ Skipping {Path(img_path).name} (install Pillow for conversion)")
                        self.update_progress(50 + ((i + 1) / len(all_images)) * 40, f"Preparing {i + 1}/{len(all_images)}")
                    self.update_progress(90, "Writing PDF...")
                    with open(output_path, "wb") as f:
                        f.write(img2pdf.convert(image_paths))
                else:
                    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                        for i, (_, _, _, img_path) in enumerate(all_images):
                            ext = Path(img_path).suffix
                            zf.write(img_path, f"{i + 1:05d}{ext}")
                            self.update_progress(50 + ((i + 1) / len(all_images)) * 50, f"Adding {i + 1}/{len(all_images)}")

                size_mb = os.path.getsize(output_path) / (1024 * 1024)
                self.log(f"\n✅ Created: {Path(output_path).name}")
                self.log(f"   📄 {len(all_images)} pages • {size_mb:.1f} MB")
                self.update_progress(100, "Complete!")
                return True
            except Exception as e:
                self.log(f"❌ Error: {e}")
                return False


if __name__ == "__main__":
    print("CBZMerger core loaded OK")
```

- [ ] **Step 4: Run tests — all should pass**

```
pytest tests/test_core.py -v
```

Expected: All 9 tests `PASSED`.

- [ ] **Step 5: Commit**

```bash
git add cbz_merger.py tests/test_core.py
git commit -m "feat: add CBZMerger core with bug fixes and unit tests"
```

---

## Task 3: SmartNamer Class (TDD)

**Files:**
- Create: `tests/test_smart_namer.py`
- Modify: `cbz_merger.py` (add `SmartNamer` class after `CBZMerger`)

- [ ] **Step 1: Write failing tests**

Create `tests/test_smart_namer.py`:

```python
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
```

- [ ] **Step 2: Run tests — expect failure**

```
pytest tests/test_smart_namer.py -v
```

Expected: `ERROR` — `ImportError: cannot import name 'SmartNamer'`

- [ ] **Step 3: Add `SmartNamer` class to `cbz_merger.py`**

Insert this class after `CBZMerger` (before `if __name__ == "__main__"`):

```python
class SmartNamer:
    """Suggests a merged output filename from a list of input file stems."""

    def suggest(self, stems: list, extension: str) -> str:
        if not stems:
            return f"Merged{extension}"
        if len(stems) == 1:
            return f"{stems[0]}{extension}"

        numbers = [self._last_number(s) for s in stems]
        if any(n is None for n in numbers):
            return f"{stems[0]}_Merged{extension}"

        prefixes = [self._prefix_before_last_number(s) for s in stems]
        common = self._common_prefix(prefixes).rstrip(" -_.")

        min_n, max_n = min(numbers), max(numbers)
        if min_n == max_n:
            return f"{stems[0]}{extension}"

        if common:
            return f"{common} {min_n}-{max_n}{extension}"
        return f"{min_n}-{max_n}{extension}"

    def _last_number(self, stem: str) -> Optional[int]:
        parts = re.split(r'(\d+)', stem)
        for part in reversed(parts):
            if part.isdigit():
                return int(part)
        return None

    def _prefix_before_last_number(self, stem: str) -> str:
        parts = re.split(r'(\d+)', stem)
        last_digit_idx = -1
        for i, p in enumerate(parts):
            if p.isdigit():
                last_digit_idx = i
        if last_digit_idx == -1:
            return stem
        return ''.join(parts[:last_digit_idx])

    def _common_prefix(self, strings: list) -> str:
        if not strings:
            return ''
        prefix = strings[0]
        for s in strings[1:]:
            while not s.startswith(prefix):
                prefix = prefix[:-1]
                if not prefix:
                    return ''
        return prefix
```

- [ ] **Step 4: Run tests — all should pass**

```
pytest tests/test_smart_namer.py -v
```

Expected: All 9 tests `PASSED`.

- [ ] **Step 5: Run all tests together to verify nothing broke**

```
pytest tests/ -v
```

Expected: All 18 tests `PASSED`.

- [ ] **Step 6: Commit**

```bash
git add cbz_merger.py tests/test_smart_namer.py
git commit -m "feat: add SmartNamer with TDD — auto-names merged output from filename range"
```

---

## Task 4: PyQt6 App Skeleton

**Files:**
- Modify: `cbz_merger.py` (add `MergeWorker`, `FileListWidget`, `MainWindow`, update `main()`)

Goal: running `python cbz_merger.py` opens a window. No merge functionality yet.

- [ ] **Step 1: Add imports to top of `cbz_merger.py`**

Replace the existing import block with:

```python
#!/usr/bin/env python3
"""
Yor CBZ Merger v3.0 — Comic Book Archive Merger Tool
Combines CBZ, CBR, ZIP, RAR files and image folders into a single CBZ or PDF.
Modern Clean UI · Light/Dark theme · PyQt6
"""

import os
import sys
import re
import zipfile
import tempfile
from pathlib import Path
from typing import Optional

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem, QLabel, QProgressBar,
    QTextEdit, QCheckBox, QFileDialog, QMessageBox, QSizePolicy, QFrame,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSettings, QMimeData
from PyQt6.QtGui import QColor, QFont, QDragEnterEvent, QDropEvent

try:
    import rarfile
    RAR_SUPPORT = True
except ImportError:
    RAR_SUPPORT = False

try:
    import img2pdf
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False
```

- [ ] **Step 2: Add QSS theme strings after the feature flags**

Add these two constants (insert before `class CBZMerger`):

```python
LIGHT_QSS = """
QMainWindow { background-color: #f8f9fa; }
QWidget { background-color: #f8f9fa; color: #212529; font-family: "Segoe UI", Arial, sans-serif; }
QWidget#header { background-color: #ffffff; border-bottom: 1px solid #e9ecef; }
QWidget#toolbar { background-color: #ffffff; border-bottom: 1px solid #e9ecef; }
QWidget#options_bar { background-color: #f8f9fa; border-bottom: 1px solid #e9ecef; }
QWidget#footer { background-color: #ffffff; border-top: 1px solid #e9ecef; }
QWidget#smart_bar { background-color: #fff9db; border: 1px solid #ffe066; border-radius: 6px; }
QListWidget { background-color: #ffffff; border: 1px solid #dee2e6; border-radius: 6px;
              font-size: 12px; color: #212529; }
QListWidget::item:selected { background-color: #e8f0fe; color: #0d6efd; }
QProgressBar { background-color: #e9ecef; border-radius: 3px; text-align: center; max-height: 6px; }
QProgressBar::chunk { background-color: #0d6efd; border-radius: 3px; }
QTextEdit { background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 6px;
            color: #495057; font-family: Consolas, monospace; font-size: 10px; }
QCheckBox { color: #495057; font-size: 11px; }
QLabel#subtext { color: #6c757d; font-size: 10px; }
QLabel#badge_on { background-color: #d1e7dd; color: #0f5132; padding: 2px 8px;
                  border-radius: 4px; font-size: 9px; font-weight: bold; }
QLabel#badge_off { background-color: #e9ecef; color: #6c757d; padding: 2px 8px;
                   border-radius: 4px; font-size: 9px; }
QPushButton#btn_primary { background-color: #0d6efd; color: white; border: none;
                          border-radius: 6px; padding: 5px 14px; font-weight: bold; }
QPushButton#btn_primary:hover { background-color: #0b5ed7; }
QPushButton#btn_folder { background-color: #6f42c1; color: white; border: none;
                         border-radius: 6px; padding: 5px 14px; font-weight: bold; }
QPushButton#btn_folder:hover { background-color: #5a32a3; }
QPushButton#btn_secondary { background-color: #f8f9fa; color: #495057;
                            border: 1px solid #dee2e6; border-radius: 6px; padding: 5px 12px; }
QPushButton#btn_secondary:hover { background-color: #e9ecef; }
QPushButton#btn_merge { background-color: #198754; color: white; border: none;
                        border-radius: 8px; padding: 10px 28px; font-size: 13px; font-weight: bold; }
QPushButton#btn_merge:hover { background-color: #157347; }
QPushButton#btn_merge:disabled { background-color: #adb5bd; color: #f8f9fa; }
QPushButton#btn_merge_pdf { background-color: #6f42c1; color: white; border: none;
                            border-radius: 8px; padding: 10px 28px; font-size: 13px; font-weight: bold; }
QPushButton#btn_merge_pdf:hover { background-color: #5a32a3; }
QPushButton#btn_merge_pdf:disabled { background-color: #adb5bd; color: #f8f9fa; }
"""

DARK_QSS = """
QMainWindow { background-color: #1e1e2e; }
QWidget { background-color: #1e1e2e; color: #cdd6f4; font-family: "Segoe UI", Arial, sans-serif; }
QWidget#header { background-color: #181825; border-bottom: 1px solid #313244; }
QWidget#toolbar { background-color: #181825; border-bottom: 1px solid #313244; }
QWidget#options_bar { background-color: #1e1e2e; border-bottom: 1px solid #313244; }
QWidget#footer { background-color: #181825; border-top: 1px solid #313244; }
QWidget#smart_bar { background-color: #2a2a1a; border: 1px solid #3d3d00; border-radius: 6px; }
QListWidget { background-color: #181825; border: 1px solid #313244; border-radius: 6px;
              font-size: 12px; color: #cdd6f4; }
QListWidget::item:selected { background-color: #313244; color: #89b4fa; }
QProgressBar { background-color: #313244; border-radius: 3px; text-align: center; max-height: 6px; }
QProgressBar::chunk { background-color: #89b4fa; border-radius: 3px; }
QTextEdit { background-color: #181825; border: 1px solid #313244; border-radius: 6px;
            color: #a6adc8; font-family: Consolas, monospace; font-size: 10px; }
QCheckBox { color: #cdd6f4; font-size: 11px; }
QLabel#subtext { color: #6c7086; font-size: 10px; }
QLabel#badge_on { background-color: #1a3a2a; color: #a6e3a1; padding: 2px 8px;
                  border-radius: 4px; font-size: 9px; font-weight: bold; }
QLabel#badge_off { background-color: #313244; color: #6c7086; padding: 2px 8px;
                   border-radius: 4px; font-size: 9px; }
QPushButton#btn_primary { background-color: #89b4fa; color: #1e1e2e; border: none;
                          border-radius: 6px; padding: 5px 14px; font-weight: bold; }
QPushButton#btn_primary:hover { background-color: #74c7ec; }
QPushButton#btn_folder { background-color: #cba6f7; color: #1e1e2e; border: none;
                         border-radius: 6px; padding: 5px 14px; font-weight: bold; }
QPushButton#btn_folder:hover { background-color: #f5c2e7; }
QPushButton#btn_secondary { background-color: #313244; color: #cdd6f4;
                            border: 1px solid #45475a; border-radius: 6px; padding: 5px 12px; }
QPushButton#btn_secondary:hover { background-color: #45475a; }
QPushButton#btn_merge { background-color: #a6e3a1; color: #1e1e2e; border: none;
                        border-radius: 8px; padding: 10px 28px; font-size: 13px; font-weight: bold; }
QPushButton#btn_merge:hover { background-color: #94e2d5; }
QPushButton#btn_merge:disabled { background-color: #45475a; color: #6c7086; }
QPushButton#btn_merge_pdf { background-color: #cba6f7; color: #1e1e2e; border: none;
                            border-radius: 8px; padding: 10px 28px; font-size: 13px; font-weight: bold; }
QPushButton#btn_merge_pdf:hover { background-color: #f5c2e7; }
QPushButton#btn_merge_pdf:disabled { background-color: #45475a; color: #6c7086; }
"""
```

- [ ] **Step 3: Add `MergeWorker` class after `SmartNamer`**

```python
class MergeWorker(QThread):
    """Runs CBZMerger.merge_archives in a background thread."""

    progress = pyqtSignal(float, str)   # (value 0–100, status text)
    log      = pyqtSignal(str)           # log line
    finished = pyqtSignal(bool)          # True = success

    def __init__(self, files: list, output_path: str, output_pdf: bool):
        super().__init__()
        self.files       = files
        self.output_path = output_path
        self.output_pdf  = output_pdf

    def run(self):
        merger = CBZMerger(
            progress_callback=self.progress.emit,
            log_callback=self.log.emit,
        )
        success = merger.merge_archives(self.files, self.output_path, self.output_pdf)
        self.finished.emit(success)
```

- [ ] **Step 4: Add `FileListWidget` class after `MergeWorker`**

```python
class FileListWidget(QWidget):
    """File list with native drag-and-drop and operation signals."""

    files_changed = pyqtSignal(list)  # emits current file list on every change

    def __init__(self, parent=None):
        super().__init__(parent)
        self._files: list[str] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        layout.addWidget(self.list_widget)

        self.setAcceptDrops(True)
        self._refresh_list()

    # ── Drag-and-drop ──────────────────────────────────────────────────────────

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.list_widget.setStyleSheet("QListWidget { border: 2px dashed #0d6efd; }")

    def dragLeaveEvent(self, event):
        self.list_widget.setStyleSheet("")

    def dropEvent(self, event: QDropEvent):
        self.list_widget.setStyleSheet("")
        paths = [url.toLocalFile() for url in event.mimeData().urls()]
        self.add_items(paths)
        event.acceptProposedAction()

    # ── Public API ─────────────────────────────────────────────────────────────

    def add_items(self, paths: list) -> int:
        merger = CBZMerger()
        added = 0
        for path in paths:
            if path in self._files:
                continue
            if os.path.isdir(path) and merger.is_image_folder(path):
                self._files.append(path)
                added += 1
            elif os.path.isfile(path) and Path(path).suffix.lower() in CBZMerger.SUPPORTED_EXTENSIONS:
                self._files.append(path)
                added += 1
        if added:
            self._files.sort(key=CBZMerger().natural_sort_key)
            self._refresh_list()
            self.files_changed.emit(self._files.copy())
        return added

    def remove_selected(self):
        rows = sorted({i.row() for i in self.list_widget.selectedIndexes()}, reverse=True)
        for row in rows:
            if row < len(self._files):
                del self._files[row]
        self._refresh_list()
        self.files_changed.emit(self._files.copy())

    def clear(self):
        self._files.clear()
        self._refresh_list()
        self.files_changed.emit(self._files.copy())

    def move_up(self):
        row = self.list_widget.currentRow()
        if 0 < row < len(self._files):
            self._files[row], self._files[row - 1] = self._files[row - 1], self._files[row]
            self._refresh_list()
            self.list_widget.setCurrentRow(row - 1)
            self.files_changed.emit(self._files.copy())

    def move_down(self):
        row = self.list_widget.currentRow()
        if 0 <= row < len(self._files) - 1:
            self._files[row], self._files[row + 1] = self._files[row + 1], self._files[row]
            self._refresh_list()
            self.list_widget.setCurrentRow(row + 1)
            self.files_changed.emit(self._files.copy())

    def get_files(self) -> list:
        return self._files.copy()

    # ── Private ────────────────────────────────────────────────────────────────

    def _refresh_list(self):
        self.list_widget.clear()
        if not self._files:
            item = QListWidgetItem("   Drop files or folders here\n   Supported: CBZ, CBR, ZIP, RAR, image folders")
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self.list_widget.addItem(item)
            return
        for i, filepath in enumerate(self._files):
            name = Path(filepath).name
            ext  = Path(filepath).suffix.lower()
            if os.path.isdir(filepath):
                label = f"  {i+1:02d}.  📁  {name}/"
            elif ext == ".cbz":
                label = f"  {i+1:02d}.  📘  {name}"
            elif ext == ".cbr":
                label = f"  {i+1:02d}.  📕  {name}"
            else:
                label = f"  {i+1:02d}.  📦  {name}"

            if os.path.isfile(filepath):
                size_mb = os.path.getsize(filepath) / (1024 * 1024)
                label += f"    {size_mb:.1f} MB"

            self.list_widget.addItem(QListWidgetItem(label))
```

- [ ] **Step 5: Add `MainWindow` skeleton and `main()` at the bottom of the file**

Replace the `if __name__ == "__main__":` block with:

```python
class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CBZ Merger")
        self.setMinimumSize(700, 600)
        self.resize(950, 750)

        self._dark = False
        self._settings  = QSettings("YorEdition", "CBZMerger")
        self._worker: Optional[MergeWorker] = None

        self._build_ui()
        self._load_settings()

    # ── UI Construction ────────────────────────────────────────────────────────

    def _build_ui(self):
        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._make_header())
        root.addWidget(self._make_toolbar())
        root.addWidget(self._make_options_bar())

        inner = QWidget()
        inner_layout = QVBoxLayout(inner)
        inner_layout.setContentsMargins(20, 12, 20, 12)
        inner_layout.setSpacing(8)

        self.file_list = FileListWidget()
        self.file_list.files_changed.connect(self._on_files_changed)
        inner_layout.addWidget(self.file_list, stretch=1)

        self.smart_bar = self._make_smart_bar()
        inner_layout.addWidget(self.smart_bar)

        inner_layout.addWidget(self._make_progress_area())
        inner_layout.addWidget(self._make_log_panel())

        root.addWidget(inner, stretch=1)
        root.addWidget(self._make_footer())

        self._on_files_changed([])   # set initial state

    def _make_header(self) -> QWidget:
        w = QWidget()
        w.setObjectName("header")
        w.setFixedHeight(56)
        h = QHBoxLayout(w)
        h.setContentsMargins(20, 0, 20, 0)

        icon = QLabel("📚")
        icon.setFont(QFont("Segoe UI Emoji", 22))
        h.addWidget(icon)

        titles = QVBoxLayout()
        title = QLabel("CBZ Merger")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        sub = QLabel("Combine comic archives & image folders")
        sub.setObjectName("subtext")
        titles.addWidget(title)
        titles.addWidget(sub)
        h.addLayout(titles)
        h.addStretch()

        for text, enabled in [("Drag & Drop", True), ("RAR", RAR_SUPPORT), ("PDF", PDF_SUPPORT)]:
            badge = QLabel(f"{'✓' if enabled else '○'} {text}")
            badge.setObjectName("badge_on" if enabled else "badge_off")
            h.addWidget(badge)

        h.addSpacing(12)
        self.theme_btn = QPushButton("🌙")
        self.theme_btn.setObjectName("btn_secondary")
        self.theme_btn.setFixedSize(34, 28)
        self.theme_btn.setToolTip("Toggle dark / light mode")
        self.theme_btn.clicked.connect(self._toggle_theme)
        h.addWidget(self.theme_btn)
        return w

    def _make_toolbar(self) -> QWidget:
        w = QWidget()
        w.setObjectName("toolbar")
        w.setFixedHeight(44)
        h = QHBoxLayout(w)
        h.setContentsMargins(20, 0, 20, 0)
        h.setSpacing(6)

        def btn(label, obj_name, slot):
            b = QPushButton(label)
            b.setObjectName(obj_name)
            b.clicked.connect(slot)
            return b

        h.addWidget(btn("＋ Add Files",  "btn_primary",   self._add_files))
        h.addWidget(btn("📁 Add Folder", "btn_folder",    self._add_folder))
        h.addWidget(btn("− Remove",      "btn_secondary", self.file_list.remove_selected))
        h.addWidget(btn("✕ Clear",       "btn_secondary", self.file_list.clear))
        h.addStretch()
        h.addWidget(btn("▲", "btn_secondary", self.file_list.move_up))
        h.addWidget(btn("▼", "btn_secondary", self.file_list.move_down))
        return w

    def _make_options_bar(self) -> QWidget:
        w = QWidget()
        w.setObjectName("options_bar")
        w.setFixedHeight(36)
        h = QHBoxLayout(w)
        h.setContentsMargins(20, 0, 20, 0)
        h.setSpacing(20)

        lbl = QLabel("Options")
        lbl.setObjectName("subtext")
        h.addWidget(lbl)

        self.auto_name_cb = QCheckBox("Auto-name with smart range")
        self.auto_name_cb.setChecked(True)
        self.auto_name_cb.stateChanged.connect(self._update_smart_bar)
        h.addWidget(self.auto_name_cb)

        self.pdf_cb = QCheckBox("Export as PDF")
        if not PDF_SUPPORT:
            self.pdf_cb.setEnabled(False)
            self.pdf_cb.setToolTip("Install 'img2pdf' to enable PDF export")
        self.pdf_cb.stateChanged.connect(self._on_pdf_toggled)
        h.addWidget(self.pdf_cb)

        h.addStretch()
        self.counter_lbl = QLabel("No items")
        self.counter_lbl.setObjectName("subtext")
        h.addWidget(self.counter_lbl)
        return w

    def _make_smart_bar(self) -> QWidget:
        w = QWidget()
        w.setObjectName("smart_bar")
        h = QHBoxLayout(w)
        h.setContentsMargins(12, 6, 12, 6)

        bulb = QLabel("💡")
        h.addWidget(bulb)

        h.addWidget(QLabel("Suggested filename:"))

        self.smart_name_lbl = QLabel("")
        self.smart_name_lbl.setFont(QFont("Consolas", 10, QFont.Weight.Bold))
        h.addWidget(self.smart_name_lbl)

        hint = QLabel("(editable at save)")
        hint.setObjectName("subtext")
        h.addWidget(hint)
        h.addStretch()

        w.setVisible(False)
        return w

    def _make_progress_area(self) -> QWidget:
        w = QWidget()
        h = QVBoxLayout(w)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(4)

        row = QHBoxLayout()
        self.status_lbl = QLabel("Ready")
        self.status_lbl.setObjectName("subtext")
        self.pct_lbl = QLabel("")
        self.pct_lbl.setObjectName("subtext")
        row.addWidget(self.status_lbl)
        row.addStretch()
        row.addWidget(self.pct_lbl)
        h.addLayout(row)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        h.addWidget(self.progress_bar)
        return w

    def _make_log_panel(self) -> QWidget:
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(4)

        row = QHBoxLayout()
        log_lbl = QLabel("Log")
        log_lbl.setObjectName("subtext")
        clear_btn = QPushButton("Clear")
        clear_btn.setObjectName("btn_secondary")
        clear_btn.setFixedHeight(22)
        clear_btn.clicked.connect(self._clear_log)
        row.addWidget(log_lbl)
        row.addStretch()
        row.addWidget(clear_btn)
        v.addLayout(row)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFixedHeight(110)
        v.addWidget(self.log_text)
        return w

    def _make_footer(self) -> QWidget:
        w = QWidget()
        w.setObjectName("footer")
        w.setFixedHeight(56)
        h = QHBoxLayout(w)
        h.setContentsMargins(20, 0, 20, 0)

        ver = QLabel("v3.0 · Yor Edition")
        ver.setObjectName("subtext")
        h.addWidget(ver)
        h.addStretch()

        self.merge_btn = QPushButton("🔀 Merge to CBZ")
        self.merge_btn.setObjectName("btn_merge")
        self.merge_btn.setFixedHeight(42)
        self.merge_btn.setMinimumWidth(180)
        self.merge_btn.clicked.connect(self._start_merge)
        h.addWidget(self.merge_btn)
        return w

    # ── Slots ──────────────────────────────────────────────────────────────────

    def _on_files_changed(self, files: list):
        count = len(files)
        if count == 0:
            self.counter_lbl.setText("No items")
        else:
            folders = sum(1 for f in files if os.path.isdir(f))
            items   = count - folders
            parts   = []
            if items:   parts.append(f"{items} file{'s' if items > 1 else ''}")
            if folders: parts.append(f"{folders} folder{'s' if folders > 1 else ''}")
            self.counter_lbl.setText(" • ".join(parts))
        self._update_smart_bar()

    def _update_smart_bar(self):
        files = self.file_list.get_files()
        show = self.auto_name_cb.isChecked() and len(files) >= 2
        self.smart_bar.setVisible(show)
        if show:
            ext = ".pdf" if self.pdf_cb.isChecked() else ".cbz"
            stems = [Path(f).stem for f in files]
            suggested = SmartNamer().suggest(stems, ext)
            self.smart_name_lbl.setText(suggested)

    def _on_pdf_toggled(self):
        is_pdf = self.pdf_cb.isChecked()
        if is_pdf:
            self.merge_btn.setText("🔀 Merge to PDF")
            self.merge_btn.setObjectName("btn_merge_pdf")
        else:
            self.merge_btn.setText("🔀 Merge to CBZ")
            self.merge_btn.setObjectName("btn_merge")
        self.merge_btn.setStyle(self.merge_btn.style())   # force QSS re-apply
        self._update_smart_bar()

    def _add_files(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Select Comic Book Archives", "",
            "Comic Archives (*.cbz *.cbr *.zip *.rar);;All Files (*.*)"
        )
        if paths:
            added = self.file_list.add_items(paths)
            self._append_log(f"➕ Added {added} file(s)")

    def _add_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Image Folder")
        if not folder:
            return
        if not CBZMerger().is_image_folder(folder):
            QMessageBox.warning(self, "No Images", f"No images found in:\n{Path(folder).name}")
            return
        added = self.file_list.add_items([folder])
        if added:
            self._append_log(f"📁 Added: {Path(folder).name}")
        else:
            self._append_log("⚠️ Folder already in list")

    def _append_log(self, text: str):
        self.log_text.append(text)

    def _clear_log(self):
        self.log_text.clear()

    def _on_progress(self, value: float, status: str):
        self.progress_bar.setValue(int(value))
        if status:
            self.status_lbl.setText(status)
        self.pct_lbl.setText(f"{int(value)}%" if value > 0 else "")

    def _start_merge(self):
        files = self.file_list.get_files()
        if not files:
            QMessageBox.warning(self, "No Files", "Add some files or folders first.")
            return

        is_pdf  = self.pdf_cb.isChecked()
        ext     = ".pdf" if is_pdf else ".cbz"
        fmt     = "PDF"  if is_pdf else "CBZ"

        if self.auto_name_cb.isChecked():
            stems = [Path(f).stem for f in files]
            default_name = SmartNamer().suggest(stems, ext)
        else:
            default_name = f"{Path(files[0]).stem}_Merged{ext}"

        output_path, _ = QFileDialog.getSaveFileName(
            self, f"Save Merged {fmt}", default_name,
            f"{fmt} Files (*{ext})"
        )
        if not output_path:
            return

        self.merge_btn.setEnabled(False)
        self._clear_log()
        self._on_progress(0, "Starting...")

        self._worker = MergeWorker(files, output_path, is_pdf)
        self._worker.progress.connect(self._on_progress)
        self._worker.log.connect(self._append_log)
        self._worker.finished.connect(self._on_merge_finished)
        self._worker.start()

    def _on_merge_finished(self, success: bool):
        self.merge_btn.setEnabled(True)
        if success:
            QMessageBox.information(self, "Success", "✅ Merge complete!")
            self._auto_clear()
        else:
            QMessageBox.critical(self, "Error", "Merge failed. Check the log for details.")

    def _auto_clear(self):
        self.file_list.clear()
        self._clear_log()
        self._on_progress(0, "Ready")
        self.status_lbl.setText("Ready")
        self.pct_lbl.setText("")

    # ── Theme ──────────────────────────────────────────────────────────────────

    def _toggle_theme(self):
        self._dark = not self._dark
        self._apply_theme()
        self._settings.setValue("dark_mode", self._dark)

    def _apply_theme(self):
        QApplication.instance().setStyleSheet(DARK_QSS if self._dark else LIGHT_QSS)
        self.theme_btn.setText("☀️" if self._dark else "🌙")

    def _load_settings(self):
        self._dark = self._settings.value("dark_mode", False, type=bool)
        self._apply_theme()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("CBZ Merger")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
```

- [ ] **Step 6: Run the app — window should open cleanly**

```
python cbz_merger.py
```

Expected: window opens, header visible, file list shows placeholder text, merge button visible.

- [ ] **Step 7: Verify tests still pass (no import regressions)**

```
pytest tests/ -v
```

Expected: All 18 tests `PASSED`.

- [ ] **Step 8: Commit**

```bash
git add cbz_merger.py
git commit -m "feat: complete PyQt6 rewrite — full UI with all panels and merge flow"
```

---

## Task 5: Build Script

**Files:**
- Create: `build.bat`

- [ ] **Step 1: Install PyInstaller**

```
pip install pyinstaller
```

- [ ] **Step 2: Create `build.bat`**

```bat
@echo off
echo Building CBZ-Merger.exe...
pyinstaller --onefile --windowed --name "CBZ-Merger" cbz_merger.py
echo.
if exist dist\CBZ-Merger.exe (
    echo Done! Output: dist\CBZ-Merger.exe
) else (
    echo Build failed — check output above.
)
pause
```

- [ ] **Step 3: Run build**

```
build.bat
```

Expected: `dist\CBZ-Merger.exe` created. Double-click to verify it opens.

- [ ] **Step 4: Add `.gitignore` entries**

Append to `.gitignore` (create it if it doesn't exist):

```
# PyInstaller
build/
dist/
*.spec

# Brainstorm sessions
.superpowers/

# Python
__pycache__/
*.pyc
.pytest_cache/
```

- [ ] **Step 5: Commit**

```bash
git add build.bat .gitignore
git commit -m "chore: add PyInstaller build script and gitignore"
```

---

## Task 6: Smoke Test Checklist

Run the app (`python cbz_merger.py`) and verify each item manually:

- [ ] Window opens at ~950×750, centered
- [ ] Header shows "CBZ Merger", badges show ✓/○ for Drag & Drop / RAR / PDF based on installed packages
- [ ] 🌙 toggle switches to dark mode, ☀️ switches back; reopening the app remembers the last choice
- [ ] "＋ Add Files" opens file dialog, adds archives to list with correct icon (📘/📕/📦)
- [ ] "📁 Add Folder" opens folder dialog; rejects folders with no images (shows warning)
- [ ] Adding the same file twice does not duplicate it
- [ ] Log shows `➕ Added N file(s)` after adding files
- [ ] ▲/▼ reorder selected item in the list
- [ ] "− Remove" removes selected items; "✕ Clear" clears all
- [ ] Smart name bar appears when ≥2 files are loaded and "Auto-name" is checked
- [ ] Smart name bar shows correct suggestion: e.g., files `A 1.cbz`, `A 2.cbz`, `A asdfasdf 3.cbz` → `A 1-3.cbz`
- [ ] Unchecking "Auto-name" hides the smart bar
- [ ] "Export as PDF" checkbox changes button to "Merge to PDF" (purple) and back
- [ ] Merge button opens Save dialog pre-filled with SmartNamer suggestion
- [ ] Merging 2–3 CBZ files produces a valid output CBZ that can be opened
- [ ] Progress bar advances during merge; log shows per-file status
- [ ] After successful merge: success dialog shown, then file list, log, and progress reset
- [ ] Drag-and-drop from file explorer onto the list adds supported files
- [ ] Unsupported dropped files (e.g., `.txt`) are silently ignored

- [ ] **Commit after all checks pass**

```bash
git add -A
git commit -m "test: all smoke tests passing — v3.0 overhaul complete"
```

---

## Self-Review Notes

- All 6 spec requirements covered: PyQt6 migration ✓, Modern Clean UI ✓, Light/Dark toggle ✓, SmartNamer ✓, Auto-clear ✓, Bug fixes ✓
- All 3 bug fixes addressed: `add_files` rewritten in `FileListWidget.add_items`, `extract_archive` trailing `return False` fixed, layout resize handled by PyQt6 natively
- `SmartNamer` and `CBZMerger` both have full unit test coverage before GUI code is written
- `MergeWorker` uses Qt signals — thread-safe, no `root.after()` equivalent needed
- `QSettings` persists dark/light preference across sessions
- `build.bat` references `cbz_merger.py` — must be run from project root
