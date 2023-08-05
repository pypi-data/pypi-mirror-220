"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2023
mail@gtombrink.de
"""
from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from trajectopy.gui.models.selection import ResultSelection, TrajectorySelection


class RequestType(Enum):
    pass


@dataclass
class Request(ABC):
    type: RequestType
    selection: Optional[TrajectorySelection | ResultSelection | str] = None
