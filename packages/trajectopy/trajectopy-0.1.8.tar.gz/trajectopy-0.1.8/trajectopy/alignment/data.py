"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2023
mail@gtombrink.de
"""
import copy
from dataclasses import dataclass
import logging
import numpy as np
from trajectopy.evaluation.matching import match_trajectories
from trajectopy.trajectory import Trajectory
from trajectopy.util.datahandling import gradient_3d
from trajectopy.settings.alignment_settings import AlignmentSettings
from trajectopy.util.spatialsorter import Sorting

logger = logging.getLogger("root")


@dataclass
class ObservationContainer:
    xyz_from: np.ndarray
    xyz_to: np.ndarray
    euler: np.ndarray
    speed: np.ndarray

    @property
    def x_from(self) -> np.ndarray:
        return self.xyz_from[:, 0]

    @property
    def y_from(self) -> np.ndarray:
        return self.xyz_from[:, 1]

    @property
    def z_from(self) -> np.ndarray:
        return self.xyz_from[:, 2]

    @property
    def x_to(self) -> np.ndarray:
        return self.xyz_to[:, 0]

    @property
    def y_to(self) -> np.ndarray:
        return self.xyz_to[:, 1]

    @property
    def z_to(self) -> np.ndarray:
        return self.xyz_to[:, 2]

    @property
    def speed_x(self) -> np.ndarray:
        return self.speed[:, 0]

    @property
    def speed_y(self) -> np.ndarray:
        return self.speed[:, 1]

    @property
    def speed_z(self) -> np.ndarray:
        return self.speed[:, 2]

    @property
    def euler_x(self) -> np.ndarray:
        return self.euler[:, 0]

    @property
    def euler_y(self) -> np.ndarray:
        return self.euler[:, 1]

    @property
    def euler_z(self) -> np.ndarray:
        return self.euler[:, 2]


class AlignmentData:
    """Class holding the data required for Alignment"""

    def __init__(
        self,
        xyz_from: np.ndarray,
        xyz_to: np.ndarray,
        settings: AlignmentSettings,
        rpy_body: np.ndarray = None,
        rpy_body_to: np.ndarray = None,
        tstamps: np.ndarray = None,
        speed: np.ndarray = None,
    ) -> None:
        """Initializes new AlignmentData instance

        Args:
            xyz_from (np.ndarray): Source coordinates
            xyz_to (np.ndarray): Target coordinates
            rpy_body (np.ndarray): Orientation of the vehicle / platform
            tstamps_to (np.ndarray): Time stamps of the target positions

        Raises:
            DimensionError: Raised when input arrays are not of equal size.
            TrajectoryError: Raised when there are no orientations but leverarm estimation
                             is desired
        """
        if rpy_body is None and settings.estimation_of.leverarm:
            raise ValueError(
                f"align_with: Please provide platform orientations for {settings.estimation_of.short_mode_str} alignment!"
            )

        if tstamps is None and speed is None and settings.estimation_of.time_shift:
            raise ValueError(
                f"align_with: Please provide timestamps or speed of target positions for {settings.estimation_of.short_mode_str} alignment!"
            )

        input_lengths = [len(a) for a in [tstamps, xyz_from, xyz_to, rpy_body, speed] if a is not None]

        if len(set(input_lengths)) != 1:
            raise ValueError("Input array must be of same size!")

        self.xyz_from: np.ndarray = copy.deepcopy(xyz_from)
        self.rotation_center = np.mean(self.xyz_from, axis=0)
        self.xyz_to: np.ndarray = copy.deepcopy(xyz_to)
        self.rpy_body = copy.deepcopy(rpy_body)
        self.rpy_body_to = copy.deepcopy(rpy_body_to)
        self.tstamps = copy.deepcopy(tstamps)
        self.speed = copy.deepcopy(speed) if speed is not None else self.init_speed()
        self.settings = copy.deepcopy(settings)

        self._init_thresholds()
        self._init_variances()

    @classmethod
    def from_trajectories(
        cls: "AlignmentData", traj_from: Trajectory, traj_to: Trajectory, alignment_settings: AlignmentSettings
    ) -> "AlignmentData":
        """Prepare two trajectories for alignment.

        This method will transform two trajectories
        to local coordinates filter the trajectories
        by speed and resample both trajectories to
        the same sampling.

        It returns an AlignmentData instance that can be
        used to perform an Alignment. This method will not
        modify the original trajectories, since it will deep
        copy both.

        Args:
            traj_from (Trajectory): Trajectory that should be
                                    aligned to the other trajectory.
            traj_to (Trajectory): Target trajectory
            alignment_config (AlignmentConfig): Config holding all
                                                alignment settings.

        Returns:
            AlignmentData: Dataclass holding the data needed for
                        an alignment.
        """

        traj_from = traj_from.copy()
        traj_to = traj_to.copy()

        traj_from.set_sorting(sorting=Sorting.CHRONO)
        traj_to.set_sorting(sorting=Sorting.CHRONO)

        # speed filter
        traj_to.apply_index(traj_to.speed >= alignment_settings.preprocessing.min_speed)
        traj_from.apply_index(traj_from.speed >= alignment_settings.preprocessing.min_speed)

        if alignment_settings.preprocessing.time_start != 0 or alignment_settings.preprocessing.time_end != 0:
            time_span = (
                traj_from.tstamps[0] + alignment_settings.preprocessing.time_start,
                traj_from.tstamps[0] + alignment_settings.preprocessing.time_end,
            )
            traj_to.crop(time_span[0], time_span[1])
            traj_from.crop(time_span[0], time_span[1])

        if len(traj_from) == 0 or len(traj_to) == 0:
            raise ValueError("At least one trajectory is empty after preprocessing!")

        match_trajectories(
            traj_test=traj_from, traj_ref=traj_to, settings=alignment_settings.preprocessing.matching_settings
        )

        logger.info(
            f"Using timespan of {traj_from.tstamps[-1] - traj_from.tstamps[0]:.3f} seconds between {traj_from.tstamps[0]:.3f} and {traj_from.tstamps[-1]:.3f}."
        )

        if alignment_settings.estimation_of.leverarm and traj_from.rot is None:
            raise ValueError(
                f"align_with: Please provide platform orientations for {alignment_settings.estimation_of.short_mode_str} alignment!"
            )

        rpy_body = traj_from.rot.as_euler(seq="xyz") if traj_from.rot is not None else None

        return cls(
            xyz_from=traj_from.pos.xyz,
            xyz_to=traj_to.pos.xyz,
            tstamps=traj_from.tstamps,
            rpy_body=rpy_body,
            rpy_body_to=traj_to.rot.as_euler(seq="xyz") if traj_to.rot is not None else None,
            settings=alignment_settings,
            speed=traj_from.speed_3d,
        )

    @property
    def num_points(self) -> int:
        return len(self.xyz_from)

    def init_speed(self) -> np.ndarray:
        """Speed of target trajectory

        Returns:
            np.ndarray: nx3 array containing the speeds in x/y/z directions
        """
        return gradient_3d(self.xyz_from, tstamps=self.tstamps)

    def _init_variances(self) -> None:
        """Sets the variance vectors"""
        variance_dims = (self.num_points, 3)
        self.variances_rpy_body = np.ones(variance_dims) * self.settings.stochastics.var_roll_pitch
        self.variances_rpy_body[:, 2] = np.ones((self.num_points,)) * self.settings.stochastics.var_yaw

        self.variances_xyz_from = np.ones(variance_dims) * self.settings.stochastics.var_xy_from
        self.variances_xyz_from[:, 2] = np.ones((self.num_points,)) * self.settings.stochastics.var_z_from

        self.variances_xyz_to = np.ones(variance_dims) * self.settings.stochastics.var_xy_to
        self.variances_xyz_to[:, 2] = np.ones((self.num_points,)) * self.settings.stochastics.var_z_to

        self.variances_speed_to = np.ones(variance_dims) * self.settings.stochastics.var_speed_to

    def _init_thresholds(self) -> None:
        """Computes thresholds for parameter updates

        This method creates thresholds for each
        type of parameter. Based on a given metric
        threshold, this method will translate those
        to angle and scale thresholds.
        Finally it will put all thresholds together
        to a 11x1 threshold vector
        """
        max_dist_from = np.linalg.norm(np.max(self.xyz_from, axis=0) - np.min(self.xyz_from, axis=0))
        max_dist_to = np.linalg.norm(np.max(self.xyz_to, axis=0) - np.min(self.xyz_to, axis=0))
        max_dist = np.max([max_dist_from, max_dist_to])

        # scale and angle threshold should fit to metric threshold
        scale_and_angle_th = self.settings.metric_threshold / max_dist

        thresholds = np.ones(11)
        thresholds[:3] *= self.settings.metric_threshold
        thresholds[3:7] *= scale_and_angle_th
        thresholds[7] *= self.settings.time_threshold
        thresholds[8:] *= self.settings.metric_threshold
        self.thresholds = thresholds
