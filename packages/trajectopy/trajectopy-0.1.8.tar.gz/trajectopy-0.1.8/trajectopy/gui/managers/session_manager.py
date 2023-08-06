"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2023
mail@gtombrink.de
"""
import glob
import logging
import os
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from trajectopy.gui.managers.manager import Manager
from trajectopy.gui.requests.file_request import FileRequest, FileRequestType
from trajectopy.gui.requests.plot_settings_request import PlotSettingsRequest, PlotSettingsRequestType
from trajectopy.gui.requests.session_request import SessionRequest, SessionRequestType
from trajectopy.gui.requests.result_model_request import ResultModelRequest, ResultModelRequestType
from trajectopy.gui.requests.trajectory_model_request import TrajectoryModelRequest, TrajectoryModelRequestType


logger = logging.getLogger("root")


class SessionManager(Manager):
    trajectory_model_request = pyqtSignal(TrajectoryModelRequest)
    result_model_request = pyqtSignal(ResultModelRequest)
    plot_settings_request = pyqtSignal(PlotSettingsRequest)
    file_request = pyqtSignal(FileRequest)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.REQUEST_MAPPING = {
            SessionRequestType.NEW: self.new_session,
            SessionRequestType.EXPORT: self.export_session,
            SessionRequestType.IMPORT: self.import_session,
        }
        self._session_request: SessionRequest = None

    def get_request(self) -> SessionRequest:
        return super().get_request()

    @pyqtSlot(SessionRequest)
    def handle_request(self, session_request: SessionRequest) -> None:
        super().handle_request(session_request)

    def new_session(self) -> None:
        self.trajectory_model_request.emit(TrajectoryModelRequest(type=TrajectoryModelRequestType.RESET))
        self.result_model_request.emit(ResultModelRequest(type=ResultModelRequestType.RESET))
        self.plot_settings_request.emit(PlotSettingsRequest(type=PlotSettingsRequestType.RESET))
        logger.info("Cleared application and started a new session.")

    def import_session(self) -> None:
        session_request = self.get_request()

        traj_file_list = glob.glob(os.path.join(session_request.selection, "*.traj"))
        result_file_list = glob.glob(os.path.join(session_request.selection, "*.result"))

        self.file_request.emit(FileRequest(type=FileRequestType.READ_TRAJ, file_list=traj_file_list))
        self.file_request.emit(FileRequest(type=FileRequestType.READ_RES, file_list=result_file_list))

        self.file_request.emit(
            FileRequest(
                type=FileRequestType.READ_TRAJ_ORDER,
                file_list=[os.path.join(session_request.selection, "trajectory_order.txt")],
            )
        )

        self.file_request.emit(
            FileRequest(
                type=FileRequestType.READ_RES_ORDER,
                file_list=[os.path.join(session_request.selection, "result_order.txt")],
            )
        )

        self.plot_settings_request.emit(
            PlotSettingsRequest(type=PlotSettingsRequestType.IMPORT_FROM_SESSION, selection=session_request.selection)
        )

    def export_session(self) -> None:
        session_request = self.get_request()
        os.makedirs(session_request.selection, exist_ok=True)
        self.trajectory_model_request.emit(
            TrajectoryModelRequest(type=TrajectoryModelRequestType.EXPORT_ALL, selection=session_request.selection)
        )
        self.result_model_request.emit(
            ResultModelRequest(type=ResultModelRequestType.EXPORT_ALL, selection=session_request.selection)
        )
        self.plot_settings_request.emit(
            PlotSettingsRequest(type=PlotSettingsRequestType.EXPORT_TO_SESSION, selection=session_request.selection)
        )
