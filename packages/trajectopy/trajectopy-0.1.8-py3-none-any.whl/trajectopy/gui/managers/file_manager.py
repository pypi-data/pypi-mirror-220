"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2023
mail@gtombrink.de
"""
import logging
from pathlib import Path
from typing import Tuple
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from trajectopy.gui.managers.manager import Manager

from trajectopy.gui.models.entry import ResultEntry, TrajectoryEntry
from trajectopy.gui.models.selection import ResultSelection, TrajectorySelection
from trajectopy.gui.requests.file_request import FileRequest, FileRequestType
from trajectopy.gui.requests.result_model_request import ResultModelRequest, ResultModelRequestType
from trajectopy.gui.requests.trajectory_model_request import TrajectoryModelRequest, TrajectoryModelRequestType
from trajectopy.gui.util import show_progress

logger = logging.getLogger("root")


class FileManager(Manager):
    trajectory_model_request = pyqtSignal(TrajectoryModelRequest)
    result_model_request = pyqtSignal(ResultModelRequest)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.REQUEST_MAPPING = {
            FileRequestType.READ_TRAJ: self.read_trajectory_files,
            FileRequestType.WRITE_TRAJ: self.write_trajectory,
            FileRequestType.READ_RES: self.read_result_files,
            FileRequestType.WRITE_RES: self.write_result,
            FileRequestType.READ_RES_ORDER: self.read_res_order,
            FileRequestType.READ_TRAJ_ORDER: self.read_traj_order,
            FileRequestType.WRITE_LIST: self.write_list,
        }

    def get_request(self) -> FileRequest:
        return super().get_request()

    @show_progress
    @pyqtSlot(FileRequest)
    def handle_request(self, file_request: FileRequest) -> None:
        super().handle_request(file_request)

    def read_trajectory_files(self) -> None:
        for file in self.get_request().file_list:
            logger.info(f"Reading file: {file}")
            trajectory_file, settings_file = self._get_traj_filenames(file)

            traj_entry = TrajectoryEntry.from_file(
                trajectory_filename=trajectory_file, settings_filename=settings_file
            )

            self.trajectory_model_request.emit(
                TrajectoryModelRequest(
                    type=TrajectoryModelRequestType.ADD,
                    selection=TrajectorySelection(entries=[traj_entry]),
                )
            )

    @staticmethod
    def _get_traj_filenames(file: str) -> Tuple[Path, Path]:
        file_path = Path(file)
        file_name = file_path.stem
        file_directory = file_path.parent
        settings_file = file_directory / f"{file_name}.yaml"
        return Path(file), Path(settings_file)

    def write_trajectory(self) -> None:
        trajectory_entry = self.get_request().selection.entries[0]
        trajectory_entry.to_file(self.get_request().file_list[0])

    def read_result_files(self) -> None:
        for file in self.get_request().file_list:
            logger.info(f"Reading file: {file}")
            result_entry = ResultEntry.from_file(filename=file)

            self.result_model_request.emit(
                ResultModelRequest(type=ResultModelRequestType.ADD, selection=ResultSelection(entries=[result_entry]))
            )

    def write_result(self) -> None:
        result_entry = self.get_request().selection.entries[0]
        result_entry.to_file(self.get_request().file_list[0])

    def write_list(self) -> None:
        with open(self.get_request().file_list[0], "w") as f:
            f.write("\n".join(self.get_request().selection))
            f.write("\n")

    def read_list(self) -> None | list[str]:
        if not Path(self.get_request().file_list[0]).is_file():
            logger.warning("No order file found.")
            return

        with open(self.get_request().file_list[0], "r") as f:
            file_list = [line.strip() for line in f.readlines()]
        return file_list

    def read_res_order(self) -> None:
        if id_list := self.read_list():
            self.result_model_request.emit(ResultModelRequest(type=ResultModelRequestType.SORT, selection=id_list))

    def read_traj_order(self) -> None:
        if id_list := self.read_list():
            self.trajectory_model_request.emit(
                TrajectoryModelRequest(type=TrajectoryModelRequestType.SORT, selection=id_list)
            )
