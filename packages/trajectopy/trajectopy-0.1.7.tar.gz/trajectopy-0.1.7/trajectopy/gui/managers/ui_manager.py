"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2023
mail@gtombrink.de
"""
import logging
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6 import QtWidgets
from trajectopy.gui.managers.manager import Manager
from trajectopy.gui.models.entry import AlignmentEntry
from trajectopy.gui.requests.file_request import FileRequest, FileRequestType
from trajectopy.gui.requests.result_model_request import ResultModelRequest, ResultModelRequestType
from trajectopy.gui.requests.session_request import SessionRequest, SessionRequestType
from trajectopy.gui.requests.trajectory_manager_request import TrajectoryManagerRequest, TrajectoryManagerRequestType
from trajectopy.gui.requests.ui_request import UIRequest, UIRequestType
from trajectopy.gui.util import browse_dir_dialog, read_file_dialog, save_file_dialog, show_msg_box
from trajectopy.gui.views.alignment_edit_window import AlignmentEditWindow
from trajectopy.gui.views.properties_window import PropertiesGUI
from trajectopy.gui.views.result_selection_window import AlignmentSelector
from trajectopy.gui.views.settings_window import SettingsGUI
from trajectopy.util.datahandling import merge_dicts


logger = logging.getLogger("root")


class UIManager(Manager):
    trajectory_manager_request = pyqtSignal(TrajectoryManagerRequest)
    result_model_request = pyqtSignal(ResultModelRequest)
    file_request = pyqtSignal(FileRequest)
    session_request = pyqtSignal(SessionRequest)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.REQUEST_MAPPING = {
            UIRequestType.EPSG_SELECTION: self.epsg_input,
            UIRequestType.GRID_SELECTION: self.grid_input,
            UIRequestType.ALIGNMENT_SELECTION: self.alignment_selection,
            UIRequestType.IMPORT_TRAJ: self.trajectory_import_dialog,
            UIRequestType.IMPORT_RES: self.result_import_dialog,
            UIRequestType.EXPORT_TRAJ: self.trajectory_export_dialog,
            UIRequestType.EXPORT_RES: self.result_export_dialog,
            UIRequestType.MESSAGE: self.message_box,
            UIRequestType.TRAJ_PROPERTIES: self.show_properties,
            UIRequestType.RES_PROPERTIES: self.show_properties,
            UIRequestType.TRAJ_SETTINGS: self.show_trajectory_settings,
            UIRequestType.CONFIRM_RESET: self.show_reset_question,
            UIRequestType.EXPORT_SESSION: self.session_export_dialog,
            UIRequestType.IMPORT_SESSION: self.session_import_dialog,
            UIRequestType.EDIT_ALIGNMENT: self.edit_alignment,
        }

    def get_request(self) -> UIRequest:
        return super().get_request()

    @pyqtSlot(UIRequest)
    def handle_request(self, ui_request: UIRequest) -> None:
        super().handle_request(ui_request)

    def message_box(self) -> None:
        show_msg_box(self.get_request().payload)

    def show_properties(self) -> None:
        property_window = PropertiesGUI(parent=self.parent(), num_cols=len(self.get_request().selection.entries) + 1)
        property_window.reset()
        merged_properties = merge_dicts(tuple(entry.property_dict for entry in self.get_request().selection.entries))
        property_window.add_from_dict(merged_properties)
        property_window.show()

    def show_trajectory_settings(self) -> None:
        settings_window = SettingsGUI(parent=self.parent(), trajectory_entry=self.get_request().selection.entries[0])
        settings_window.show()

    def alignment_selection(self) -> None:
        result_selection = AlignmentSelector(parent=self.parent(), alignments=self.get_request().selection.entries)
        result_selection.selection_made.connect(self.handle_alignment_selection)
        result_selection.show()

    @pyqtSlot(AlignmentEntry)
    def handle_alignment_selection(self, selected_alignment: AlignmentEntry) -> None:
        self.trajectory_manager_request.emit(
            TrajectoryManagerRequest(
                type=TrajectoryManagerRequestType.APPLY_ALIGNMENT,
                selection=self.get_request().payload,
                target=selected_alignment,
            )
        )

    def trajectory_import_dialog(self) -> None:
        if selected_files := read_file_dialog(None, file_filter="Trajectory Files (*.traj);;All Files (*.*)"):
            self.file_request.emit(FileRequest(type=FileRequestType.READ_TRAJ, file_list=selected_files))
        else:
            return

    def trajectory_export_dialog(self) -> None:
        if selected_file := save_file_dialog(None, file_filter="Trajectory File (*.traj)"):
            self.file_request.emit(
                FileRequest(
                    type=FileRequestType.WRITE_TRAJ, file_list=[selected_file], selection=self.get_request().selection
                )
            )
        else:
            return

    def result_export_dialog(self) -> None:
        if selected_file := save_file_dialog(None, file_filter="Result File (*.result)"):
            self.file_request.emit(
                FileRequest(
                    type=FileRequestType.WRITE_RES, file_list=[selected_file], selection=self.get_request().selection
                )
            )
        else:
            return

    def result_import_dialog(self) -> None:
        if selected_files := read_file_dialog(None, file_filter="Result Files (*.result);;All Files (*.*)"):
            self.file_request.emit(FileRequest(type=FileRequestType.READ_RES, file_list=selected_files))
        else:
            return

    def show_reset_question(self) -> None:
        reply = QtWidgets.QMessageBox.question(
            self.parent(),
            "Confirmation",
            "The current Session will be lost. Continue?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
        )

        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            self.session_request.emit(SessionRequest(type=SessionRequestType.NEW))

    def session_export_dialog(self) -> None:
        if selected_file := browse_dir_dialog(None):
            self.session_request.emit(SessionRequest(type=SessionRequestType.EXPORT, selection=selected_file))
        else:
            return

    def session_import_dialog(self) -> None:
        if selected_file := browse_dir_dialog(None):
            self.session_request.emit(SessionRequest(type=SessionRequestType.NEW, selection=selected_file))
            self.session_request.emit(SessionRequest(type=SessionRequestType.IMPORT, selection=selected_file))
        else:
            return

    def epsg_input(self) -> None:
        epsg, ok = QtWidgets.QInputDialog.getInt(None, "Please enter an EPSG code", "EPSG:")

        if not ok or epsg is None:
            return

        self.trajectory_manager_request.emit(
            TrajectoryManagerRequest(
                type=TrajectoryManagerRequestType.CHANGE_ESPG, selection=self.get_request().selection, target=epsg
            )
        )

    def grid_input(self) -> None:
        grid, ok = QtWidgets.QInputDialog.getDouble(
            None, "Please enter a grid size in seconds", "Grid size [s]:", min=0.0001, value=0.01, decimals=4
        )

        if not ok or grid is None:
            return

        self.trajectory_manager_request.emit(
            TrajectoryManagerRequest(
                type=TrajectoryManagerRequestType.INTERPOLATE_GRID, selection=self.get_request().selection, target=grid
            )
        )

    def edit_alignment(self) -> None:
        alignment = self.get_request().selection.entries[0]
        alignment_window = AlignmentEditWindow(parent=self.parent(), alignment_entry=alignment)
        alignment_window.update_signal.connect(lambda: self.result_model_request.emit(
            ResultModelRequest(type=ResultModelRequestType.UPDATE, selection=self.get_request().selection)
        ))
        alignment_window.show()
