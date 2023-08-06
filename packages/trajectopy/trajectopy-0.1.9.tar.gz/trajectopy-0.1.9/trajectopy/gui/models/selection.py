"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2023
mail@gtombrink.de
"""
from dataclasses import dataclass, field
from typing import Union

from trajectopy.gui.models.entry import AlignmentEntry, AbsoluteDeviationEntry, TrajectoryEntry

ArbitraryResultEntry = Union[AlignmentEntry, AbsoluteDeviationEntry]


@dataclass
class TrajectorySelection:
    entries: list[TrajectoryEntry] = field(default_factory=list)
    reference_entry: TrajectoryEntry | None = None

    def __len__(self) -> int:
        return len(self.entries)

    def __bool__(self):
        return bool(self.entries)

    @property
    def reference_is_set(self) -> bool:
        return self.reference_entry is not None


@dataclass
class ResultSelection:
    entries: list[ArbitraryResultEntry] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.entries)

    def __bool__(self):
        return bool(self.entries)
