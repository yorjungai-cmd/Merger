import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication

from cbz_merger import FileListWidget


def _app():
    return QApplication.instance() or QApplication([])


def test_syncs_file_order_after_internal_list_reorder(tmp_path):
    app = _app()
    paths = []
    for name in ["vol001.cbz", "vol002.cbz", "vol003.cbz"]:
        path = tmp_path / name
        path.write_bytes(b"fake")
        paths.append(str(path))

    widget = FileListWidget()
    widget.add_items(paths)

    moved = widget.list_widget.takeItem(2)
    widget.list_widget.insertItem(0, moved)
    widget._sync_files_from_list()

    assert widget.get_files() == [paths[2], paths[0], paths[1]]
