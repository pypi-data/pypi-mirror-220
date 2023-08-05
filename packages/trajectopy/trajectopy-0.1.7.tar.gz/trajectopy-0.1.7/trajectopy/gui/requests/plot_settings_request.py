"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2023
mail@gtombrink.de
"""
from dataclasses import dataclass
from enum import auto

from trajectopy.gui.requests.request import Request, RequestType


class PlotSettingsRequestType(RequestType):
    IMPORT_FROM_SESSION = auto()
    EXPORT_TO_SESSION = auto()
    RESET = auto()


@dataclass
class PlotSettingsRequest(Request):
    pass
