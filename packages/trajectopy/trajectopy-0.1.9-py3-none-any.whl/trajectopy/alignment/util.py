"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2023
mail@gtombrink.de
"""
import logging
from typing import Tuple

from trajectopy.alignment.alignment import Alignment
from trajectopy.settings.alignment_settings import AlignmentSettings
from trajectopy.trajectory import Trajectory
from trajectopy.util.rotationset import RotationSet

logger = logging.getLogger("root")


def adopt_first_pose(*, traj_from: Trajectory, traj_to: Trajectory) -> Trajectory:
    """Transform trajectory so that the first pose is identical in both

    Args:
        traj_from (Trajectory): Trajectory to be transformed
        traj_to (Trajectory): Target Trajectory

    Returns:
        Trajectory: Transformed trajectory
    """
    adopt_first_position(traj_from=traj_from, traj_to=traj_to)
    adopt_first_orientation(traj_from=traj_from, traj_to=traj_to)
    return traj_from


def adopt_first_position(*, traj_from: Trajectory, traj_to: Trajectory) -> Trajectory:
    """Transform trajectory so that the first position is identical in both

    Args:
        traj_from (Trajectory): Trajectory to be transformed
        traj_to (Trajectory): Target Trajectory

    Returns:
        Trajectory: Transformed trajectory
    """
    position_difference = traj_to.pos.xyz[0, :] - traj_from.pos.xyz[0, :]
    traj_from.pos.xyz += position_difference
    return traj_from


def adopt_first_orientation(*, traj_from: Trajectory, traj_to: Trajectory) -> Trajectory:
    """Transform trajectory so that the first orientation is identical in both

    Args:
        traj_from (Trajectory): Trajectory to be transformed
        traj_to (Trajectory): Target Trajectory

    Returns:
        Trajectory: Transformed trajectory
    """
    if None not in [traj_to.rot, traj_from.rot]:
        rpy_from = traj_from.rot.as_euler(seq="xyz")
        rotation_difference = traj_to.rot.as_euler(seq="xyz")[0, :] - rpy_from[0, :]

        traj_from.rot = RotationSet.from_euler(seq="xyz", angles=rpy_from + rotation_difference)

    return traj_from


def align_trajectories(
    *, traj_from: Trajectory, traj_to: Trajectory, alignment_settings: AlignmentSettings
) -> Tuple[Trajectory, Alignment]:
    """Aligns two trajectories

    Performs a
    - Helmert
    - Leverarm
    - Time shift

    estimation depending on the configuration.
    After this, the estimated parameters are applied
    to the 'traj_from' trajectory.

    Args:
        traj_from (Trajectory)
        traj_to (Trajectory)
        alignment_config (AlignmentConfig): Configuration holding all
                                            relevant settings for aligning
                                            the trajectories.

    Returns:
        Tuple[Trajectory, Trajectory]: Aligned trajectories
    """
    # one of the trajectories is in an unknown datum
    if (
        None in [traj_to.pos.local_transformer, traj_to.pos.local_transformer]
        and not alignment_settings.estimation_of.helmert
    ):
        print(
            "\n ____________________________________________________\n"
            "| --------------------- WARNING --------------------- |\n"
            f"| {'One of the trajectories is in an unknown datum.':<51} |\n"
            f"| {'However, according to the configuration, no Helmert':<51} |\n"
            f"| {'transformation should be performed.':<51} |\n"
            f"| {'Consider performing a Helmert transformation.':<51} |\n"
            "|_____________________________________________________|\n"
        )
    logger.info("Aligning trajectories ...")

    alignment = Alignment(
        traj_from=traj_from,
        traj_to=traj_to,
        settings=alignment_settings,
    )

    traj_from.apply_alignment(alignment_parameters=alignment.est_params)

    return traj_from, alignment
