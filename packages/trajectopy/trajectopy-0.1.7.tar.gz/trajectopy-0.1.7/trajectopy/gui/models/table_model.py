"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2023
mail@gtombrink.de
"""
import copy
import logging
from typing import Callable
from trajectopy.gui.models.entry import Entry
from PyQt6.QtCore import QAbstractTableModel, Qt, QVariant
from PyQt6.QtCore import pyqtSlot
from trajectopy.gui.requests.request import Request, RequestType

logger = logging.getLogger("root")


class BaseTableModel(QAbstractTableModel):
    def __init__(self, headers: list[str] | None = None):
        super().__init__()
        self.items: list[Entry] = []
        self._headers = [""] if headers is None else headers

    def rowCount(self, parent):
        return len(self.items)

    def columnCount(self, parent):
        return len(self._headers)

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self._headers[section]

    def data(self, index, role):
        if not self.items:
            return

        if role == Qt.ItemDataRole.DisplayRole:
            return self.items[index.row()].column[index.column()]

        return QVariant()

    def get(self, id: str) -> Entry:
        for item in self.items:
            if item.id == id:
                return item
    
    def set(self, id: str, entry: Entry) -> None:
        for i, item in enumerate(self.items):
            if item.id == id:
                self.items[i] = entry
                self.layoutChanged.emit()
                return

    def add(self, entry: Entry) -> None:
        self.items.append(entry)
        self.layoutChanged.emit()

    def remove(self, ids: list[str]) -> None:
        self.items = [item for item in self.items if item.id not in ids]
        self.layoutChanged.emit()


class RequestTableModel(BaseTableModel):
    def __init__(self, headers: list[str], REQUEST_MAPPING: dict[RequestType, Callable] = {}):
        super().__init__(headers)
        self.REQUEST_MAPPING = REQUEST_MAPPING
        self._request: Request | None = None

    def set_request(self, request: Request) -> None:
        self._request = request

    def get_request(self) -> Request | None:
        return self._request

    @pyqtSlot(Request)
    def handle_request(self, request: Request) -> None:
        self.set_request(request=request)
        func = self.REQUEST_MAPPING.get(request.type)
        if func is None:
            logger.error(f"Unable to handle request of type {request.type}")
            return
        func()
        logger.debug(f"{self.__class__.__name__}: Handled request of type {request.type}")

    def add_entries(self) -> None:
        for entry in self.get_request().selection.entries:
            self.add(entry)
        
    def update_selected_entries(self) -> None:
        for entry in self.get_request().selection.entries:
            self.set(entry.id, entry)

    def remove_selected_entries(self) -> None:
        """Remove selected entries"""
        self.remove([entry.id for entry in self.get_request().selection.entries])

    def copy_selected_entries(self) -> None:
        """Deep copy entries"""
        for entry in self.get_request().selection.entries:
            entry_copy = copy.deepcopy(entry)
            entry_copy.renew_id()
            self.add(entry_copy)

    def reset(self) -> None:
        self.items = []
        self.layoutChanged.emit()

    def sort_items(self) -> None:
        """Sorts the items so that their id order matches the desired order"""
        desired_order = self.get_request().selection
        present_ids = [item.id for item in self.items]
        if any(id not in present_ids for id in desired_order):
            raise ValueError("Desired order contains ids that are not present in the model.")

        self.items = [self.get(id) for id in desired_order]
        self.layoutChanged.emit()
