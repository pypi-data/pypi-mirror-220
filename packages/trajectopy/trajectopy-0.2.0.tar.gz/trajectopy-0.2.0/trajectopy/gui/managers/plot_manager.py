"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2023
mail@gtombrink.de
"""
import logging
from trajectopy.gui.managers.manager import Manager
from trajectopy.gui.models.entry import AbsoluteDeviationEntry
from trajectopy.gui.requests.plot_requests import PlotRequest, PlotRequestType
from trajectopy.gui.requests.ui_request import UIRequest, UIRequestType
from trajectopy.settings.plot_settings import PlotSettings

from trajectopy.plotting.plot_tabs import PlotTabs
from PyQt6.QtCore import pyqtSlot

logger = logging.getLogger("root")


class PlotManager(Manager):
    def __init__(self, parent) -> None:
        super().__init__(parent=parent)
        self.plot_settings = PlotSettings()
        self.REQUEST_MAPPING = {
            PlotRequestType.TRAJECTORIES: self.plot_selected_trajectories,
            PlotRequestType.SINGLE_DEVIATIONS: self.plot_selected_deviations,
            PlotRequestType.TRAJECTORY_LAPS: self.plot_trajectory_laps,
            PlotRequestType.MULTI_DEVIATIONS: self.plot_multi_deviations,
            PlotRequestType.DEVIATION_LAPS: self.plot_deviation_laps,
            PlotRequestType.UPDATE_SETTINGS: self.update_settings,
            PlotRequestType.CORRELATION: self.plot_correlation,
        }

    def get_request(self) -> PlotRequest:
        return super().get_request()

    @pyqtSlot(PlotRequest)
    def handle_request(self, plot_request: PlotRequest) -> None:
        super().handle_request(plot_request)

    def update_settings(self) -> None:
        self.plot_settings = self.get_request().plot_settings

    def plot_selected_trajectories(self) -> None:
        trajectory_list = [entry.trajectory for entry in self.get_request().selection.entries]
        plot_tabs = PlotTabs(parent=self.parent())
        plot_tabs.show_trajectories(trajectory_list, dim=self.get_request().dim)

    def plot_selected_deviations(self) -> None:
        plot_tabs = PlotTabs(parent=self.parent())
        plot_tabs.show_single_deviations(
            devs=self.get_request().selection.entries[0].deviations, plot_settings=self.plot_settings
        )

    def plot_trajectory_laps(self) -> None:
        trajectory_entry = self.get_request().selection.entries[0]
        traj_list = trajectory_entry.trajectory.divide_into_laps()
        if traj_list is None:
            self.ui_request.emit(
                UIRequest(
                    type=UIRequestType.MESSAGE,
                    payload="Please sort Trajectory first!",
                )
            )
            return

        plot_tabs = PlotTabs(parent=self.parent())
        plot_tabs.show_trajectories(traj_list, plot_settings=self.plot_settings)

    def plot_multi_deviations(self) -> None:
        plot_tabs = PlotTabs(parent=self.parent())
        deviation_entries: list[AbsoluteDeviationEntry] = self.get_request().selection.entries
        deviation_list = [entry.deviations for entry in deviation_entries]
        plot_tabs.show_multi_deviations(deviation_list=deviation_list, plot_settings=self.plot_settings)

    def plot_deviation_laps(self) -> None:
        plot_tabs = PlotTabs(parent=self.parent())
        plot_tabs.show_multi_deviations(
            deviation_list=self.get_request().selection.entries[0].deviations.divide_into_laps(),
            plot_settings=self.plot_settings,
        )

    def plot_correlation(self) -> None:
        estimated_parameters = self.get_request().selection.entries[0].estimated_parameters
        plot_tabs = PlotTabs(parent=self.parent())
        plot_tabs.show_estimation(estimated_parameters=estimated_parameters)
