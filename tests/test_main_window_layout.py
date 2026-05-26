import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication

from cbz_merger import MainWindow


def _app():
    return QApplication.instance() or QApplication([])


def test_footer_uses_full_width_surface_with_transparent_version_label():
    app = _app()
    window = MainWindow()

    footer = window.findChild(type(window.centralWidget()), "footer")
    version_label = window.findChild(type(window.counter_lbl), "version_label")

    assert footer is not None
    assert footer.minimumHeight() >= 64
    assert version_label is not None
    assert version_label.autoFillBackground() is False
