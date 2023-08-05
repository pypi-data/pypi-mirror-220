"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2023
mail@gtombrink.de
"""
import logging
import os
from PyQt6.QtWidgets import QInputDialog
from PyQt6.QtCore import pyqtSignal
from trajectopy.gui.models.entry import ResultEntry, ResultType
from trajectopy.gui.models.selection import ResultSelection
from trajectopy.gui.models.table_model import RequestTableModel
from trajectopy.gui.requests.file_request import FileRequest, FileRequestType
from trajectopy.gui.requests.result_model_request import ResultModelRequestType
from trajectopy.gui.requests.ui_request import UIRequest, UIRequestType

logger = logging.getLogger("root")


class ResultTableModel(RequestTableModel):
    ui_request = pyqtSignal(UIRequest)
    file_request = pyqtSignal(FileRequest)

    def __init__(self):
        REQUEST_MAPPING = {
            ResultModelRequestType.ADD: self.add_entries,
            ResultModelRequestType.UPDATE: self.update_selected_entries,
            ResultModelRequestType.RENAME: self.rename_result,
            ResultModelRequestType.REMOVE: self.remove_selected_entries,
            ResultModelRequestType.PASS_ALIGNMENTS_TO_UI: self.pass_alignments_to_ui,
            ResultModelRequestType.RESET: self.reset,
            ResultModelRequestType.EXPORT_ALL: self.export_all,
            ResultModelRequestType.EDIT_ALIGNMENT: self.edit_alignment,
            ResultModelRequestType.COPY: self.copy_selected_entries,
            ResultModelRequestType.SORT: self.sort_items,
        }
        super().__init__(headers=["Name", "Type", "Process Time", "ID"], REQUEST_MAPPING=REQUEST_MAPPING)
        self.items: list[ResultEntry]

    def export_all(self) -> None:
        for item in self.items:
            filename = os.path.join(self.get_request().selection, f"{item.id}.result")
            self.file_request.emit(
                FileRequest(
                    type=FileRequestType.WRITE_RES, selection=ResultSelection(entries=[item]), file_list=[filename]
                )
            )
        self.write_result_order()

    def write_result_order(self):
        result_order_filename = os.path.join(self.get_request().selection, "result_order.txt")
        self.file_request.emit(
            FileRequest(
                type=FileRequestType.WRITE_LIST,
                selection=[item.id for item in self.items],
                file_list=[result_order_filename],
            )
        )

    def rename_result(self) -> None:
        selected_entry = self.get_request().selection.entries[0]
        input_name, ok = QInputDialog.getText(None, "Please enter a name", "Name:", text=selected_entry.name)
        if ok and input_name is not None:
            selected_entry.set_name(input_name)

        self.layoutChanged.emit()

    def get_results_by_type(self, type: ResultType) -> list[ResultEntry]:
        return [entry for entry in self.items if entry._result_type == type]

    def pass_alignments_to_ui(self) -> None:
        if alignment_entries := self.get_results_by_type(ResultType.ALIGNMENT):
            self.ui_request.emit(
                # selected trajectories get shifted to payload, available alignments use the selection slot
                UIRequest(
                    type=UIRequestType.ALIGNMENT_SELECTION,
                    selection=ResultSelection(entries=alignment_entries),
                    payload=self.get_request().selection,
                )
            )
        else:
            self.ui_request.emit(UIRequest(type=UIRequestType.MESSAGE, payload="No Alignments available!"))

    def edit_alignment(self) -> None:
        self.ui_request.emit(
            UIRequest(
                type=UIRequestType.EDIT_ALIGNMENT,
                selection=ResultSelection(entries=self.get_request().selection.entries),
            )
        )
