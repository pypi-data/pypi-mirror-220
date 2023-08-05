"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2023
mail@gtombrink.de
"""
import copy
from dataclasses import dataclass, field
from enum import auto
from trajectopy.gui.requests.request import Request, RequestType


class FileRequestType(RequestType):
    READ_TRAJ = auto()
    WRITE_TRAJ = auto()
    READ_RES = auto()
    WRITE_RES = auto()
    WRITE_LIST = auto()
    READ_TRAJ_ORDER = auto()
    READ_RES_ORDER = auto()


@dataclass
class FileRequest(Request):
    file_list: list[str] = field(default_factory=list)

    
    def __post_init__(self) -> None:
        self.selection = copy.deepcopy(self.selection)