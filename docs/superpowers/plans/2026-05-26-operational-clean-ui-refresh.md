# Operational Clean UI Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refresh CBZ Merger to v2.1.0 with a cleaner operational UI focused on scan-friendly file rows, compact summary information, and restrained light/dark themes.

**Architecture:** Keep the current single-file PyQt6 app. `FileListWidget` owns row formatting and file metadata display; `MainWindow` owns layout composition and summary labels; QSS constants own visual styling. Core merge behavior stays unchanged.

**Tech Stack:** Python 3.10+, PyQt6, pytest, PyInstaller.

---

## File Map

| File | Action | Purpose |
|---|---|---|
| `cbz_merger.py` | Modify | Version bump, row formatting helper, summary strip labels, QSS refresh |
| `tests/test_file_list_widget.py` | Modify | TDD coverage for structured row labels and total count after remove/clear |
| `README.md` | Modify | Document v2.1.0 UI refresh and test count if changed |
| `CHANGELOG.md` | Modify | Add v2.1.0 release notes |
| `docs/superpowers/specs/2026-05-26-operational-clean-ui-refresh-design.md` | Modify | Mark implementation notes complete |

---

## Task 1: File Row Formatting

**Files:**
- Modify: `tests/test_file_list_widget.py`
- Modify: `cbz_merger.py`

- [x] **Step 1: Write failing tests**

Add tests that expect file rows to use structured separators and that remove/clear update total image count:

```python
def test_formats_file_rows_as_operational_metadata(tmp_path):
    app = _app()
    archive = tmp_path / "vol001.cbz"
    import zipfile
    with zipfile.ZipFile(archive, "w") as zf:
        zf.writestr("001.jpg", b"x")
        zf.writestr("002.png", b"x")

    widget = FileListWidget()
    widget.add_items([str(archive)])

    text = widget.list_widget.item(0).text()
    assert "01 | CBZ | vol001.cbz" in text
    assert "2 images" in text
    assert "MB" in text


def test_total_image_count_updates_after_remove_and_clear(tmp_path):
    app = _app()
    paths = []
    import zipfile
    for archive_name, image_names in [
        ("vol001.cbz", ["001.jpg", "002.jpg"]),
        ("vol002.cbz", ["003.jpg"]),
    ]:
        archive = tmp_path / archive_name
        with zipfile.ZipFile(archive, "w") as zf:
            for image_name in image_names:
                zf.writestr(image_name, b"x")
        paths.append(str(archive))

    widget = FileListWidget()
    widget.add_items(paths)
    widget.list_widget.setCurrentRow(0)
    widget.remove_selected()
    assert widget.total_image_count() == 1
    widget.clear()
    assert widget.total_image_count() == 0
```

- [x] **Step 2: Run tests and verify RED**

Run:

```bash
$env:QT_QPA_PLATFORM='offscreen'; pytest tests/test_file_list_widget.py::test_formats_file_rows_as_operational_metadata tests/test_file_list_widget.py::test_total_image_count_updates_after_remove_and_clear -v
```

Expected: first test fails because the row still uses the old icon-heavy blob format.

- [x] **Step 3: Implement row formatting helper**

In `FileListWidget`, add `_file_type_label`, `_image_count_label`, and `_format_row_label`. Update `_refresh_list()` to call the helper.

- [x] **Step 4: Run file-list tests and verify GREEN**

Run:

```bash
$env:QT_QPA_PLATFORM='offscreen'; pytest tests/test_file_list_widget.py -v
```

Expected: all file-list tests pass.

---

## Task 2: Summary Strip And Theme Refresh

**Files:**
- Modify: `cbz_merger.py`

- [x] **Step 1: Update summary strip labels**

Replace the smart bar wording with compact operational labels:

- `Suggested:`
- filename in strong monospace text
- `Total: N images`
- `Output: CBZ` or `Output: PDF`

- [x] **Step 2: Update options row summary**

Keep file/folder count and include known total images in the right-side summary label, for example:

```text
3 files · 552 images
```

- [x] **Step 3: Refresh QSS**

Update `LIGHT_QSS` and `DARK_QSS` toward neutral operational surfaces, clearer selected rows, compact row spacing, subdued smart strip, and a strong but not oversized merge button.

- [x] **Step 4: Compile check**

Run:

```bash
python -m py_compile cbz_merger.py
```

Expected: exit code 0.

---

## Task 3: Version, Docs, Build, Push

**Files:**
- Modify: `cbz_merger.py`
- Modify: `README.md`
- Modify: `CHANGELOG.md`
- Modify: `docs/superpowers/specs/2026-05-26-operational-clean-ui-refresh-design.md`

- [x] **Step 1: Bump version**

Set `__version__ = "2.1.0"` in `cbz_merger.py`.

- [x] **Step 2: Update docs**

Update README title/footer and feature text to mention Operational Clean UI. Add CHANGELOG `2.1.0`. Add implementation note to the UI refresh spec.

- [x] **Step 3: Full verification**

Run:

```bash
$env:QT_QPA_PLATFORM='offscreen'; pytest tests/ -v
python -m py_compile cbz_merger.py
```

Expected: all tests pass and compile exits 0.

- [x] **Step 4: Build exe**

Run:

```bash
python -m PyInstaller --onefile --windowed --name "CBZ-Merger" cbz_merger.py
```

Expected: build completes and updates `dist/CBZ-Merger.exe`.

- [x] **Step 5: Commit and push**

Stage only intended source, test, and doc files:

```bash
git add cbz_merger.py tests/test_file_list_widget.py README.md CHANGELOG.md docs/superpowers/specs/2026-05-26-operational-clean-ui-refresh-design.md docs/superpowers/plans/2026-05-26-operational-clean-ui-refresh.md
git commit -m "release: v2.1.0 operational clean UI"
git push origin main
```

Expected: `main` and `origin/main` point to the new commit.
