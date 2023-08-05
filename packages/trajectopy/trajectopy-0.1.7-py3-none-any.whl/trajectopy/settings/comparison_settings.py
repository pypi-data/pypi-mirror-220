from dataclasses import dataclass, field
from enum import Enum, auto

from trajectopy.settings.core import Settings, field_extractor
from trajectopy.util.printing import dict2table


class ComparisonMethod(Enum):
    ABSOLUTE = auto()
    RELATIVE = auto()
    UNKNOWN = auto()


class MatchingMethod(Enum):
    NEAREST_SPATIAL = auto()
    NEAREST_TEMPORAL = auto()
    INTERPOLATION = auto()
    UNKNOWN = auto()


class RelativeMode(Enum):
    TIME = auto()
    DISTANCE = auto()


@dataclass
class MatchingSettings(Settings):
    method: MatchingMethod = MatchingMethod.INTERPOLATION
    max_time_diff: float = 0.01
    max_distance: float = 0.01

    def to_dict(self) -> dict[str, str]:
        return {
            "method": self.method.name,
            "max_time_diff": self.max_time_diff,
            "max_distance": self.max_distance,
        }

    @classmethod
    def from_config_dict(cls: "MatchingSettings", config_dict: dict) -> "MatchingSettings":
        return matching_settings_from_dict(config_dict=config_dict)


@dataclass
class ComparisonType(Settings):
    comparison_method: ComparisonMethod = ComparisonMethod.UNKNOWN
    matching_settings: MatchingSettings = field(default_factory=MatchingSettings)
    relative_mode: RelativeMode = RelativeMode.DISTANCE

    def __str__(self) -> str:
        if self.comparison_method == ComparisonMethod.ABSOLUTE:
            return f"{self.comparison_method.name} - {self.matching_settings.method.name}"

        return f"{self.comparison_method.name} - {self.matching_settings.method.name} - {self.relative_mode.name}"

    def to_dict(self) -> dict[str, str]:
        return {
            "comparison_method": self.comparison_method.name,
            "matching_settings": self.matching_settings.to_dict(),
            "relative_mode": self.relative_mode.name,
        }

    @classmethod
    def from_config_dict(cls: "ComparisonType", config_dict: dict) -> "ComparisonType":
        return comparison_type_from_dict(config_dict=config_dict)

    @classmethod
    def from_string(cls, string: str) -> "ComparisonType":
        comp_type = ComparisonType()
        comparison_method = comparison_method_from_string(string)
        matching_setttings = MatchingSettings()
        matching_setttings.method = matching_method_from_string(string)
        relative_mode = relative_mode_from_string(string)

        comp_type.comparison_method = comparison_method
        comp_type.matching_settings = matching_setttings
        comp_type.relative_mode = relative_mode
        return comp_type


@dataclass
class ComparisonSettings(Settings):
    type: ComparisonType = field(default_factory=ComparisonType)
    relative_pair_distance: float = 10.0
    relative_pair_time_difference: float = 10.0
    use_all_pose_pairs: bool = False

    @classmethod
    def from_config_dict(cls: "ComparisonSettings", config_dict: dict) -> "ComparisonSettings":
        return field_extractor(
            config_class=cls(),
            config_dict=config_dict,
            fill_missing_with={"default": 0.0},
            field_handler={"type": comparison_type_from_dict},
        )

    def __str__(self) -> str:
        return dict2table(
            input={
                "relative_pair_time_difference": self.relative_pair_time_difference,
                "relative_pair_distance": self.relative_pair_distance,
                "use_all_pose_pairs": self.use_all_pose_pairs,
                "matching type": self.type.matching_settings.method.name,
                "min_time_diff": self.type.matching_settings.max_time_diff,
                "max_distance": self.type.matching_settings.max_distance,
            },
            title="Comparison Settings",
        )

    def to_dict(self) -> dict[str, str]:
        return {
            "relative_pair_time_difference": self.relative_pair_time_difference,
            "relative_pair_distance": self.relative_pair_distance,
            "use_all_pose_pairs": self.use_all_pose_pairs,
            "type": self.type.to_dict(),
        }


def comparison_method_from_string(string: str) -> ComparisonMethod:
    if "absolute" in string.lower():
        return ComparisonMethod.ABSOLUTE

    return ComparisonMethod.RELATIVE if "relative" in string.lower() else ComparisonMethod.UNKNOWN


def matching_method_from_string(string: str) -> MatchingMethod:
    if "nearest_spatial" in string.lower():
        return MatchingMethod.NEAREST_SPATIAL

    if "nearest_temporal" in string.lower():
        return MatchingMethod.NEAREST_TEMPORAL

    return MatchingMethod.INTERPOLATION if "interpolation" in string.lower() else MatchingMethod.UNKNOWN


def relative_mode_from_string(string: str) -> RelativeMode:
    return RelativeMode.TIME if "time" in string.lower() else RelativeMode.DISTANCE


def matching_settings_from_dict(config_dict: dict) -> MatchingSettings:
    return field_extractor(
        config_class=MatchingSettings(),
        config_dict=config_dict,
        fill_missing_with={"default": 0.0},
        field_handler={"method": matching_method_from_string},
    )


def comparison_type_from_dict(config_dict: dict) -> ComparisonType:
    return field_extractor(
        config_class=ComparisonType(),
        config_dict=config_dict,
        fill_missing_with={"default": 0.0},
        field_handler={
            "comparison_method": comparison_method_from_string,
            "matching_settings": matching_settings_from_dict,
            "relative_mode": relative_mode_from_string,
        },
    )
