from PyQt6.QtCore import QCoreApplication
from PyQt6.QtWidgets import QDialog
from typing import TYPE_CHECKING
from PyQt6 import uic
import os


if TYPE_CHECKING:
    from .MainWindow import MainWindow


class ValidationDialog(QDialog):
    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "ValidationDialog.ui"), self)

        self._main_window = main_window

    def open_dialog(self):
        try:
            self.output_box.setPlainText(str(self._main_window.get_desktop_entry().get_validation_messages()))
        except FileNotFoundError:
            self.output_box.setPlainText(QCoreApplication.translate("ValidationDialog", "desktop-file-validate was not found"))

        self.exec()