"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2023
mail@gtombrink.de
"""
import logging
from typing import Tuple

import numpy as np
from scipy.spatial import KDTree
from trajectopy.settings.comparison_settings import MatchingMethod, MatchingSettings

from trajectopy.trajectory import Trajectory

logger = logging.getLogger("root")


def match_trajectories(
    traj_test: Trajectory, traj_ref: Trajectory, settings: MatchingSettings
) -> Tuple[Trajectory, Trajectory]:
    if settings.method == MatchingMethod.INTERPOLATION:
        traj_test.same_sampling(traj_ref)
        return traj_test, traj_ref

    if settings.method == MatchingMethod.NEAREST_TEMPORAL:
        return match_trajectories_temporal(traj_test=traj_test, traj_ref=traj_ref, max_distance=settings.max_time_diff)

    if settings.method == MatchingMethod.NEAREST_SPATIAL:
        return match_trajectories_spatial(traj_test=traj_test, traj_ref=traj_ref, max_distance=settings.max_distance)


def match_trajectories_temporal(
    traj_test: Trajectory, traj_ref: Trajectory, max_distance: float = 0.01
) -> Tuple[Trajectory, Trajectory]:
    """This method matches both trajectories temporally

    After this operation, both trajectories will have the length of the
    test trajectory. This means, that the reference trajectory may be
    modified.

    Args:
        traj_test (Trajectory): Test trajectory
        traj_ref (Trajectory): Reference trajectory
        max_distance (float, optional): Maximum distance between two timestamps.
                                        Defaults to 0.1.

    Returns:
        Tuple[Trajectory, Trajectory]: Matched trajectories
    """
    tstamps_ref_2d = np.c_[traj_ref.tstamps, np.zeros(traj_ref.tstamps.shape)]
    tstamps_test_2d = np.c_[traj_test.tstamps, np.zeros(traj_test.tstamps.shape)]
    ref_indices, test_indices = kd_matcher(ref=tstamps_ref_2d, test=tstamps_test_2d, max_distance=max_distance)
    logger.info(f"Found {len(ref_indices)} temporal matches")
    return traj_test.apply_index(test_indices), traj_ref.apply_index(ref_indices)


def match_trajectories_spatial(
    traj_test: Trajectory, traj_ref: Trajectory, max_distance: float = None
) -> Tuple[Trajectory, Trajectory]:
    """This method matches both trajectories spatially

    After this operation, both trajectories will have the length of the
    test trajectory. This means, that the reference trajectory may be
    modified.

    Args:
        traj_from (Trajectory): Test trajectory
        traj_to (Trajectory): Reference trajectory
        max_distance (float, optional): Maximum distance between two poses.
                                        Defaults to None. This means all
                                        matches are accepted.

    Returns:
        Tuple[Trajectory, Trajectory]: Matched trajectories
    """
    ref_indices, test_indices = kd_matcher(ref=traj_ref.pos.xyz, test=traj_test.pos.xyz, max_distance=max_distance)
    logger.info(f"Found {len(ref_indices)} spatial matches")
    return traj_test.apply_index(test_indices), traj_ref.apply_index(ref_indices)


def kd_matcher(ref: np.ndarray, test: np.ndarray, max_distance: float = None) -> Tuple[np.ndarray, np.ndarray]:
    """This method matches data using a KDTree

    Args:
        ref (np.ndarray): Reference data
        test (np.ndarray): Test data
        max_distance (float): Maximum distance for a match

    Returns:
        Tuple[np.ndarray, np.ndarray]: Matched indices
    """
    if max_distance is None or max_distance == 0:
        distances, closest_indices = KDTree(ref).query(test, k=1, workers=-1)
    else:
        distances, closest_indices = KDTree(ref).query(test, k=1, workers=-1, distance_upper_bound=max_distance)

    distance_index_matrix = np.array([[not np.isinf(dist), index] for index, dist in enumerate(distances)], dtype=int)
    distance_filter = distance_index_matrix[:, 0].astype(bool)

    if not distance_filter.any():
        raise ValueError("No matches found!")

    return closest_indices[distance_filter], distance_index_matrix[distance_filter, 1]


def rough_timestamp_matching(traj_ref: Trajectory, traj_test: Trajectory, max_distance: float = None) -> float:
    """This method roughly matches two trajectories temporally
    Args:
        traj_from (Trajectory): Test trajectory
        traj_to (Trajectory): Reference trajectory

    Returns:
        float: Mean time offset
    """
    traj_test, traj_ref = match_trajectories_spatial(
        traj_test=traj_test.copy(), traj_ref=traj_ref.copy(), max_distance=max_distance
    )
    mean_time_offset = np.median(traj_ref.tstamps - traj_test.tstamps)
    logger.info(f"Median time offset: {mean_time_offset:.3f} s")
    return mean_time_offset
