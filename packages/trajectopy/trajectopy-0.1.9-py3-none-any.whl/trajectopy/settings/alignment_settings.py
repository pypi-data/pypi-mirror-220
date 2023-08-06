"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2023
mail@gtombrink.de
"""
from dataclasses import dataclass, field
import numpy as np
from trajectopy.settings.comparison_settings import MatchingSettings, matching_settings_from_dict
from trajectopy.settings.core import Settings, field_extractor, yaml2dict


METRIC_THRESHOLD = 1e-4
TIME_THRESHOLD = 1e-4


@dataclass
class AlignmentPreprocessing(Settings):
    min_speed: float = 0.0
    time_start: float = 0.0
    time_end: float = 0.0
    matching_settings: MatchingSettings = field(default_factory=MatchingSettings)

    def to_dict(self) -> dict[str, str]:
        return {
            "min_speed": self.min_speed,
            "time_start": self.time_start,
            "time_end": self.time_end,
            "matching_settings": self.matching_settings.to_dict(),
        }

    @classmethod
    def from_config_dict(cls, config_dict: dict) -> "AlignmentPreprocessing":
        return field_extractor(
            config_class=cls(),
            config_dict=config_dict,
            fill_missing_with={"default": 0.0},
            field_handler={"matching_settings": matching_settings_from_dict},
        )


@dataclass
class AlignmentEstimationSettings(Settings):
    helmert: bool = True
    trans_x: bool = True
    trans_y: bool = True
    trans_z: bool = True
    rot_x: bool = True
    rot_y: bool = True
    rot_z: bool = True
    scale: bool = True

    time_shift: bool = False
    use_x_speed: bool = True
    use_y_speed: bool = True
    use_z_speed: bool = True

    leverarm: bool = False
    lever_x: bool = True
    lever_y: bool = True
    lever_z: bool = True

    def __bool__(self) -> bool:
        return not self.all_disabled

    @classmethod
    def from_config_dict(cls: "AlignmentEstimationSettings", config_dict: dict) -> "AlignmentEstimationSettings":
        return field_extractor(
            config_class=cls(),
            config_dict=config_dict,
            fill_missing_with={
                "default": True,
                "helmert": False,
                "leverarm": False,
                "time_shift": False,
            },
        )

    @classmethod
    def from_bool_list(cls: "AlignmentEstimationSettings", bool_list: list[bool]) -> "AlignmentEstimationSettings":
        if len(bool_list) != 11:
            raise ValueError("Size mismatch: bool_list must have length 11 (Number of parameters)")

        helmert_enabled = any(bool_list[:8])
        leverarm_enabled = any(bool_list[8:])

        return AlignmentEstimationSettings(
            helmert=helmert_enabled,
            leverarm=leverarm_enabled,
            trans_x=bool_list[0],
            trans_y=bool_list[1],
            trans_z=bool_list[2],
            rot_x=bool_list[3],
            rot_y=bool_list[4],
            rot_z=bool_list[5],
            scale=bool_list[6],
            time_shift=bool_list[7],
            lever_x=bool_list[8],
            lever_y=bool_list[9],
            lever_z=bool_list[10],
        )

    @property
    def all_disabled(self) -> bool:
        return not any([self.helmert_enabled, self.time_shift_enabled, self.leverarm_enabled])

    @property
    def helmert_enabled(self) -> bool:
        return any(self.helmert_filter)

    @property
    def leverarm_enabled(self) -> bool:
        return any(self.leverarm_filter)

    @property
    def time_shift_enabled(self) -> bool:
        return any(self.time_shift_filter)

    @property
    def short_mode_str(self) -> str:
        settings_str = ""

        if self.helmert_enabled:
            settings_str += "Helmert "

        if self.time_shift_enabled:
            settings_str += "Time-Shift "

        if self.leverarm_enabled:
            settings_str += "Leverarm"

        return settings_str

    @property
    def time_shift_filter(self) -> list[bool]:
        return [
            self.use_x_speed and self.time_shift,
            self.use_y_speed and self.time_shift,
            self.use_z_speed and self.time_shift,
        ]

    @property
    def helmert_filter(self) -> list[bool]:
        return [
            self.trans_x and self.helmert,
            self.trans_y and self.helmert,
            self.trans_z and self.helmert,
            self.rot_x and self.helmert,
            self.rot_y and self.helmert,
            self.rot_z and self.helmert,
            self.scale and self.helmert,
        ]

    @property
    def leverarm_filter(self) -> list[bool]:
        return [
            self.lever_x and self.leverarm,
            self.lever_y and self.leverarm,
            self.lever_z and self.leverarm,
        ]

    @property
    def enabled_parameter_filter(self) -> list[bool]:
        full_filter = []

        if self.helmert_enabled:
            full_filter.extend(self.helmert_filter)

        if self.time_shift_enabled:
            full_filter.append(self.time_shift)

        if self.leverarm_enabled:
            full_filter.extend(self.leverarm_filter)

        return full_filter

    @property
    def parameter_filter(self) -> list[bool]:
        return self.helmert_filter + [self.time_shift_enabled] + self.leverarm_filter


@dataclass
class AlignmentStochastics(Settings):
    var_xy_from: float = 1.0
    var_z_from: float = 1.0
    var_xy_to: float = 1.0
    var_z_to: float = 1.0
    var_roll_pitch: float = float(np.deg2rad(1.0)) ** 2
    var_yaw: float = float(np.deg2rad(1.0)) ** 2
    var_speed_to: float = 1.0
    error_probability: float = 0.05

    @classmethod
    def from_config_dict(cls: "AlignmentStochastics", config_dict: dict) -> "AlignmentStochastics":
        init_class: "AlignmentStochastics" = field_extractor(
            config_class=cls(),
            config_dict=config_dict,
            fill_missing_with={
                "default": 1.0,
                "error_probability": 0.05,
            },
        )
        return init_class


@dataclass
class AlignmentSettings(Settings):
    """Dataclass defining alignment configuration

    Args:

        - mode (str): Mode of the H(elmert)-L(everarm)-T(ime) transformation
                          Depending on the presence of the letters "h", "l", "t"
                          inside this string, the alignment will estimate the
                          corresponding parameters
        - std_xx (float): Standard deviations in their corresponding unit
                          of the supported observation_groups:
            - xy_from (source positions)
            - z_from
            - xy_to (target positions)
            - z_to
            - roll_pitch (platform orientations)
            - yaw

    """

    preprocessing: AlignmentPreprocessing = field(default_factory=AlignmentPreprocessing)
    estimation_of: AlignmentEstimationSettings = field(default_factory=AlignmentEstimationSettings)
    stochastics: AlignmentStochastics = field(default_factory=AlignmentStochastics)
    metric_threshold: float = METRIC_THRESHOLD
    time_threshold: float = TIME_THRESHOLD

    def __str__(self) -> str:
        return str(self.preprocessing) + str(self.estimation_of) + str(self.stochastics)

    def to_dict(self) -> dict[str, str]:
        return {
            "preprocessing": self.preprocessing.to_dict(),
            "estimation_of": self.estimation_of.to_dict(),
            "stochastics": self.stochastics.to_dict(),
        }

    @classmethod
    def from_file(cls, file: str) -> "AlignmentSettings":
        return cls.from_config_dict(config_dict=yaml2dict(file))

    @classmethod
    def from_config_dict(cls: "AlignmentSettings", config_dict: dict) -> "AlignmentSettings":
        preprocessing = AlignmentPreprocessing.from_config_dict(config_dict.get("preprocessing", {}))
        estimation_of = AlignmentEstimationSettings.from_config_dict(config_dict.get("estimation_of", {}))
        stochastics = AlignmentStochastics.from_config_dict(config_dict.get("stochastics", {}))

        return cls(preprocessing=preprocessing, estimation_of=estimation_of, stochastics=stochastics)
