"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2023
mail@gtombrink.de
"""
import copy
from dataclasses import dataclass
from enum import auto
from typing import Any
from trajectopy.gui.requests.request import Request, RequestType


class TrajectoryManagerRequestType(RequestType):
    SWITCH_SORTING = auto()
    COMPARE = auto()
    ALIGN = auto()
    ADAPT_FIRST_POSE = auto()
    ADAPT_FIRST_POSITION = auto()
    ADAPT_FIRST_ORIENTATION = auto()
    APPLY_ALIGNMENT = auto()
    APPROXIMATE = auto()
    SORT = auto()
    CHANGE_ESPG = auto()
    EPSG_TO_REF = auto()
    INTERSECT = auto()
    INTERPOLATE = auto()
    INTERPOLATE_GRID = auto()
    MERGE = auto()
    ADAPT_SAMPLING = auto()
    MATCH_TIMESTAMPS = auto()
    ADAPT_ORIENTATIONS = auto()
    ROUGH_TIMESTAMPS_MATCHING = auto()


@dataclass
class TrajectoryManagerRequest(Request):
    target: Any = None

    def __post_init__(self) -> None:
        self.selection = copy.deepcopy(self.selection)
