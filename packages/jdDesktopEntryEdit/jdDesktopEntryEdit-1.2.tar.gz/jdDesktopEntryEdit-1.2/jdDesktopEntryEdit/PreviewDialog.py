from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
from PyQt6.QtWidgets import QDialog, QApplication
import desktop_entry_lib
from PyQt6 import uic
import os
import re


class DesktopEntryHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):

        super(DesktopEntryHighlighter, self).__init__(parent)

        self._highlighting_rules: list[tuple[re.Pattern, QTextCharFormat]] = []

        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor("blue"))
        self._highlighting_rules.append((re.compile("^([A-z]|-)+(?==.)"), keywordFormat))

        sectionHeaderFormat = QTextCharFormat()
        sectionHeaderFormat.setForeground(QColor("darkorange"))
        self._highlighting_rules.append((re.compile(r"^\[.+\]"), sectionHeaderFormat))

        commentFormat = QTextCharFormat()
        commentFormat.setFontItalic(True)
        commentFormat.setForeground(QColor("green"))
        self._highlighting_rules.append((re.compile("#.*$"), commentFormat))

        #xmlElementFormat = QTextCharFormat()
        #xmlElementFormat.setForeground(QColor("#000070")) #blue
        #self._highlighting_rules.append((re.compile("<(.*?)[> ]"), xmlElementFormat))

        #single_line_comment_format = QTextCharFormat()
        #single_line_comment_format.setForeground(QColor("#a0a0a4")) # grey
        #self._highlighting_rules.append((re.compile("<!--[^\n]*-->"), single_line_comment_format))

        #self._value_format = QTextCharFormat()
        #self._value_format.setForeground(QColor("#e35e00")) #orange
        #self._value_regex = re.compile(r"(?<=\S=)[\"\'](.*?)[\"\']")

    def highlightBlock(self, text):
        for pattern, format in self._highlighting_rules:
            for i in pattern.finditer(text):
                self.setFormat(i.start(), i.end() - i.start(), format)

        #for i in self._value_regex.finditer(text):
        #    self.setFormat(i.start(), i.end() - i.start(), self._value_format)


class PreviewDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "PreviewDialog.ui"), self)

        self._highlighter = DesktopEntryHighlighter(self.preview_edit.document())

        self.copy_button.clicked.connect(lambda: QApplication.clipboard().setText(self.preview_edit.toPlainText()))
        self.close_button.clicked.connect(self.close)

    def open_preview(self, text: str) -> None:
        self.preview_edit.setPlainText(text)
        self.exec()
