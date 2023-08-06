"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2023
mail@gtombrink.de
"""
from dataclasses import dataclass
from enum import auto

from trajectopy.gui.requests.request import Request, RequestType


class SessionRequestType(RequestType):
    IMPORT = auto()
    EXPORT = auto()
    NEW = auto()


@dataclass
class SessionRequest(Request):
    pass
