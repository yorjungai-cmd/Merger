# CBZ Merger — Full Overhaul Design Spec

**Date:** 2026-05-26
**Status:** Approved

---

## Revision Notes

### 2.0.3 — 2026-05-26

- File list rows show per-item image counts after file size.
- Smart filename bar shows total image count for the current merge list.
- Image counts are cached per path inside `FileListWidget` and refreshed when items are added or cleared.

### 2.0.2 — 2026-05-26

- File list now supports drag-and-drop reordering inside the list.
- Existing ▲/▼ reorder buttons remain available.
- External drag-and-drop for adding files and folders remains supported.

---

## Overview

Complete rewrite of `cbz_merger.py` from tkinter to PyQt6. Preserves all existing functionality, fixes 3 confirmed bugs, adds 2 new features, and establishes a Modern Clean UI with Light/Dark theme toggle. Output remains a single Python file distributable as source or compiled `.exe`.

---

## Goals

- Fix all known bugs in the current codebase
- Migrate UI framework from tkinter → PyQt6
- Modern Clean UI with Light/Dark toggle (Light default)
- Smart auto-naming: detect common prefix + number range from input filenames
- Auto-clear file list and log after successful merge
- Maintain single-file architecture (`cbz_merger.py`)
- Support both run-from-source and PyInstaller `.exe` distribution

---

## Architecture

### Single file: `cbz_merger.py`

Four classes with clear responsibilities:

#### `CBZMerger`
Core business logic — unchanged from current version except bug fixes.

- `extract_archive(archive_path, extract_to)` → bool
- `collect_images_by_subfolder(directory)` → List[tuple]
- `natural_sort_key(path)` → list
- `merge_archives(input_items, output_path, output_pdf)` → bool
- `is_supported_file(filepath)` → bool
- `is_image_file(filename)` → bool
- `is_image_folder(folderpath)` → bool

#### `SmartNamer` (new)
Analyzes input filenames to suggest a merged output filename.

- `suggest(stems: List[str], extension: str)` → str

See SmartNamer Algorithm section below.

#### `FileListWidget(QWidget)`
Encapsulates the file list area: QListWidget + drag-and-drop registration + visual feedback on drag enter/leave.

- `add_items(paths: List[str])`
- `remove_selected()`
- `clear()`
- `move_up()`
- `move_down()`
- Drag items within the list to reorder merge sequence
- Shows per-item image count and exposes total image count for the smart filename bar
- `get_files()` → List[str]

#### `MainWindow(QMainWindow)`
Top-level application window. Owns all UI panels, wires signals, runs merge in QThread.

---

## UI Layout

```
┌─────────────────────────────────────────────────────────┐
│ 📚 CBZ Merger   Combine comic archives    ✓DnD ✓RAR ✓PDF  🌙 │  ← Header
├─────────────────────────────────────────────────────────┤
│ [＋ Add Files] [📁 Add Folder] [− Remove] [✕ Clear]  [▲][▼] │  ← Toolbar
├─────────────────────────────────────────────────────────┤
│ Options  ☑ Auto-name smart range  ☐ Export as PDF  3 files │  ← Options bar
├─────────────────────────────────────────────────────────┤
│  01  📘  A 1.cbz                              12.4 MB   │  │
│  02  📕  A 2.cbr                               9.8 MB   │  │  ← FileListWidget
│  03  📦  A asdfasdf 3.cbz                     11.2 MB   │  │    (expandable)
├─────────────────────────────────────────────────────────┤
│ 💡 Suggested filename:  A 1-3.cbz  (แก้ไขได้ตอน save)      │  ← Smart name bar
├─────────────────────────────────────────────────────────┤
│ Extracting 2/3...                               65%     │  ← Progress
│ ████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░       │
├─────────────────────────────────────────────────────────┤
│ Log                                            [Clear]  │
│ 📚 Processing 3 item(s)...                              │  ← Log panel
│ 📘 [1/3] A 1.cbz  ✓ 48 images                          │
├─────────────────────────────────────────────────────────┤
│ v3.0 · Yor Edition                    [🔀 Merge to CBZ] │  ← Footer
└─────────────────────────────────────────────────────────┘
```

### Theme
- **Light (default):** white panels, `#0d6efd` accent, `#198754` merge button
- **Dark:** `#1e1e2e` base, `#cdd6f4` text, same accent colors
- Toggle: 🌙/☀️ button top-right — persists via `QSettings`

### File list colors (both themes)
| Type | Icon | Color |
|---|---|---|
| .cbz | 📘 | Blue |
| .cbr | 📕 | Red |
| .zip/.rar | 📦 | Orange |
| Folder | 📁 | Purple |

---

## Bug Fixes

