"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2023
mail@gtombrink.de
"""
from dataclasses import dataclass
from enum import auto

from trajectopy.gui.requests.request import Request, RequestType
from trajectopy.settings.plot_settings import PlotSettings


class PlotRequestType(RequestType):
    SINGLE_DEVIATIONS = auto()
    MULTI_DEVIATIONS = auto()
    TRAJECTORIES = auto()
    TRAJECTORY_LAPS = auto()
    DEVIATION_LAPS = auto()
    UPDATE_SETTINGS = auto()
    CORRELATION = auto()


@dataclass
class PlotRequest(Request):
    dim: int = 2
    plot_settings: PlotSettings = None
