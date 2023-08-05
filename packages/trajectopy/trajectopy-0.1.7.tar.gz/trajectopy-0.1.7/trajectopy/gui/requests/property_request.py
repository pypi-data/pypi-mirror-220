"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2023
mail@gtombrink.de
"""
from dataclasses import dataclass
from enum import auto
from trajectopy.gui.requests.request import Request, RequestType


class PropertyModelRequestType(RequestType):
    EXPORT = auto()


@dataclass
class PropertyModelRequest(Request):
    file: str = None
