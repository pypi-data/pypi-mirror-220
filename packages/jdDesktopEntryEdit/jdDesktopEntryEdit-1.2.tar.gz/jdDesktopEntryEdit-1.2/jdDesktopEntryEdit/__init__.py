from PyQt6.QtCore import QTranslator, QLibraryInfo, QLocale
from PyQt6.QtWidgets import QApplication
from .Environment import Environment
from .MainWindow import MainWindow
import argparse
import sys
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?", help="The path to a file")
    args = parser.parse_known_args()[0]

    app = QApplication(sys.argv)

    env = Environment()

    app.setDesktopFileName("page.codeberg.JakobDev.jdDesktopEntryEdit.desktop")
    app.setApplicationName("jdDesktopEntryEdit")
    app.setWindowIcon(env.icon)

    app_translator = QTranslator()
    qt_translator = QTranslator()
    app_trans_dir = os.path.join(env.program_dir, "translations")
    qt_trans_dir = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
    language = env.settings.get("language")
    if language == "default":
        system_language = QLocale.system().name()
        app_translator.load(os.path.join(app_trans_dir, "jdDesktopEntryEdit_" + system_language.split("_")[0] + ".qm"))
        app_translator.load(os.path.join(app_trans_dir, "jdDesktopEntryEdit_" + system_language + ".qm"))
        qt_translator.load(os.path.join(qt_trans_dir, "qt_" + system_language.split("_")[0] + ".qm"))
        qt_translator.load(os.path.join(qt_trans_dir, "qt_" + system_language + ".qm"))
    elif language == "en":
        pass
    else:
        app_translator.load(os.path.join(app_trans_dir, "jdDesktopEntryEdit_" + language + ".qm"))
        qt_translator.load(os.path.join(qt_trans_dir, "qt_" + language.split("_")[0] + ".qm"))
        qt_translator.load(os.path.join(qt_trans_dir, "qt_" + language + ".qm"))
    app.installTranslator(app_translator)
    app.installTranslator(qt_translator)

    w = MainWindow(env)
    w.show()
    w.startup()

    if args.file:
        w.open_file(os.path.abspath(args.file))

    sys.exit(app.exec())
