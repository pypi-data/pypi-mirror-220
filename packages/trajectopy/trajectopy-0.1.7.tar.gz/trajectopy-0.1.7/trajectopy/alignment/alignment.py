"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2023
mail@gtombrink.de
"""
import copy
import logging
from typing import Tuple

import numpy as np
from numpy import matlib
from scipy.sparse import csc_matrix, spdiags
from scipy.sparse.linalg import spsolve
from scipy.stats.distributions import chi2
from trajectopy.alignment.direct_helmert_transformation import direct_helmert_transformation

from trajectopy.alignment.data import AlignmentData, ObservationContainer
from trajectopy.alignment.functional_model.interface import FunctionalRelationship
from trajectopy.alignment.parameters import AlignmentParameters, HelmertTransformation, Leverarm, Parameter
from trajectopy.settings.alignment_settings import AlignmentSettings
from trajectopy.alignment.direct_leverarm import direct_leverarm
from trajectopy.alignment.direct_timeshift import direct_timeshift
from trajectopy.trajectory import Trajectory
from trajectopy.util.definitions import Unit
from trajectopy.util.printing import dict2table

# logger configuration
logger = logging.getLogger("root")


OBSERVATION_GROUPS: dict[str, Tuple[int, int]] = {
    "XY_FROM": (0, 2),
    "Z_FROM": (2, 3),
    "XYZ_FROM": (0, 3),
    "XY_TO": (3, 5),
    "Z_TO": (5, 6),
    "XYZ_TO": (3, 6),
    "POSITIONS": (0, 6),
    "ROLL_PITCH": (6, 8),
    "YAW": (8, 9),
    "RPY": (6, 9),
    "SPEED": (9, 12),
}

POSITION_VARIANCE_GROUPS: list[str] = ["XY_FROM", "Z_FROM", "XY_TO", "Z_TO"]
ORIENTATION_VARIANCE_GROUPS: list[str] = ["ROLL_PITCH", "YAW"]
SPEED_VARIANCE_GROUP: list[str] = ["SPEED"]


class AlignmentError(Exception):
    pass


class Alignment:
    """Class representing the alignment of two trajectories

    This class will align two trajectories using a combination
    of a 3d Helmert-transformation, a leverarm estimation and a
    time-shift estimation.

    It can fully align two trajectories their separation can be
    described by:
    - a translational shift
    - a rotation of the positions
    - a rotation of the orientations (rotation of the n-frame)
    - a scale factor
    - a time shift
    - a leverarm (e.g. mounted at different locations on the platform)
    """

    def __init__(
        self,
        traj_from: Trajectory,
        traj_to: Trajectory,
        settings: AlignmentSettings,
    ) -> None:
        """Constructor

        This method prepares the data and performs an trajectory alignment

        Args:
            alignment_data (AlignmentData): Stores all data required for the alignment
            mode (AlignmentMode, optional): Indicates the desired mode, i.e. whether a
                                            - helmert transformation
                                            - scale estimation
                                            - leverarm estimation
                                            - time shift estimation
                                            should be performed
            error_probability (float, optional): Used for the stochastic global test.
                                                 Defaults to 0.05.
        """
        self.funcrel = FunctionalRelationship()
        self.traj_from = traj_from.copy()
        self.traj_to = traj_to.copy()
        self.settings = settings
        self._setup_alignment()

        logger.info("Initialized Alignment!")
        logger.info(self)
        logger.info("Performing alignment...")
        if settings.estimation_of.all_disabled:
            logger.warning("Nothing to estimate since all parameters are disabled")
            return

        self._estimation_process()
        print_summary(self)

    def __str__(self) -> str:
        return settings_str(self)

    @property
    def data(self) -> AlignmentData:
        return self._data

    def _build_data_object(self) -> None:
        """Builds the data object

        This method builds the data object which is used for the alignment

        Returns:
            AlignmentData: Stores all data required for the alignment
        """
        self._data = AlignmentData.from_trajectories(self.traj_from, self.traj_to, alignment_settings=self.settings)

    def _setup_alignment(self) -> None:
        """Sets up the alignment

        This method sets up the alignment by
        - building the data object
        - setting up the parameters
        - setting up the variance groups
        """
        self._build_data_object()
        self._set_variances()
        self._set_parameters()

    def _set_parameters(self) -> None:
        """Sets up the parameters"""
        self._est_params = self.init_parameters()
        self._residuals = None
        self._est_obs = None
        self._has_results = False
        self._converged = False

    def _set_variances(self) -> None:
        """Sets up the variances"""
        self.variance_groups = self.init_variance_groups()
        self.variances = self.init_variances()
        self._group_variance_factors = [np.Inf] * len(self.variance_groups)
        logging.debug(dict2table(self.group_stds, title="Group Standard Deviations (a-priori)"))

    def init_variance_groups(self) -> list[str]:
        variance_groups = copy.deepcopy(POSITION_VARIANCE_GROUPS)

        if self.settings.estimation_of.leverarm_enabled:
            variance_groups.extend(ORIENTATION_VARIANCE_GROUPS)

        if self.settings.estimation_of.time_shift_enabled:
            variance_groups.extend(SPEED_VARIANCE_GROUP)
            OBSERVATION_GROUPS["SPEED"] = (9, 12) if self.settings.estimation_of.leverarm_enabled else (6, 9)

        return variance_groups

    def _estimation_process(self) -> None:
        """Handles the estimation of the parameters

        Calls either robust reweighting or variance
        estimation methods.
        """
        self._estimate_parameters()
        self.variance_component_estimation()
        self.variance_estimation()
        self._has_results = True

    @property
    def has_results(self) -> bool:
        return self._has_results

    @property
    def residuals(self) -> np.ndarray:
        return self._residuals

    @property
    def est_obs(self) -> np.ndarray:
        return self._est_obs

    @property
    def est_params(self) -> AlignmentParameters:
        return self._est_params

    @property
    def group_variance_factors(self) -> list[float]:
        return self._group_variance_factors

    @property
    def num_obs_per_epoch(self) -> int:
        return len(self.observations) // self.data.num_points

    @property
    def redundancy(self) -> int:
        return len(self.observations) - self._est_params.num_enabled

    @property
    def observations(self) -> np.ndarray:
        """Returns the correct observation vector

        The observation vector always consists
        of the source and target positions and
        may also include the platform orientations,
        depening on whether the leverarm should
        be also estimated.

        [
         x_from, y_from, z_from,
         x_to, y_to, z_to,
         roll_body, pitch_body, yaw_body,
         ...
        ]

        Returns:
            np.ndarray: observation vector
        """
        obs_init: np.ndarray = np.c_[self.data.xyz_from, self.data.xyz_to]
        if self.settings.estimation_of.leverarm_enabled:
            obs_init = np.c_[obs_init, self.data.rpy_body]

        if self.settings.estimation_of.time_shift_enabled:
            obs_init = np.c_[obs_init, self.data.speed]
        return np.reshape(obs_init, (obs_init.size, 1))

    def init_parameters(self) -> AlignmentParameters:
        """This method computes initial parameters
        for the iterative adjustment

        For this, the helmert transformation and
        the leverarm estimation are done separatetly
        using methods that do not require inital
        parameters.

        Returns:
            AlignmentParameters: Hold the estimates parameters.
                                 14 = 7 (helmert+scale) 3 (leverarm) 1 (time) 3 (orientation)
        """
        if self.settings.estimation_of.helmert_enabled:
            helmert_init = direct_helmert_transformation(xyz_from=self.data.xyz_from, xyz_to=self.data.xyz_to)
            xyz_init = helmert_init.apply_to(self.data.xyz_from)
        else:
            helmert_init = HelmertTransformation()
            xyz_init = self.data.xyz_from

        if self.settings.estimation_of.time_shift_enabled and not self.settings.estimation_of.leverarm_enabled:
            time_shift_init, _ = direct_timeshift(xyz_from=xyz_init, xyz_to=self.data.xyz_to, speed=self.speed)
        else:
            time_shift_init = Parameter(value=0.0, name="Time shift", unit=Unit.SECOND)

        if self.data.rpy_body is None or not self.settings.estimation_of.leverarm_enabled:
            leverarm_init = Leverarm()
        else:
            leverarm_init, time_shift_init, _ = direct_leverarm(
                speed=self.data.speed if self.settings.estimation_of.time_shift_enabled else None,
                xyz_from=xyz_init,
                xyz_to=self.data.xyz_to,
                rpy_body=self.data.rpy_body,
            )

        alignparams = AlignmentParameters(
            sim_trans_x=helmert_init.trans_x,
            sim_trans_y=helmert_init.trans_y,
            sim_trans_z=helmert_init.trans_z,
            sim_rot_x=helmert_init.rot_x,
            sim_rot_y=helmert_init.rot_y,
            sim_rot_z=helmert_init.rot_z,
            sim_scale=helmert_init.scale,
            time_shift=time_shift_init,
            lever_x=leverarm_init.x,
            lever_y=leverarm_init.y,
            lever_z=leverarm_init.z,
        )

        alignparams.apply_settings(self.settings.estimation_of)
        return alignparams

    @property
    def speed(self) -> np.ndarray:
        """
        This method returns the speed of the platform
        in m/s.

        Unlike data.speed, this method filters the
        speed matrix depending on the alignment settings.
        If for example 'use_x_speed' is set to False,
        the first column of the speed matrix will contain
        only zeros. In this way, the x speed will not affect
        any computations.

        Returns:
            np.ndarray: Speed matrix nx3
        """
        speed_filtered = np.zeros((self.data.speed.shape))
        speed_filtered[:, self.settings.estimation_of.time_shift_filter] = self.data.speed[
            :, self.settings.estimation_of.time_shift_filter
        ]

        return speed_filtered

    def init_variances(self) -> np.ndarray:
        """Sets up the variance vector

        Its size depends on whether the
        leverarm should be estimated or
        not. In this case, not only the
        source and the target positions
        are relevant but also the platform
        orientations. Also, when estimating
        the time shift, the platform speed
        is also considered.

        Returns:
            np.ndarray: variance vector
        """

        num_of_variances = self.data.xyz_to.size + self.data.xyz_from.size
        if self.settings.estimation_of.leverarm_enabled:
            num_of_variances += self.data.rpy_body.size

        if self.settings.estimation_of.time_shift_enabled:
            num_of_variances += self.data.speed.size

        variances = np.ones((num_of_variances,))

        self._set_group(
            input=variances,
            values=self.data.variances_xyz_from,
            group_indices=OBSERVATION_GROUPS["XYZ_FROM"],
        )
        self._set_group(
            input=variances,
            values=self.data.variances_xyz_to,
            group_indices=OBSERVATION_GROUPS["XYZ_TO"],
        )

        if self.settings.estimation_of.leverarm_enabled:
            self._set_group(
                input=variances,
                values=self.data.variances_rpy_body,
                group_indices=OBSERVATION_GROUPS["RPY"],
            )

        if self.settings.estimation_of.time_shift_enabled:
            self._set_group(
                input=variances, values=self.data.variances_speed_to, group_indices=OBSERVATION_GROUPS["SPEED"]
            )
        return variances

    def _get_group(self, input: np.ndarray, group_indices: Tuple[int, int]) -> np.ndarray:
        return tuple(input[i :: self.num_obs_per_epoch].ravel() for i in range(group_indices[0], group_indices[1]))

    def _set_group(self, input: np.ndarray, values: np.ndarray, group_indices: Tuple[int, int]) -> None:
        if values.shape[1] != group_indices[1] - group_indices[0]:
            raise ValueError("Input array should have 1 column for each index defined by group_indices range!")

        for col_index, i in enumerate(range(group_indices[0], group_indices[1])):
            input[i :: self.num_obs_per_epoch] = values[:, col_index]

    @property
    def group_stds(self) -> dict[str, float]:
        group_std_dict = {}

        for group_key in self.variance_groups:
            group_indices = OBSERVATION_GROUPS[group_key]
            group_std_dict[group_key] = np.mean(
                np.sqrt(self._get_group(input=self.variances, group_indices=group_indices))
            )

        return group_std_dict

    @property
    def sigma_ll(self):
        return spdiags(self.variances, 0, len(self.variances), len(self.variances))

    def convert_to_observation_container(self, observations: np.ndarray) -> ObservationContainer:
        x_from, y_from, z_from = self._get_group(input=observations, group_indices=OBSERVATION_GROUPS["XYZ_FROM"])
        x_to, y_to, z_to = self._get_group(input=observations, group_indices=OBSERVATION_GROUPS["XYZ_TO"])

        if self.settings.estimation_of.leverarm_enabled:
            roll, pitch, yaw = self._get_group(input=observations, group_indices=OBSERVATION_GROUPS["RPY"])
        else:
            roll, pitch, yaw = np.zeros((x_from.size,)), np.zeros((x_from.size,)), np.zeros((x_from.size,))

        if self.settings.estimation_of.time_shift_enabled:
            x_speed, y_speed, z_speed = self._get_group(input=observations, group_indices=OBSERVATION_GROUPS["SPEED"])
        else:
            x_speed, y_speed, z_speed = np.zeros((x_from.size,)), np.zeros((x_from.size,)), np.zeros((x_from.size,))

        return ObservationContainer(
            xyz_from=np.c_[x_from, y_from, z_from],
            xyz_to=np.c_[x_to, y_to, z_to],
            speed=np.c_[x_speed, y_speed, z_speed],
            euler=np.c_[roll, pitch, yaw],
        )

    @property
    def variance_factor(self) -> float:
        return (self._residuals.T @ spsolve(csc_matrix(self.sigma_ll), self._residuals)) / self.redundancy

    @property
    def _condition_xyz_to(self) -> np.ndarray:
        """
        Helper function returning the constant xyz_to component of
        the condition matrix
        """
        return [
            np.c_[
                -np.ones((self.data.num_points, 1)),
                np.zeros((self.data.num_points, 1)),
                np.zeros((self.data.num_points, 1)),
            ],
            np.c_[
                np.zeros((self.data.num_points, 1)),
                -np.ones((self.data.num_points, 1)),
                np.zeros((self.data.num_points, 1)),
            ],
            np.c_[
                np.zeros((self.data.num_points, 1)),
                np.zeros((self.data.num_points, 1)),
                -np.ones((self.data.num_points, 1)),
            ],
        ]

    def variance_component_estimation(self) -> dict[str, bool]:
        """Performs an estimation of the variances for different observation groups

        The observations groups are:
            - x and y components of xyz_from
            - z component of xyz_from
            - x and y components of xyz_to
            - z component of xyz_to
            - roll / pitch components of rpy_body
            - yaw component of rpy_body
            - speed (at target positions)

        """
        variances_changed = True
        cnt = 0
        while variances_changed:
            group_global_tests: dict[str, bool] = {}
            for i, group_key in enumerate(self.variance_groups):
                group_indices = OBSERVATION_GROUPS[group_key]
                group_variances = np.c_[self._get_group(input=self.variances, group_indices=group_indices)]
                group_residuals = np.c_[self._get_group(input=self._residuals, group_indices=group_indices)]
                group_redundancy = (
                    group_residuals.size
                )  # here I take a shortcut (If there are a lot of observations, the redundancy can be approximated by the number of observations)
                group_variance_factor = (
                    np.sum(group_residuals * np.reciprocal(group_variances) * group_residuals) / group_redundancy
                )

                group_global_test = self._global_test(variance=group_variance_factor, redundancy=group_redundancy)

                # global test for group
                if not group_global_test:
                    # only scale if global test gets denied otherwise I can assume that
                    # our a-priori model is correct
                    self._set_group(
                        input=self.variances,
                        values=group_variances * group_variance_factor,
                        group_indices=group_indices,
                    )

                group_global_tests |= {group_key: group_global_test}
                self._group_variance_factors[i] = group_variance_factor

            if variances_changed := any(not value for _, value in group_global_tests.items()):
                self._estimate_parameters()

            if cnt > 15:
                logging.warning("Breaking out of variance component estimation loop.")
                break

        logger.debug("Finished with variance component estimation.")
        logging.debug(dict2table(group_global_tests, title="Group Global Test Results"))
        return group_global_tests

    def variance_estimation(self, at_least_once: bool = False) -> None:
        cnt = 0
        global_test_result = self._global_test(variance=self.variance_factor, redundancy=self.redundancy)
        while not global_test_result or at_least_once:
            self.variances *= self.variance_factor
            self._estimate_parameters()
            global_test_result = self._global_test(variance=self.variance_factor, redundancy=self.redundancy)
            at_least_once = False
            if cnt > 15:
                logging.warning("Breaking out of global test loop.")
                break

        logger.debug(f"Global test result: {global_test_result}")

    def _global_test(self, variance: float, redundancy: int) -> bool:
        tau = variance * redundancy
        quantile = chi2.ppf(1 - self.settings.stochastics.error_probability, redundancy)

        logger.debug(
            f"Global test passed: {tau <= quantile}, quantile: {quantile:.3f}, test value: {tau:.3f}, variance factor: {self.variance_factor:.3f}"
        )
        return tau <= quantile

    def _estimate_parameters(self) -> None:
        """Helmert-Leverarm-Time Transformation using the Gauß-Helmert-Model

        The observation-equations are sorted in the following way:
        [X, Y, Z, X, Y, Z, ..., X, Y, Z]
        """
        # obs = [x_from, y_from, z_from, x_to, y_to, z_to, roll_body, pitch_body, yaw_body]

        # preparation for iterative adjustment
        est_params = self._est_params
        delta_params = [np.inf] * len(est_params)

        est_obs = copy.deepcopy(self.observations)
        contradiction_w = self._auto_functional_relationship(parameters=est_params, observations=est_obs)

        it_counter = 0
        self._converged = True
        while any(abs(value) > threshold for value, threshold in zip(delta_params, self.data.thresholds)):
            a_design = self.auto_design_matrix(parameters=est_params, observations=est_obs)

            # filter design matrix
            a_design = a_design[:, self.settings.estimation_of.parameter_filter]

            b_cond = self._condition_matrix(parameters=est_params, observations=est_obs)

            bbt = b_cond @ self.sigma_ll @ b_cond.T

            # solve normal equations
            delta_params = self._compute_parameter_deltas(contradiction_w, a_design, bbt)
            correlates_k = -spsolve(bbt, a_design @ delta_params + contradiction_w)
            residuals = self.sigma_ll @ b_cond.T @ correlates_k

            # update
            est_params.values_enabled += delta_params

            est_obs = self.observations + residuals[:, None]

            contradiction_w = (
                self._auto_functional_relationship(parameters=est_params, observations=est_obs)
                - b_cond @ residuals.ravel()
            )

            it_counter += 1

            if it_counter > 15:
                logger.error(
                    f"Adjustment does not converge! Maximum parameter update: {np.max(np.abs(delta_params)):.3e}"
                )
                self._converged = False
                break

        logger.debug(f"Iterations: {it_counter}")
        self._est_params = est_params
        self._est_obs = est_obs
        self._residuals = residuals
        self._compute_parameter_variances(a_design, bbt)

    def _compute_parameter_variances(self, a_design: csc_matrix, bbt: csc_matrix) -> None:
        sigma_xx_inv: csc_matrix = a_design.T @ spsolve(bbt, a_design)
        if sigma_xx_inv.size == 1:
            self._est_params.set_covariance_matrix(np.reciprocal(sigma_xx_inv[:, None]))
        else:
            self._est_params.set_covariance_matrix(np.linalg.pinv(sigma_xx_inv.toarray()))

    def _compute_parameter_deltas(
        self, contradiction_w: np.ndarray, a_design: csc_matrix, bbt: csc_matrix
    ) -> np.ndarray:
        if a_design.shape[1] == 1:
            return -(a_design.T @ spsolve(bbt, contradiction_w)) / (a_design.T @ spsolve(bbt, a_design))

        return -spsolve(a_design.T @ spsolve(bbt, a_design), a_design.T @ spsolve(bbt, contradiction_w))

    def auto_design_matrix(self, parameters: AlignmentParameters, observations: np.ndarray) -> csc_matrix:
        observation_container = self.convert_to_observation_container(observations)
        a_design = np.zeros((self.data.num_points * 3, 11))
        a_design[0::3, :] = self._auto_design_x(parameters, observation_container)
        a_design[1::3, :] = self._auto_design_y(parameters, observation_container)
        a_design[2::3, :] = self._auto_design_z(parameters, observation_container)
        return csc_matrix(a_design)

    def _auto_design_z(
        self, parameters: AlignmentParameters, observation_container: ObservationContainer
    ) -> np.ndarray:
        return np.c_[
            np.zeros((self.data.num_points, 1)),
            np.zeros((self.data.num_points, 1)),
            self.funcrel.eval(
                func=self.funcrel.dz_dsim_trans_z, parameters=parameters, observations=observation_container
            ),
            self.funcrel.eval(
                func=self.funcrel.dz_dsim_rot_x, parameters=parameters, observations=observation_container
            ),
            self.funcrel.eval(
                func=self.funcrel.dz_dsim_rot_y, parameters=parameters, observations=observation_container
            ),
            np.zeros((self.data.num_points, 1)),
            self.funcrel.eval(
                func=self.funcrel.dz_dsim_scale, parameters=parameters, observations=observation_container
            ),
            self.funcrel.eval(
                func=self.funcrel.dz_dtime_shift, parameters=parameters, observations=observation_container
            ),
            self.funcrel.eval(
                func=self.funcrel.dz_dlever_x, parameters=parameters, observations=observation_container
            ),
            self.funcrel.eval(
                func=self.funcrel.dz_dlever_y, parameters=parameters, observations=observation_container
            ),
            self.funcrel.eval(
                func=self.funcrel.dz_dlever_z, parameters=parameters, observations=observation_container
            ),
        ]

    def _auto_design_y(
        self, parameters: AlignmentParameters, observation_container: ObservationContainer
    ) -> np.ndarray:
        return np.c_[
            np.zeros((self.data.num_points, 1)),
            self.funcrel.eval(
                func=self.funcrel.dy_dsim_trans_y, parameters=parameters, observations=observation_container
            ),
            np.zeros((self.data.num_points, 1)),
            self.funcrel.eval(
                func=self.funcrel.dy_dsim_rot_x, parameters=parameters, observations=observation_container
            ),
            self.funcrel.eval(
                func=self.funcrel.dy_dsim_rot_y, parameters=parameters, observations=observation_container
            ),
            self.funcrel.eval(
                func=self.funcrel.dy_dsim_rot_z, parameters=parameters, observations=observation_container
            ),
            self.funcrel.eval(
                func=self.funcrel.dy_dsim_scale, parameters=parameters, observations=observation_container
            ),
            self.funcrel.eval(
                func=self.funcrel.dy_dtime_shift, parameters=parameters, observations=observation_container
            ),
            self.funcrel.eval(
                func=self.funcrel.dy_dlever_x, parameters=parameters, observations=observation_container
            ),
            self.funcrel.eval(
                func=self.funcrel.dy_dlever_y, parameters=parameters, observations=observation_container
            ),
            self.funcrel.eval(
                func=self.funcrel.dy_dlever_z, parameters=parameters, observations=observation_container
            ),
        ]

    def _auto_design_x(
        self, parameters: AlignmentParameters, observation_container: ObservationContainer
    ) -> np.ndarray:
        return np.c_[
            self.funcrel.eval(
                func=self.funcrel.dx_dsim_trans_x, parameters=parameters, observations=observation_container
            ),
            np.zeros((self.data.num_points, 1)),
            np.zeros((self.data.num_points, 1)),
            self.funcrel.eval(
                func=self.funcrel.dx_dsim_rot_x, parameters=parameters, observations=observation_container
            ),
            self.funcrel.eval(
                func=self.funcrel.dx_dsim_rot_y, parameters=parameters, observations=observation_container
            ),
            self.funcrel.eval(
                func=self.funcrel.dx_dsim_rot_z, parameters=parameters, observations=observation_container
            ),
            self.funcrel.eval(
                func=self.funcrel.dx_dsim_scale, parameters=parameters, observations=observation_container
            ),
            self.funcrel.eval(
                func=self.funcrel.dx_dtime_shift, parameters=parameters, observations=observation_container
            ),
            self.funcrel.eval(
                func=self.funcrel.dx_dlever_x, parameters=parameters, observations=observation_container
            ),
            self.funcrel.eval(
                func=self.funcrel.dx_dlever_y, parameters=parameters, observations=observation_container
            ),
            self.funcrel.eval(
                func=self.funcrel.dx_dlever_z, parameters=parameters, observations=observation_container
            ),
        ]

    def _auto_functional_relationship(self, parameters: AlignmentParameters, observations: np.ndarray) -> np.ndarray:
        # accounting for the time shift not by using the velocity model but by shifting the time stamps and re-interpolating
        observation_container = self.convert_to_observation_container(observations)
        func_xyz = np.zeros((self.data.num_points * 3,))
        func_xyz[::3] = self.funcrel.eval(
            func=self.funcrel.x, parameters=parameters, observations=observation_container
        )
        func_xyz[1::3] = self.funcrel.eval(
            func=self.funcrel.y, parameters=parameters, observations=observation_container
        )
        func_xyz[2::3] = self.funcrel.eval(
            func=self.funcrel.z, parameters=parameters, observations=observation_container
        )
        return func_xyz

    def _condition_matrix(self, parameters: AlignmentParameters, observations: np.ndarray) -> csc_matrix:
        """Computes the condition-matrix for the Gauß-Helmert-Model

        The matrix contains the derivatives of the
        observation equations with respect to the observations.

        Depending on whether the lever arm is to be estimated,
        additional columns are added to the condition matrix
        corresponding to the derivation of the functional
        relationship with respect to the platform orientations.

        Its dimensions are:
            [#Obs.-Equations x #Observations]

            #Obs.-Equations: 3 * #Points

        This matrix is sparse.

        Args:
            parameters (AlignmentParameters): (current) estimated parameters
            observations (np.ndarray): (current) estimated observations

        Returns:
            csc_matrix: sparse condition matrix
        """
        cond_xyz = self._get_condition_stack(parameters=parameters, observations=observations)

        # row indices
        # [0,0,0,0,0,0; 1,1,1,1,1,1; 2,2,2,2,2,2; 3,3,3,3,3,3; ...]
        row_idx = np.repeat(np.arange(0, self.data.num_points * 3, 1), self.num_obs_per_epoch)

        # column indices [0,1,2,3,4,5; 6,7,8,9,10,11; 12,13,14,15,16,17; ...]
        col_idx_matrix = (
            matlib.repmat(np.arange(0, self.num_obs_per_epoch), self.data.num_points * 3, 1)
            + np.repeat(
                np.arange(
                    0,
                    self.data.num_points * self.num_obs_per_epoch,
                    self.num_obs_per_epoch,
                ),
                3,
            )[:, None]
        )
        col_idx = np.reshape(col_idx_matrix, (col_idx_matrix.size,))

        return csc_matrix((np.reshape(cond_xyz, (cond_xyz.size,)), (row_idx, col_idx)))

    def _get_condition_stack(self, parameters: AlignmentParameters, observations: np.ndarray) -> np.ndarray:
        """Helper function to get the non-zero data of the condition matrix

        Depending on which parameters are estimated, this function returns
        different data.

        Args:
            parameters (AlignmentParameters): (current) estimated parameters
            observations (np.ndarray): (current) estimated observations

        Returns:
            np.ndarray: condition matrix data
        """
        xyz_from_component = self._auto_condition_xyz_from(parameters=parameters, observations=observations)

        rpy_body_component = (
            self._auto_condition_rpy_body(parameters, observations)
            if self.settings.estimation_of.leverarm_enabled
            else None
        )

        speed_to_component = (
            self._auto_condition_speed_to(parameters, observations)
            if self.settings.estimation_of.time_shift_enabled
            else None
        )

        if self.settings.estimation_of.leverarm_enabled and not self.settings.estimation_of.time_shift_enabled:
            return np.column_stack(
                [
                    np.c_[
                        xyz_from_component[i],
                        self._condition_xyz_to[i],
                        rpy_body_component[i],
                    ]
                    for i in range(3)
                ]
            )

        if self.settings.estimation_of.time_shift_enabled and not self.settings.estimation_of.leverarm_enabled:
            return np.column_stack(
                [
                    np.c_[
                        xyz_from_component[i],
                        self._condition_xyz_to[i],
                        speed_to_component[i],
                    ]
                    for i in range(3)
                ]
            )

        if self.settings.estimation_of.leverarm_enabled and self.settings.estimation_of.time_shift_enabled:
            return np.column_stack(
                [
                    np.c_[
                        xyz_from_component[i],
                        self._condition_xyz_to[i],
                        rpy_body_component[i],
                        speed_to_component[i],
                    ]
                    for i in range(3)
                ]
            )

        return np.column_stack(
            [
                np.c_[
                    xyz_from_component[i],
                    self._condition_xyz_to[i],
                ]
                for i in range(3)
            ]
        )

    def _auto_condition_rpy_body(self, parameters: AlignmentParameters, observations: np.ndarray) -> np.ndarray:
        observation_container = self.convert_to_observation_container(observations)
        return [
            np.c_[
                self.funcrel.eval(
                    func=self.funcrel.dx_deuler_x, parameters=parameters, observations=observation_container
                ),
                self.funcrel.eval(
                    func=self.funcrel.dx_deuler_y, parameters=parameters, observations=observation_container
                ),
                self.funcrel.eval(
                    func=self.funcrel.dx_deuler_z, parameters=parameters, observations=observation_container
                ),
            ],
            np.c_[
                self.funcrel.eval(
                    func=self.funcrel.dy_deuler_x, parameters=parameters, observations=observation_container
                ),
                self.funcrel.eval(
                    func=self.funcrel.dy_deuler_y, parameters=parameters, observations=observation_container
                ),
                self.funcrel.eval(
                    func=self.funcrel.dy_deuler_z, parameters=parameters, observations=observation_container
                ),
            ],
            np.c_[
                self.funcrel.eval(
                    func=self.funcrel.dz_deuler_x, parameters=parameters, observations=observation_container
                ),
                self.funcrel.eval(
                    func=self.funcrel.dz_deuler_y, parameters=parameters, observations=observation_container
                ),
                self.funcrel.eval(
                    func=self.funcrel.dz_deuler_z, parameters=parameters, observations=observation_container
                ),
            ],
        ]

    def _auto_condition_xyz_from(self, parameters: AlignmentParameters, observations: np.ndarray) -> np.ndarray:
        observation_container = self.convert_to_observation_container(observations)
        return [
            np.c_[
                self.funcrel.eval(
                    func=self.funcrel.dx_dx_from, parameters=parameters, observations=observation_container
                ),
                self.funcrel.eval(
                    func=self.funcrel.dx_dy_from, parameters=parameters, observations=observation_container
                ),
                self.funcrel.eval(
                    func=self.funcrel.dx_dz_from, parameters=parameters, observations=observation_container
                ),
            ],
            np.c_[
                self.funcrel.eval(
                    func=self.funcrel.dy_dx_from, parameters=parameters, observations=observation_container
                ),
                self.funcrel.eval(
                    func=self.funcrel.dy_dy_from, parameters=parameters, observations=observation_container
                ),
                self.funcrel.eval(
                    func=self.funcrel.dy_dz_from, parameters=parameters, observations=observation_container
                ),
            ],
            np.c_[
                self.funcrel.eval(
                    func=self.funcrel.dz_dx_from, parameters=parameters, observations=observation_container
                ),
                self.funcrel.eval(
                    func=self.funcrel.dz_dy_from, parameters=parameters, observations=observation_container
                ),
                self.funcrel.eval(
                    func=self.funcrel.dz_dz_from, parameters=parameters, observations=observation_container
                ),
            ],
        ]

    def _auto_condition_speed_to(self, parameters: AlignmentParameters, observations: np.ndarray) -> np.ndarray:
        observation_container = self.convert_to_observation_container(observations)
        return [
            np.c_[
                self.funcrel.eval(
                    func=self.funcrel.dx_dspeed_x, parameters=parameters, observations=observation_container
                ),
                self.funcrel.eval(
                    func=self.funcrel.dx_dspeed_y, parameters=parameters, observations=observation_container
                ),
                self.funcrel.eval(
                    func=self.funcrel.dx_dspeed_z, parameters=parameters, observations=observation_container
                ),
            ],
            np.c_[
                self.funcrel.eval(
                    func=self.funcrel.dy_dspeed_x, parameters=parameters, observations=observation_container
                ),
                self.funcrel.eval(
                    func=self.funcrel.dy_dspeed_y, parameters=parameters, observations=observation_container
                ),
                self.funcrel.eval(
                    func=self.funcrel.dy_dspeed_z, parameters=parameters, observations=observation_container
                ),
            ],
            np.c_[
                self.funcrel.eval(
                    func=self.funcrel.dz_dspeed_x, parameters=parameters, observations=observation_container
                ),
                self.funcrel.eval(
                    func=self.funcrel.dz_dspeed_y, parameters=parameters, observations=observation_container
                ),
                self.funcrel.eval(
                    func=self.funcrel.dz_dspeed_z, parameters=parameters, observations=observation_container
                ),
            ],
        ]


def print_summary(alignment: Alignment) -> None:
    logger.info(dict2table(alignment.group_stds, title="Group Standard Deviations"))
    logger.info(alignment.est_params)


def settings_str(alignment: Alignment) -> str:
    return (
        f"\n _____________________________________________________________________\n"
        f"| ---------------------------- Alignment ---------------------------- |\n"
        f"| Estimation of:           {alignment.settings.estimation_of.short_mode_str:<42} |\n"
        f"| Error probability [%]:   {alignment.settings.stochastics.error_probability*100:<42} |\n"
        f"|_____________________________________________________________________|\n"
    )
