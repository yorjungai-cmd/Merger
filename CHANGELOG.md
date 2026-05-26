# Changelog

All notable changes to CBZ Merger are documented here.

---

## [2.1.1] — 2026-05-26

### Fixed

- **Footer surface clipping** — version text in the lower footer now sits on a full-width footer surface in both light and dark themes instead of appearing inside a cut-off block.

### Changed

- Program and documentation version bumped to `2.1.1`.

---

## [2.1.0] — 2026-05-26

### Added

- **Operational Clean UI refresh** — file rows now use a structured metadata layout for type, filename, image count, and file size.
- **Compact output summary** — suggested filename, total image count, and output type now appear in a quieter summary strip.
- **Options summary** — the options row now includes total image count when known.

### Changed

- Light and dark themes now use more neutral operational surfaces, clearer separators, and stronger selected-row states.
- Merge buttons are still dominant but slightly more compact.
- Program and documentation version bumped to `2.1.0`.

---

## [2.0.3] — 2026-05-26

### Added

- **Per-item image counts** — each file list row now shows the number of images inside the archive or folder after the file size.
- **Merged total image count** — the smart filename bar now shows the total number of images that will be included after merging the current list.

### Changed

- Program and documentation version bumped to `2.0.3`.

---

## [2.0.2] — 2026-05-26

### Added

- **Drag reorder in file list** — files can now be reordered directly by dragging items in the list, while the existing ▲/▼ buttons remain available.

### Changed

- Program and documentation version bumped to `2.0.2`.

---

## [2.0.0] — 2026-05-26

### Overview

Complete rewrite from tkinter to PyQt6. New UI framework, new features, bug fixes, and unit tests.

### Added

- **PyQt6 UI** — replaced tkinter with PyQt6 for better widgets, native drag-and-drop, and proper layout resizing
- **Light / Dark theme** — toggle button (🌙/☀️) in header, preference persisted via `QSettings`
- **Smart auto-naming** (`SmartNamer`) — analyzes input filenames to suggest a merged output name with number range (e.g. `A 1-3.cbz`)
- **Auto-clear after merge** — file list, log, and progress bar reset automatically after a successful merge
- **Add Folder → archives** — "Add Folder" now accepts folders containing .cbz/.zip/.cbr/.rar files (enumerates and adds each archive individually)
- **File size display** — each file in the list shows its size in MB
- **Smart name bar** — preview panel showing suggested output filename, visible whenever ≥ 2 files are loaded with Auto-name enabled
- **`MergeWorker(QThread)`** — merge runs in a background thread via Qt signals; UI never freezes
- **`FileListWidget(QWidget)`** — dedicated widget with native drag-and-drop support
- **`requirements.txt`** — pinned dependency list
- **`build.bat`** — one-line PyInstaller build script for `.exe` output
- **22 unit tests** — `CBZMerger` core (13 tests) and `SmartNamer` (9 tests)

### Fixed

- **`add_files` counting bug** — previous version used side-effect trick (`not list.append(f)`) that made the added count always 0 and added dead duplicate-checking code
- **`extract_archive` unreachable code** — old version had a `return False` after the try/except block that was never reached; fixed to single clean catch-all
- **Layout resize bug** — tkinter `grid_rowconfigure(5, weight=1)` was set on the wrong row (progress bar instead of file list); resolved naturally by switching to PyQt6 layouts
- **Unsupported archive format** — now logs a warning instead of silently returning False
- **`natural_sort_key` duplication** — previously defined in both core class and GUI class; now only in `CBZMerger`

### Changed

- Window title: `Yor CBZ Merger` → `CBZ Merger 2.0`
- Footer label: `v3.0 · Yor Edition` → `v2.0 · Crafted by Yor Anupong`
- `tkinterdnd2` no longer required (PyQt6 has native drag-and-drop)
- "Add Folder" dialog title changed to "Select Folder" (accepts both archive and image folders)
- Warning message when folder contains neither archives nor images: `"No supported archives or images found"`

---

## [1.0.0] — 2025 (original)

Initial release. Single-file tkinter application with Catppuccin Mocha dark theme.

### Features
- Merge CBZ, CBR, ZIP, RAR archives and image folders into a single CBZ
- Optional PDF export via `img2pdf`
- Optional drag & drop via `tkinterdnd2`
- Natural sort ordering
- Progress bar and log panel
- File list management (add, remove, reorder, clear)