### Bug 1 — `add_files` dead code and wrong count (`cbz_merger.py:811–818`)

**Current (broken):**
```python
added = sum(1 for f in files if f not in self.files and not self.files.append(f))  # inserts via side-effect
added = len([f for f in files if f not in self.files])  # always 0 — already inserted above
for f in files:                                           # dead code
    if f not in self.files:
        self.files.append(f)
self.log_message(f"➕ Added {len(files)} file(s)")       # wrong count
```

**Fix:** Single clean loop, track actual count.
```python
added = 0
for f in files:
    if f not in self.files:
        self.files.append(f)
        added += 1
if added:
    self.files.sort(key=self.natural_sort_key)
    self.refresh_listbox()
self.log_message(f"➕ Added {added} file(s)")
```

### Bug 2 — Unreachable `return False` in `extract_archive` (`cbz_merger.py:97`)

**Fix:** Remove the trailing `return False` after the try/except block. The except clause already returns False; the statement after the block is unreachable.

### Bug 3 — Wrong row gets `weight=1` in layout (`cbz_merger.py:383`)

**Fix:** Not applicable in PyQt6 — `QVBoxLayout` with `setStretch` on the `FileListWidget` handles resize correctly by design.

---

## New Features

### Feature 1 — SmartNamer

**Algorithm:**

```
Input stems: ["A 1", "A 2", "A asdfasdf 3"]

1. For each stem, split off the last numeric group:
   "A 1"          → prefix="A ",           number=1
   "A 2"          → prefix="A ",           number=2
   "A asdfasdf 3" → prefix="A asdfasdf ",  number=3

2. Find longest common prefix of all prefix strings:
   common("A ", "A ", "A asdfasdf ") → "A "

3. Strip trailing whitespace/separators:
   "A " → "A"

4. Collect numbers → min=1, max=3

5. Result: "A 1-3" + output_extension → "A 1-3.cbz"
```

**Edge cases:**
| Case | Output |
|---|---|
| Single file | Original stem + extension |
| No numbers in any name | `{first_stem}_Merged.cbz` |
| Non-sequential numbers (1, 3, 7) | `A 1-7.cbz` (min–max) |
| All same name | Original name (no range appended) |
| Empty common prefix | `1-3.cbz` |

**UI integration:**
- Smart name bar appears below the file list whenever ≥2 files are loaded and "Auto-name" is checked
- Bar shows: `💡 Suggested: A 1-3.cbz (แก้ไขได้ตอน save)`
- On save dialog open, `initialFile` is pre-filled with the suggestion; user can edit freely

### Feature 2 — Auto-clear after successful merge

After `merge_archives` returns `True` and the success dialog is dismissed:
1. Clear file list (`self.files = []`)
2. Clear log text
3. Reset progress bar to 0
4. Reset status label to "Ready"
5. Hide smart name bar (no files loaded)

---

## Dependencies

### `requirements.txt`
```
PyQt6>=6.6.0
rarfile>=4.0
img2pdf>=0.4.0
Pillow>=10.0.0
```

`rarfile`, `img2pdf`, and `Pillow` are optional — the app detects them at startup and disables the relevant UI controls if absent.

`tkinterdnd2` is no longer required (PyQt6 provides native drag-and-drop).

### Optional dependency detection pattern
```python
try:
    import rarfile
    RAR_SUPPORT = True
except ImportError:
    RAR_SUPPORT = False
```

Header badges show `✓ RAR` (green) or `○ RAR` (grey) accordingly.

---

## Build & Distribution

### Run from source
```bash
pip install -r requirements.txt
python cbz_merger.py
```

### Build `.exe` (`build.bat`)
```bat
@echo off
pyinstaller --onefile --windowed --name "CBZ-Merger" cbz_merger.py
echo Done. Find CBZ-Merger.exe in dist/
```
(หากต้องการ custom icon ให้เพิ่ม `--icon=icon.ico` หลัง `--windowed`)

PyInstaller bundles PyQt6, rarfile, img2pdf, and Pillow if installed. The `--windowed` flag suppresses the console window.

---

## Threading

Merge runs in a `QThread` subclass. Progress and log updates are emitted as Qt signals and connected to UI slots on the main thread — thread-safe by design, no `root.after()` equivalent needed.

```python
class MergeWorker(QThread):
    progress = pyqtSignal(float, str)
    log = pyqtSignal(str)
    finished = pyqtSignal(bool)

    def run(self):
        merger = CBZMerger(
            progress_callback=self.progress.emit,
            log_callback=self.log.emit,
        )
        success = merger.merge_archives(...)
        self.finished.emit(success)
```

---

## Out of Scope

- Thumbnail preview in file list
- ComicInfo.xml metadata support
- Batch output (multiple output files in one run)
- Cloud/network sources
