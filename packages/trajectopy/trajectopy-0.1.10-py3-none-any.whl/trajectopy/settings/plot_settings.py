"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2023
mail@gtombrink.de
"""
from dataclasses import dataclass
import yaml
import logging
from trajectopy.settings.core import Settings, field_extractor, yaml2dict

logger = logging.getLogger("root")


@dataclass
class PlotSettings(Settings):
    rms_window_width: float = 1.0
    grid_mp: float = 4.0
    always_show_zero: bool = True
    c_bar_step_divisor: int = 4
    scatter_no_axis: bool = True
    scatter_sigma_factor: float = 3.0
    scatter_rotate: bool = False
    unit_is_mm: bool = False
    hist_as_stairs: bool = False
    smoothing_window_size: float = 1.0
    show_mean_line: bool = True
    heatmap_spacing: float = 1.0
    show_directed_devs: bool = True

    @classmethod
    def from_config_dict(cls: "Settings", config_dict: dict) -> "Settings":
        return super().from_config_dict(config_dict)

    @property
    def unit_multiplier(self) -> float:
        return 1000 if self.unit_is_mm else 1

    @property
    def unit_str(self) -> str:
        return "[mm]" if self.unit_is_mm else "[m]"

    def to_file(self, filename: str) -> None:
        with open(filename, "w") as file:
            yaml.dump(self.to_dict(), file)

    @classmethod
    def from_config_dict(cls: "PlotSettings", config_dict: dict) -> "PlotSettings":
        return field_extractor(config_class=cls(), config_dict=config_dict, fill_missing_with={"default": None})

    @classmethod
    def from_file(cls: "PlotSettings", filename: str) -> "PlotSettings":
        return cls.from_config_dict(config_dict=yaml2dict(filename))

    def reset(self) -> None:
        self.__init__()
