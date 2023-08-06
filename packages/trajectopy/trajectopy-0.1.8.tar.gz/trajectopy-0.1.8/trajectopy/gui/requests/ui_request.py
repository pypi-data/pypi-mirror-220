"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2023
mail@gtombrink.de
"""
from dataclasses import dataclass
from enum import auto
from typing import Any

from trajectopy.gui.requests.request import Request, RequestType


class UIRequestType(RequestType):
    TRAJ_PROPERTIES = auto()
    RES_PROPERTIES = auto()
    TRAJ_SETTINGS = auto()
    PLOT_SETTINGS = auto()
    EPSG_SELECTION = auto()
    GRID_SELECTION = auto()
    ALIGNMENT_SELECTION = auto()
    EXPORT_TRAJ = auto()
    IMPORT_TRAJ = auto()
    EXPORT_RES = auto()
    IMPORT_RES = auto()
    MESSAGE = auto()
    CONFIRM_RESET = auto()
    EXPORT_SESSION = auto()
    IMPORT_SESSION = auto()
    EDIT_ALIGNMENT = auto()
    EXPORT_DEV_SUMMARY = auto()


@dataclass
class UIRequest(Request):
    payload: Any = None
