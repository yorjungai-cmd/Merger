# Graph Report - .  (2026-05-26)

## Corpus Check
- Corpus is ~9,934 words - fits in a single context window. You may not need a graph.

## Summary
- 118 nodes · 242 edges · 7 communities (6 shown, 1 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 32 edges (avg confidence: 0.83)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Archive Processing Core|Archive Processing Core]]
- [[_COMMUNITY_UI Window & Controls|UI Window & Controls]]
- [[_COMMUNITY_Documentation & Docs|Documentation & Docs]]
- [[_COMMUNITY_SmartNamer Algorithm|SmartNamer Algorithm]]
- [[_COMMUNITY_File List Widget|File List Widget]]
- [[_COMMUNITY_App Entry & Threading|App Entry & Threading]]

## God Nodes (most connected - your core abstractions)
1. `CBZMerger` - 29 edges
2. `MainWindow` - 27 edges
3. `SmartNamer` - 17 edges
4. `CBZ Merger Overhaul Design Spec` - 16 edges
5. `FileListWidget` - 15 edges
6. `CBZ Merger README` - 10 edges
7. `CBZ Merger Overhaul Implementation Plan` - 10 edges
8. `CBZMerger Class` - 10 edges
9. `CBZ Merger v2.0 (PyQt6)` - 10 edges
10. `MainWindow(QMainWindow) Class` - 7 edges

## Surprising Connections (you probably didn't know these)
- `CBZ Merger Overhaul Implementation Plan` --references--> `CBZMerger Unit Tests (test_core.py)`  [EXTRACTED]
  docs/superpowers/plans/2026-05-26-cbz-merger-overhaul.md → tests/test_core.py
- `CBZ Merger Overhaul Implementation Plan` --references--> `SmartNamer Unit Tests (test_smart_namer.py)`  [EXTRACTED]
  docs/superpowers/plans/2026-05-26-cbz-merger-overhaul.md → tests/test_smart_namer.py
- `CBZMerger Class` --references--> `rarfile Dependency`  [INFERRED]
  cbz_merger.py → requirements.txt
- `CBZMerger Class` --references--> `img2pdf Dependency`  [INFERRED]
  cbz_merger.py → requirements.txt
- `CBZMerger Class` --references--> `Pillow Dependency`  [INFERRED]
  cbz_merger.py → requirements.txt

## Hyperedges (group relationships)
- **CBZ Merger Core Class Hierarchy** — class_cbzmerger, class_smartnamer, class_mergeworker, class_filelistwidget, class_mainwindow [EXTRACTED 1.00]
- **Optional Runtime Dependencies** — dep_rarfile, dep_img2pdf, dep_pillow [EXTRACTED 1.00]
- **v2.0 New Features** — class_smartnamer, feature_lightdark_theme, rationale_autoclear, class_mergeworker, class_filelistwidget [EXTRACTED 1.00]
- **Overhaul Design and Plan Documents** — spec_overhaul, plan_overhaul [INFERRED 0.95]
- **Unit Test Suite** — test_core, test_smartnamer, dep_pytest [EXTRACTED 1.00]

## Communities (7 total, 1 thin omitted)

### Community 0 - "Archive Processing Core"
Cohesion: 0.12
Nodes (16): CBZMerger, Core logic for merging comic book archives., Returns naturally-sorted list of archive files directly inside folderpath., test_collect_images_sorted_naturally(), test_extract_cbz_returns_true_and_extracts(), test_extract_missing_file_returns_false(), test_extract_unsupported_extension_returns_false(), test_find_archives_in_folder_empty_when_no_archives() (+8 more)

### Community 1 - "UI Window & Controls"
Cohesion: 0.15
Nodes (4): MainWindow, Main application window., QMainWindow, QWidget

### Community 2 - "Documentation & Docs"
Cohesion: 0.20
Nodes (26): build.bat PyInstaller Script, CBZ Merger Changelog, CBZMerger Class, FileListWidget(QWidget) Class, MainWindow(QMainWindow) Class, MergeWorker(QThread) Class, SmartNamer Class, img2pdf Dependency (+18 more)

### Community 3 - "SmartNamer Algorithm"
Cohesion: 0.22
Nodes (11): Suggests a merged output filename from a list of input file stems., SmartNamer, test_all_same_number_no_range(), test_empty_common_prefix_uses_numbers_only(), test_empty_list_returns_merged(), test_no_numbers_falls_back_to_merged_suffix(), test_non_sequential_numbers_use_min_max(), test_pdf_extension_preserved() (+3 more)

### Community 5 - "App Entry & Threading"
Cohesion: 0.29
Nodes (4): main(), MergeWorker, Runs CBZMerger.merge_archives in a background QThread., QThread

## Knowledge Gaps
- **1 isolated node(s):** `pytest Dependency`
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CBZMerger` connect `Archive Processing Core` to `File List Widget`, `App Entry & Threading`?**
  _High betweenness centrality (0.279) - this node is a cross-community bridge._
- **Why does `MainWindow` connect `UI Window & Controls` to `Archive Processing Core`, `App Entry & Threading`?**
  _High betweenness centrality (0.205) - this node is a cross-community bridge._
- **Why does `SmartNamer` connect `SmartNamer Algorithm` to `UI Window & Controls`, `App Entry & Threading`?**
  _High betweenness centrality (0.166) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `CBZMerger` (e.g. with `test_natural_sort_orders_numerically()` and `test_natural_sort_handles_no_digits()`) actually correct?**
  _`CBZMerger` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `SmartNamer` (e.g. with `test_range_from_typical_chapter_names()` and `test_single_file_uses_original_name()`) actually correct?**
  _`SmartNamer` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Core logic for merging comic book archives.`, `Returns naturally-sorted list of archive files directly inside folderpath.`, `Suggests a merged output filename from a list of input file stems.` to the rest of the system?**
  _9 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Archive Processing Core` be split into smaller, more focused modules?**
  _Cohesion score 0.1206896551724138 - nodes in this community are weakly interconnected._