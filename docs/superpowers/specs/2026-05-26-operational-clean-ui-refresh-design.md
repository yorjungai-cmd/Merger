# CBZ Merger — Operational Clean UI Refresh Design

**Date:** 2026-05-26
**Status:** Implemented
**Target Version:** 2.1.0

---

## Overview

Refresh the CBZ Merger interface toward an **Operational Clean UI**: a quiet, precise utility surface designed for repeated work with many comic archives. The app should feel more like a focused desktop tool than a decorative showcase. The existing PyQt6 single-file architecture remains in place.

This refresh does not change merge behavior. It reorganizes visual hierarchy, file-list readability, metadata presentation, and action placement around the workflows already present in v2.0.3.

---

## Implementation Notes

### 2.1.1 — 2026-05-26

- Footer version label now uses a transparent label surface over the full-width footer background.
- Footer height and vertical margins were increased to prevent the lower UI from looking cut off in light and dark themes.

### 2.1.0 — 2026-05-26

- Implemented structured text rows in `FileListWidget`: `index | type | filename | images | size`.
- Reworked the smart summary strip to show suggested filename, total images, and output type.
- Added total image count to the options row summary.
- Refreshed light and dark QSS toward neutral operational surfaces.
- Preserved existing merge logic, drag reorder behavior, and external drag/drop.

---

## Goals

- Make the file list easier to scan when many files are loaded.
- Keep drag-and-drop adding and drag reorder behavior.
- Preserve light/dark theme support, but make both themes feel more consistent.
- Make metadata obvious: file type, filename, image count, and file size.
- Make the suggested output area a compact summary strip.
- Keep the merge button as the strongest action without making it oversized.
- Avoid marketing-style UI, large decorative panels, and nested card layouts.

---

## Non-Goals

- No thumbnail previews.
- No multi-window redesign.
- No new merge formats.
- No metadata editing, ComicInfo.xml, or batch output.
- No migration away from the current single-file PyQt6 application.

---

## Visual Direction

The visual style should be restrained and work-focused:

- Neutral surfaces with clear separators.
- Compact controls with predictable spacing.
- Rounded corners no larger than the current 6-8px range.
- Color used for status and action priority, not decoration.
- No gradient-orb backgrounds, hero sections, or large ornamental artwork.
- Typography should be modest: small labels, clear file rows, and a single strong merge action.

The UI should still feel polished, but the polish should come from alignment, spacing, contrast, and state clarity.

---

## Layout

### Header

Purpose: identify the app and environment.

Contents:
- App name and version.
- Short utility subtitle.
- Runtime badges: Drag & Drop, RAR, PDF.
- Theme toggle.

Design:
- Keep height compact.
- Avoid large icon emphasis.
- Keep badges readable but secondary.

### Toolbar

Purpose: file-list actions.

Contents:
- Add Files
- Add Folder
- Remove
- Clear
- Move Up
- Move Down

Design:
- Keep all action controls in one row.
- Primary file-ingest actions should be visually stronger than remove/clear/reorder.
- Reorder buttons remain available even though drag reorder is the preferred path.

### Options Row

Purpose: merge options and quick summary.

Contents:
- Auto-name with smart range.
- Export as PDF.
- Current file/folder count.
- Current total image count when known.

Design:
- Keep this row compact and informational.
- Do not duplicate the full suggested filename here.

### File List

Purpose: main work surface.

Each row should read like structured data:

```text
01 | [type] | Filename.ext                         | 184 images | 72.6 MB
```

Behavior:
- Preserve native drag reorder.
- Preserve external drag/drop to add supported files and folders.
- Preserve duplicate prevention.
- Preserve natural sorting on add.

Design:
- Move away from a single text blob per row where possible.
- If still using `QListWidgetItem` text for implementation simplicity, format consistently with stable spacing.
- Show type with a compact icon or short badge.
- Show image count and file size as metadata.
- Selected row must be obvious in light and dark themes.
- Drag target/drop indicator must be visible.
- Placeholder row remains non-selectable.

### Suggested Summary Strip

Purpose: confirm what will be created before the user clicks merge.

Contents:

```text
Suggested: [Nishikida Keishi] GRAPARA! (1-3).cbz     Total: 552 images     Output: CBZ
```

Design:
- Less visually loud than the current yellow strip.
- Clear enough to scan.
- Filename should remain the strongest text in the strip.
- Total image count and output type should be secondary metadata.

### Progress And Log

Purpose: operational feedback.

Design:
- Progress/status should sit above log.
- Log should be compact and secondary.
- The log should not compete with the file list as the main surface.

### Footer

Purpose: version identity and final action.

Contents:
- Version/author on the left.
- Merge button on the right.

Design:
- Merge button remains the dominant call to action.
- Button size should be strong but not oversized.
- Button text switches between Merge to CBZ and Merge to PDF.

---

## Theme Requirements

### Light Theme

- White or near-white content surfaces.
- Soft gray separators.
- Blue primary action.
- Green merge action for CBZ.
- Purple merge action for PDF.

### Dark Theme

- Dark neutral surfaces with enough contrast for long sessions.
- Avoid an overly purple one-note palette.
- Keep selected rows and drag states readable.
- Use the same semantic colors as light theme where practical.

---

## Architecture

Keep the current single-file architecture:

- `LIGHT_QSS` and `DARK_QSS` remain the theme surfaces.
- `FileListWidget` owns file-row rendering and drag/reorder behavior.
- `MainWindow` owns layout composition and smart-summary updates.
- `CBZMerger`, `SmartNamer`, and `MergeWorker` behavior should stay unchanged except where UI display requires a helper.

Implementation should prefer small private helpers over a large rewrite:

- `FileListWidget._format_row_label(path, index)` for row text if using text rows.
- `MainWindow._update_summary_labels()` or equivalent if smart-bar logic grows.
- Keep tests focused on behavior and generated labels, not pixel-perfect styling.

---

## Testing

Automated tests should cover:

- Existing merge and SmartNamer tests remain green.
- File list still syncs order after internal drag reorder.
- File list still shows image count metadata.
- Summary strip total remains correct after add/remove/clear/reorder.

Manual smoke tests should cover:

- Light and dark theme readability.
- Add files.
- Add folder containing archives.
- Add image folder.
- Drag reorder.
- Remove and clear.
- Toggle PDF output.
- Smart filename summary.
- Successful CBZ build.

---

## Release Requirements

When implemented:

- Bump app and docs version to `2.1.0`.
- Update `README.md`.
- Update `CHANGELOG.md`.
- Update this spec if the final implementation differs.
- Run full tests.
- Build `dist/CBZ-Merger.exe`.
- Commit and push.

---

## Approval Notes

The chosen direction is **Operational Clean UI**: restrained, work-focused, and optimized for scanning and repeated use.
