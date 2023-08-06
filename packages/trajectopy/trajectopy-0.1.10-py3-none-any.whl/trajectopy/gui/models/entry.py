"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2023
mail@gtombrink.de
"""
import logging
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from pathlib import Path
from typing import Tuple

import numpy as np

from trajectopy.alignment.parameters import AlignmentParameters
from trajectopy.evaluation.trajectory_deviations import AbsoluteTrajectoryDeviations, RelativeTrajectoryDeviations
from trajectopy.gui.util import bool_to_str, generate_id
from trajectopy.settings.alignment_settings import AlignmentEstimationSettings
from trajectopy.settings.comparison_settings import ComparisonMethod
from trajectopy.settings.processing_settings import ProcessingSettings
from trajectopy.trajectory import Trajectory
from trajectopy.util.reading import HeaderData
from trajectopy.util.rotationset import RotationSet
from trajectopy.util.spatialsorter import Sorting

logger = logging.getLogger("root")


class ResultType(Enum):
    ALIGNMENT = auto()
    APPROXIMATION = auto()
    DEVIATIONS = auto()


@dataclass
class Entry(ABC):
    id: str = field(default_factory=generate_id)

    def __post_init__(self) -> None:
        if self.id in [None, ""]:
            self.renew_id()

    def renew_id(self) -> None:
        self.id = generate_id()

    def to_file(self, filename: str) -> None:
        with open(filename, "w", newline="\n") as file:
            file.write(f"#id {self.id}\n")


@dataclass
class ResultEntry(Entry):
    time: str = field(init=False, default_factory=lambda: str(datetime.now()))
    _result_type: ResultType = field(init=False)
    name: str = "Result"

    @property
    def column(self) -> Tuple[str, str, str, str]:
        return self.name, str(self._result_type.name), self.time, self.id

    @abstractmethod
    def property_dict(self):
        pass

    def set_name(self, name: str) -> None:
        self.name = name

    def to_file(self, filename: str) -> None:
        super().to_file(filename=filename)
        with open(filename, "a", newline="\n") as file:
            file.write(f"#type {self._result_type.name}\n")
            file.write(f"#name {self.name}\n")

    @classmethod
    def from_file(cls, filename: str) -> "ResultEntry":
        header_data = HeaderData.from_file(filename)

        if header_data.comparison_type.comparison_method == ComparisonMethod.ABSOLUTE:
            logger.info("Detected Absolute Deviations file.")
            return AbsoluteDeviationEntry.from_file(filename)

        if header_data.comparison_type.comparison_method == ComparisonMethod.RELATIVE:
            logger.info("Detected Relative Deviations file.")
            return RelativeDeviationEntry.from_file(filename)

        if header_data.type == "alignment":
            logger.info("Detected Alignment file.")
            return AlignmentEntry.from_file(filename)

        raise ValueError(f"No supported result type '{header_data.type}'")


@dataclass
class DeviationEntry(ResultEntry):
    deviations: AbsoluteTrajectoryDeviations | RelativeTrajectoryDeviations = None

    def __post_init__(self) -> None:
        self._result_type = ResultType.DEVIATIONS

    def set_name(self, name: str) -> None:
        super().set_name(name)
        self.deviations.name = name

    @property
    def property_dict(self) -> dict[str, str]:
        return self.deviations.property_dict

    def to_file(self, filename: str) -> None:
        super().to_file(filename=filename)
        with open(filename, "a", newline="\n") as file:
            file.write(f"#comparison_type {self.deviations.comparison_type}\n")
            if isinstance(self.deviations, AbsoluteTrajectoryDeviations):
                file.write(f"#sorting {str(self.deviations.sorting)}\n")
        self.deviations.to_dataframe().to_csv(filename, header=False, index=False, mode="a", float_format="%.12f")


@dataclass
class AbsoluteDeviationEntry(DeviationEntry):
    @classmethod
    def from_file(cls, filename: str) -> "AbsoluteDeviationEntry":
        deviations = AbsoluteTrajectoryDeviations.from_file(filename)
        return AbsoluteDeviationEntry(
            id=HeaderData.from_file(filename).id, name=deviations.name, deviations=deviations
        )


@dataclass
class RelativeDeviationEntry(DeviationEntry):
    @classmethod
    def from_file(cls, filename: str) -> "RelativeDeviationEntry":
        deviations = RelativeTrajectoryDeviations.from_file(filename)
        return RelativeDeviationEntry(
            id=HeaderData.from_file(filename).id, name=deviations.name, deviations=deviations
        )


@dataclass
class AlignmentEntry(ResultEntry):
    estimated_parameters: AlignmentParameters = None
    estimation_of: AlignmentEstimationSettings = None

    def __post_init__(self) -> None:
        self._result_type = ResultType.ALIGNMENT

    @property
    def property_dict(self) -> dict[str, str]:
        return {
            "Translation x [m]": f"{self.estimated_parameters.helmert.trans_x.value:<10.4f} s-dev.: {np.sqrt(self.estimated_parameters.helmert.trans_x.variance):<10.4f}",
            "Translation y [m]": f"{self.estimated_parameters.helmert.trans_y.value:<10.4f} s-dev.: {np.sqrt(self.estimated_parameters.helmert.trans_y.variance):<10.4f}",
            "Translation z [m]": f"{self.estimated_parameters.helmert.trans_z.value:<10.4f} s-dev.: {np.sqrt(self.estimated_parameters.helmert.trans_z.variance):<10.4f}",
            "Rotation x [°]": f"{np.rad2deg(self.estimated_parameters.helmert.rot_x.value):<10.4f} s-dev.: {np.rad2deg(np.sqrt(self.estimated_parameters.helmert.rot_x.variance)):<10.4f}",
            "Rotation y [°]": f"{np.rad2deg(self.estimated_parameters.helmert.rot_y.value):<10.4f} s-dev.: {np.rad2deg(np.sqrt(self.estimated_parameters.helmert.rot_y.variance)):<10.4f}",
            "Rotation z [°]": f"{np.rad2deg(self.estimated_parameters.helmert.rot_z.value):<10.4f} s-dev.: {np.rad2deg(np.sqrt(self.estimated_parameters.helmert.rot_z.variance)):<10.4f}",
            "Scale [-]": f"{self.estimated_parameters.helmert.scale.value:<10.4f} s-dev.: {np.sqrt(self.estimated_parameters.helmert.scale.variance)*1e6:<10.4f} ppm",
            "Time Shift [s]": f"{self.estimated_parameters.time_shift.value:<10.4f} s-dev.: {np.sqrt(self.estimated_parameters.time_shift.variance):<10.4f}",
            "Leverarm x [m]": f"{self.estimated_parameters.leverarm.x.value:<10.4f} s-dev.: {np.sqrt(self.estimated_parameters.leverarm.x.variance):<10.4f}",
            "Leverarm y [m]": f"{self.estimated_parameters.leverarm.y.value:<10.4f} s-dev.: {np.sqrt(self.estimated_parameters.leverarm.y.variance):<10.4f}",
            "Leverarm z [m]": f"{self.estimated_parameters.leverarm.z.value:<10.4f} s-dev.: {np.sqrt(self.estimated_parameters.leverarm.z.variance):<10.4f}",
        }

    def to_file(self, filename: str) -> None:
        super().to_file(filename=filename)
        self.estimated_parameters.to_dataframe().to_csv(
            filename, header=False, index=False, mode="a", float_format="%.15f"
        )

    @classmethod
    def from_file(cls, filename: str) -> "AlignmentEntry":
        header_data = HeaderData.from_file(filename)
        estimated_parameters = AlignmentParameters.from_file(filename)
        return AlignmentEntry(
            id=header_data.id,
            name=header_data.data.get("name", "Alignment"),
            estimated_parameters=estimated_parameters,
            estimation_of=AlignmentEstimationSettings.from_bool_list(estimated_parameters.enabled_bool_list),
        )


@dataclass
class PropertyEntry(Entry):
    name: str = "Property"
    values: Tuple[str] = None

    @property
    def column(self) -> Tuple[str, str]:
        return (self.name, *self.values)


@dataclass
class TrajectoryEntry(Entry):
    full_filename: str = ""
    trajectory: Trajectory = None
    set_as_reference: bool = False
    settings: ProcessingSettings = field(default_factory=ProcessingSettings)
    group_id: str = field(default_factory=generate_id)

    def to_file(self, filename: str) -> None:
        super().to_file(filename)
        self.trajectory.to_file(filename=filename, mode="a")

    @classmethod
    def from_file(cls, trajectory_filename: Path, settings_filename: Path) -> "TrajectoryEntry":
        header_data = HeaderData.from_file(trajectory_filename)
        trajectory = Trajectory.from_file(trajectory_filename)
        if settings_filename.is_file():
            logger.info(f"Using existing settings file: {settings_filename}")
            traj_settings = ProcessingSettings.from_file(settings_filename)
        else:
            logger.info(
                "No settings file found. Settings can be provided by storing a yaml file with the same name in the same directory."
            )
            traj_settings = ProcessingSettings()

        if trajectory is None:
            raise ValueError(
                "This file does not seem to have correct trajectory information (Time, X, Y, Z, qx, qy, qz, qw)!"
            )

        return TrajectoryEntry(
            id=header_data.id, full_filename=str(trajectory_filename), trajectory=trajectory, settings=traj_settings
        )

    @property
    def name(self) -> str:
        return self.trajectory.name

    @property
    def column(self) -> Tuple[str, bool, int, int, str, str]:
        return (
            self.name,
            bool_to_str(self.set_as_reference),
            str(self.trajectory.sorting),
            self.trajectory.pos.epsg,
            str(self.trajectory.state),
            self.full_filename,
        )

    @property
    def has_orientations(self) -> str:
        return bool_to_str(self.trajectory.rot is not None)

    @property
    def filename(self) -> str:
        return os.path.basename(self.full_filename)

    @property
    def property_dict(self) -> dict[str, str]:
        """Shows a new window with trajectory properties"""
        return {
            "Name": self.trajectory.name,
            "Date": f"{datetime.fromtimestamp(self.trajectory.tstamps[0]).strftime('%Y-%m-%d %H:%M:%S')} UTC - "
            f"{datetime.fromtimestamp(self.trajectory.tstamps[-1]).strftime('%Y-%m-%d %H:%M:%S')} UTC",
            "Duration": f"{timedelta(seconds=self.trajectory.tstamps[-1] - self.trajectory.tstamps[0])}",
            "EPSG": f"{self.trajectory.pos.crs}, {self.trajectory.pos.crs.name}"
            if self.trajectory.pos.crs is not None
            else "local / unknown",
            "Orientation available": "yes" if self.trajectory.rot is not None else "no",
            "Number of Poses": str(len(self.trajectory)),
            "Sorting": f"{'Spatial' if self.trajectory.sorting == Sorting.SPATIAL else 'Chronological'}",
            "Length [m]": f"{self.trajectory.arc_length:.3f}",
            "Data Rate [Hz]": f"{self.trajectory.data_rate:.3f}",
            "Minimum Speed [m/s]": f"{np.min(self.trajectory.speed):.3f}",
            "Maximum Speed [m/s]": f"{np.max(self.trajectory.speed):.3f}",
            "Average Speed [m/s]": f"{np.mean(self.trajectory.speed):.3f}",
            "Sorting known": "yes" if self.trajectory.state.sorting_known else "no",
            "Approximated": "yes" if self.trajectory.state.approximated else "no",
            "Intersected": "yes" if self.trajectory.state.intersected else "no",
            "Interpolated": "yes" if self.trajectory.state.interpolated else "no",
            "Matched Timestamps": "yes" if self.trajectory.state.matched else "no",
            "Filename": self.full_filename,
            "UUID": str(self.id),
        }
