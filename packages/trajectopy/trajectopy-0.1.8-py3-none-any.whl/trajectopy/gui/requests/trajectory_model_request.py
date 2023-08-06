"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2023
mail@gtombrink.de
"""
from dataclasses import dataclass
from enum import auto
from trajectopy.gui.requests.request import Request, RequestType


class TrajectoryModelRequestType(RequestType):
    ADD = auto()
    UPDATE = auto()
    RENAME = auto()
    SET_REFERENCE = auto()
    UNSET_REFERENCE = auto()
    COPY = auto()
    REMOVE = auto()
    REMOVE_RELATED = auto()
    RESET = auto()
    EXPORT_ALL = auto()
    SORT = auto()


@dataclass
class TrajectoryModelRequest(Request):
    pass
