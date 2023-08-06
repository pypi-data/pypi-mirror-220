from PyQt6.QtWidgets import QTableWidget, QHeaderView, QListWidget, QComboBox, QWidget, QMessageBox
from typing import Optional, Any, TypeVar, TYPE_CHECKING
from PyQt6.QtCore import QObject, QCoreApplication
import importlib
import json
import sys
import os


if TYPE_CHECKING:
    import requests
else:
    try:
        import requests
    except ModuleNotFoundError:
        print("Optional module requests not found", file=sys.stderr)
        requests = None


def clear_table_widget(table: QTableWidget) -> None:
    """Removes all Rows from a QTableWidget"""
    while table.rowCount() > 0:
        table.removeRow(0)


def stretch_table_widget_colums_size(table: QTableWidget) -> None:
    """Stretch all Colums of a QTableWidget"""
    for i in range(table.columnCount()):
        table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)


def string_not_none(string: Optional[str]) -> str:
    if string is None:
        return ""
    else:
        return string


def none_if_empty_string(string: str, strip_spaces: bool) -> Optional[str]:
    if string.strip() == "":
        return None
    else:
        if strip_spaces:
            return string.strip()
        else:
            return string


def boolean_not_none(boolean: Optional[bool]) -> bool:
    if boolean is None:
        return False
    else:
        return boolean


def none_if_false(boolean: bool) -> Optional[bool]:
    if not boolean:
        return None
    else:
        return True


def read_json_file(path: str, default: Any) -> Any:
    """
    Tries to parse the given JSON file and prints a error if the file couldn't be parsed
    Returns default if the file is not found or couldn't be parsed
    """
    if os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except json.decoder.JSONDecodeError as e:
            print(
                f"Can't parse {os.path.basename(path)}: {e.msg}: line {e.lineno} column {e.colno} (char {e.pos})", file=sys.stderr)
            return default
        except Exception:
            print("Can't read " + os.path.basename(path), file=sys.stderr)
            return default
    else:
        return default


T = TypeVar("T")
def remove_duplicates_from_list(duplicated_list: list[T]) -> list[T]:
    new_list = []

    for i in duplicated_list:
        if i not in new_list:
            new_list.append(i)

    return new_list


def list_widget_contains_item(list_widget: QListWidget, text: str) -> bool:
    """Checks if a QListWidget contains a item with the given text"""
    for i in range(list_widget.count()):
        if list_widget.item(i).text() == text:
            return True
    return False


def select_combo_box_data(box: QComboBox, data: Any, default_index: int = 0):
    """Set the index to the item with the given data"""
    index = box.findData(data)
    if index == -1:
        box.setCurrentIndex(default_index)
    else:
        box.setCurrentIndex(index)


def get_sender_table_row(table: QTableWidget, column: int, sender: QObject) -> int:
    """Get the Row in a QTableWidget that contains the Button that was clicked"""
    for i in range(table.rowCount()):
        if table.cellWidget(i, column) == sender:
            return i


def get_logical_table_row_list(table: QTableWidget) -> list[int]:
    """Returns a List of the row indexes in the order they appear in the table"""
    index_list = []
    header = table.verticalHeader()
    for i in range(table.rowCount()):
        index_list.append(header.logicalIndex(i))
    return index_list


def check_optional_module(module: str, parent_window: Optional[QWidget] = None) -> bool:
        try:
            importlib.import_module(module)
            return True
        except ModuleNotFoundError:
            QMessageBox.critical(parent_window, QCoreApplication.translate("Functions", "{{module}} not installed").replace("{{module}}", module), QCoreApplication.translate("Functions", "Optional module {{module}} not found. It is required to use this Feature.").replace("{{module}}", module))
            return False


def get_requests_response(url: str, parent_window: Optional[QWidget] = None) -> Optional["requests.models.Response"]:
    if not check_optional_module("requests", parent_window):
        return

    try:
        r = requests.get(url)
    except requests.exceptions.MissingSchema:
        QMessageBox.critical(parent_window, QCoreApplication.translate("Functions", "Invalid URL"), QCoreApplication.translate("Functions", "The given URL is not valid"))
    except requests.exceptions.InvalidSchema:
        QMessageBox.critical(parent_window, QCoreApplication.translate("Functions", "Invalid Schema"), QCoreApplication.translate("Functions", "Only http and https are supported"))
    except requests.exceptions.ConnectionError:
        QMessageBox.critical(parent_window, QCoreApplication.translate("Functions", "Could not connect"), QCoreApplication.translate("Functions", "Could not connect to the Website"))
    except Exception:
        QMessageBox.critical(parent_window, QCoreApplication.translate("Functions", "Unknown Error"), QCoreApplication.translate("Functions", "An unknown Error happened while trying to conenct to the given URL"))
    else:
        if r.status_code != 200:
            QMessageBox.critical(parent_window, QCoreApplication.translate("Functions", "Could not get data"), QCoreApplication.translate("Functions", "Could not get data from the URL"))
        else:
            return r
