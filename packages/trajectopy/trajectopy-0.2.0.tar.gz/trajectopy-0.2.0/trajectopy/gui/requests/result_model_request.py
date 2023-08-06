"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2023
mail@gtombrink.de
"""
from dataclasses import dataclass
from enum import auto

from trajectopy.gui.requests.request import Request, RequestType


class ResultModelRequestType(RequestType):
    ADD = auto()
    UPDATE = auto()
    RENAME = auto()
    REMOVE = auto()
    PASS_ALIGNMENTS_TO_UI = auto()
    RESET = auto()
    EXPORT_ALL = auto()
    EDIT_ALIGNMENT = auto()
    COPY = auto()
    SORT = auto()


@dataclass
class ResultModelRequest(Request):
    pass
