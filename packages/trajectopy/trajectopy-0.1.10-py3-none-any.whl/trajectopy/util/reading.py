"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2023
mail@gtombrink.de
"""
from datetime import datetime
from typing import Tuple

import numpy as np
import logging
import re
from dataclasses import dataclass

import pandas as pd
from trajectopy.settings.comparison_settings import ComparisonType
from trajectopy.util.datahandling import get_rot_matrix
from trajectopy.util.definitions import GPS_LEAP_SECONDS, GPS_WEEK_ZERO, TIME_FORMAT_DICT, TimeFormat
from trajectopy.util.rotationset import RotationSet
from pointset import PointSet

from trajectopy.util.spatialsorter import SORTING_DICT, Sorting
from trajectopy.util.trajectory_processing_state import TrajectoryProcessingState

logger = logging.getLogger("root")

HEADER_KEYS = [
    "epsg",
    "name",
    "sorting",
    "state",
    "fields",
    "delimiter",
    "nframe",
    "type",
    "comparison_type",
    "rot_unit",
    "time_format",
    "datetime_format",
    "datetime_timezone",
    "id",
    "gps_week",
    "time_offset",
]


def default_line_handler(line: str) -> str:
    return " ".join(line.split()[1:])


def integer_line_handler(line: str) -> int:
    return int(line.split()[1])


def float_line_handler(line: str) -> float:
    return float(line.split()[1])


def delimiter_line_handler(line: str) -> str:
    """This function extracts the delimiter from the file header. All characters between the first and the last quotation mark are returned."""
    if delimiter_match := re.search(r"#delimiter ['\"](.)['\"]", line):
        delimiter = delimiter_match[1]
        logger.info(f"Detected delimiter '{delimiter}'")
        return delimiter

    return ","


HANDLER_MAPPING = {
    "default": default_line_handler,
    "epsg": integer_line_handler,
    "delimiter": delimiter_line_handler,
    "gps_week": integer_line_handler,
    "time_offset": float_line_handler,
}


@dataclass
class HeaderData:
    """Class to store the header data of a trajectopy file."""

    data: dict[str, str | int | float]

    @property
    def id(self) -> str:
        return self.data.get("id", "")

    @property
    def epsg(self) -> int:
        return self.data.get("epsg", 0)

    @property
    def name(self) -> str:
        return self.data.get("name", "Trajectory")

    @property
    def rot_unit(self) -> str:
        return self.data.get("rot_unit", "rad")

    @property
    def sorting(self) -> Sorting:
        return SORTING_DICT[self.data.get("sorting", "chrono")]

    @property
    def state(self) -> TrajectoryProcessingState:
        return TrajectoryProcessingState.from_string(self.data.get("state", ""))

    @property
    def fields(self) -> list[str]:
        return self.data.get("fields", "t,px,py,pz,qx,qy,qz,qw").split(",")

    @property
    def delimiter(self) -> str:
        return self.data.get("delimiter", ",")

    @property
    def nframe(self) -> str:
        return self.data.get("nframe", "enu").lower()

    @property
    def type(self) -> str:
        return self.data.get("type", "trajectory").lower()

    @property
    def comparison_type(self) -> ComparisonType:
        return ComparisonType.from_string(self.data.get("comparison_type", "unknown"))

    @property
    def time_format(self) -> str:
        return TIME_FORMAT_DICT[self.data.get("time_format", "unix").lower()]

    @property
    def gps_week(self) -> int:
        return self.data.get("gps_week", np.floor((datetime.today() - GPS_WEEK_ZERO).days / 7))

    @property
    def time_offset(self) -> float:
        return self.data.get("time_offset", 0.0)

    @property
    def datetime_format(self) -> str:
        return self.data.get("datetime_format", "%Y-%m-%d %H:%M:%S.%f")

    @property
    def datetime_timezone(self) -> str:
        return self.data.get("datetime_timezone", "UTC")

    @classmethod
    def from_file(cls, filename: str) -> "HeaderData":
        """Reads the header of a trajectory file.

        Args:
            filename (str): The path to the file.

        Returns:
            HeaderData: The header data.
        """
        metadata = {}
        with open(filename, "r") as file:
            for line in file:
                if not line.startswith("#"):
                    break
                splitted_line = line.split()
                keyword = splitted_line[0][1:]

                if keyword in HEADER_KEYS:
                    metadata[keyword] = HANDLER_MAPPING.get(keyword, HANDLER_MAPPING["default"])(line)

        logger.info(f"Read header of {filename=}")
        return cls(metadata)


def read_data(filename: str, dtype=float) -> Tuple[HeaderData, np.ndarray]:
    """Reads the header and the data from a file

    By default, the trajectory data is read using pandas. If this fails,
    numpy is used instead.

    Args:
        filename (str): File to read

    Returns:
        Tuple[HeaderData, np.ndarray]: Header data and data
    """
    header_data = HeaderData.from_file(filename)
    try:
        data = pd.read_csv(filename, comment="#", header=None, sep=header_data.delimiter).to_numpy(dtype=dtype)

        if data.shape[1] == 1:
            logger.info("Assuming whitespaces as delimiter since imported data has only one column.")
            data = pd.read_csv(filename, comment="#", header=None, delim_whitespace=True).to_numpy(dtype=dtype)
    except Exception:
        try:
            data = pd.read_csv(filename, comment="#", header=None, delim_whitespace=True).to_numpy(dtype=dtype)
        except Exception:
            logger.warning("Could not read file using pandas. Trying numpy instead.")
            data = np.loadtxt(filename, comments="#")
    return header_data, data


def extract_trajectory_rotations(header_data: HeaderData, trajectory_data: np.ndarray) -> RotationSet:
    """Extracts rotations from trajectory data and returns them as RotationSet

    Loaded rotations are converted to refer to the ENU navigation frame. For this,
    the actual navigation frame must be specified in the header of the trajectory file using
    the #nframe tag. Otherwise, the default ENU frame is assumed.

    Args:
        header_data (HeaderData): Holds information about the header of the trajectory file
        trajectory_data (np.ndarray): Holds the trajectory data

    Returns:
        RotationSet: Rotations read from the trajectory file
    """
    rot = None
    if all(field in header_data.fields for field in ["qx", "qy", "qz", "qw"]):
        rot = extract_quaternions(header_data, trajectory_data)

    if all(field in header_data.fields for field in ["ex", "ey", "ez"]) and rot is None:
        rot = extract_euler_angles(header_data, trajectory_data)

    if rot is None:
        return rot

    enu_rot = RotationSet.from_matrix(get_rot_matrix(header_data.nframe))
    return enu_rot * rot


def extract_quaternions(header_data: HeaderData, trajectory_data: np.ndarray) -> RotationSet:
    """Extracts quaternions from trajectory data and returns them as RotationSet

    Args:
        header_data (HeaderData): Holds information about the header of the trajectory file
        trajectory_data (np.ndarray): Holds the trajectory data

    Returns:
        RotationSet: Rotations read from the trajectory file
    """
    return RotationSet.from_quat(
        trajectory_data[
            :,
            [
                header_data.fields.index("qx"),
                header_data.fields.index("qy"),
                header_data.fields.index("qz"),
                header_data.fields.index("qw"),
            ],
        ].astype(float)
    )


def extract_euler_angles(header_data: HeaderData, trajectory_data: np.ndarray) -> RotationSet:
    """Extracts euler angles from trajectory data and returns them as RotationSet

    Args:
        header_data (HeaderData): Holds information about the header of the trajectory file
        trajectory_data (np.ndarray): Holds the trajectory data

    Returns:
        RotationSet: Rotations read from the trajectory file
    """
    return RotationSet.from_euler(
        seq="xyz",
        angles=trajectory_data[
            :,
            [
                header_data.fields.index("ex"),
                header_data.fields.index("ey"),
                header_data.fields.index("ez"),
            ],
        ].astype(float),
        degrees=header_data.rot_unit == "deg",
    )


def extract_trajectory_timestamps(header_data: HeaderData, trajectory_data: np.ndarray) -> np.ndarray:
    """Extracts timestamps from trajectory data and returns them as numpy array

    Args:
        header_data (HeaderData): Holds information about the header of the trajectory file
        trajectory_data (np.ndarray): Holds the trajectory data

    Returns:
        np.ndarray: Timestamps read from the trajectory file
    """

    time_columns = [pos for pos, char in enumerate(header_data.fields) if char == "t"]

    if header_data.time_format == TimeFormat.UNIX and len(time_columns) == 1:
        return trajectory_data[:, header_data.fields.index("t")].astype(float) + header_data.time_offset

    if header_data.time_format == TimeFormat.DATETIME and time_columns:
        return (
            parse_datetime(trajectory_data=trajectory_data, time_columns=time_columns, header_data=header_data)
            + header_data.time_offset
        )

    if header_data.time_format == TimeFormat.GPS_SOW and time_columns:
        return (
            parse_gps_sow(trajectory_data=trajectory_data, time_columns=time_columns, header_data=header_data)
            + header_data.time_offset
        )

    logger.warning("To timestamps found.")
    return np.array(range(len(trajectory_data)))


def parse_datetime(trajectory_data: np.ndarray, time_columns: list[int], header_data: HeaderData) -> np.ndarray:
    def concatenate_strings(arr, delimiter=" "):
        return delimiter.join(arr)

    datetime_strings = np.apply_along_axis(concatenate_strings, 1, trajectory_data[:, time_columns])

    ts_datetime = pd.to_datetime(datetime_strings, format=header_data.datetime_format)

    if header_data.datetime_timezone.upper() == "GPS":
        ts_datetime -= pd.Timedelta(seconds=GPS_LEAP_SECONDS)
        time_zone = "UTC"
        logger.info("Applied GPS leap seconds.")
    else:
        time_zone = header_data.datetime_timezone

    ts_datetime = pd.DatetimeIndex(ts_datetime).tz_localize(tz=time_zone)
    logger.info("Timezone: %s", time_zone)

    return np.array([dt_i.timestamp() for dt_i in ts_datetime])


def parse_gps_sow(trajectory_data: np.ndarray, time_columns: list[int], header_data: HeaderData) -> np.ndarray:
    """Parses GPS seconds of week to timestamps

    Args:
        trajectory_data (np.ndarray): Holds the trajectory data
        time_columns (list[int]): Indices of the column containing the GPS seconds of week
        header_data (HeaderData): Holds information about the header of the trajectory file

    Returns:
        np.ndarray: Timestamps read from the trajectory file
    """
    return (
        trajectory_data[:, time_columns].astype(float).flatten()
        + header_data.gps_week * 604800
        - GPS_LEAP_SECONDS
        + GPS_WEEK_ZERO.timestamp()
    )


def extract_trajectory_speed(header_data: HeaderData, trajectory_data: np.ndarray) -> np.ndarray:
    """Extracts speed from trajectory data and returns them as numpy array

    Args:
        header_data (HeaderData): Holds information about the header of the trajectory file
        trajectory_data (np.ndarray): Holds the trajectory data

    Returns:
        np.ndarray: Speeds read from the trajectory file
    """
    return (
        None
        if any(item not in header_data.fields for item in ["vx", "vy", "vz"])
        else trajectory_data[
            :,
            [
                header_data.fields.index("vx"),
                header_data.fields.index("vy"),
                header_data.fields.index("vz"),
            ],
        ].astype(float)
    )


def extract_trajectory_arc_lengths(header_data: HeaderData, trajectory_data: np.ndarray) -> np.ndarray:
    """Extracts arc lengths from trajectory data and returns them as numpy array

    Args:
        header_data (HeaderData): Holds information about the header of the trajectory file
        trajectory_data (np.ndarray): Holds the trajectory data

    Returns:
        np.ndarray: Arc lengths read from the trajectory file
    """
    return None if "l" not in header_data.fields else trajectory_data[:, header_data.fields.index("l")].astype(float)


def extract_trajectory_pointset(header_data: HeaderData, trajectory_data: np.ndarray) -> PointSet:
    """Extracts positions from pandas DataFrame and returns a PointSet

    The positions of 'px', 'py', 'pz' are used as indices to access
    the DataFrame.

    Args:
        header_data (HeaderData): Holds information about the header of the trajectory file
        trajectory_data (np.ndarray): Holds the trajectory data

    Returns:
        PointSet: PointSet object containing the parsed positions.
    """
    return PointSet(
        xyz=trajectory_data[
            :, [header_data.fields.index("px"), header_data.fields.index("py"), header_data.fields.index("pz")]
        ].astype(float),
        epsg=header_data.epsg,
    )
