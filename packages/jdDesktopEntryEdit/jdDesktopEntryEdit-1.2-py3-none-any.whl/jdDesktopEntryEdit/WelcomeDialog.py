from PyQt6.QtWidgets import QDialog
from typing import TYPE_CHECKING
from PyQt6 import uic
import os


if TYPE_CHECKING:
    from .Environment import Environment


class WelcomeDialog(QDialog):
    def __init__(self, env: "Environment"):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "WelcomeDialog.ui"), self)

        self._env = env

        self.button_box.accepted.connect(self._ok_button_clicked)

    def _ok_button_clicked(self) -> None:
        self._env.settings.set("showWelcomeDialog", self.show_startup_check_box.isChecked())
        self._env.settings.save(os.path.join(self._env.data_dir, "settings.json"))

        self.close()

    def open_dialog(self) -> None:
        self.show_startup_check_box.setChecked(self._env.settings.get("showWelcomeDialog"))
        self.exec()