"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2023
mail@gtombrink.de
"""
from typing import Tuple

import numpy as np
from matplotlib import pyplot as plt
from trajectopy.plotting.image_request import TIMImageRequester
from trajectopy.settings.plot_settings import PlotSettings
from matplotlib.figure import Figure
from trajectopy.trajectory import Sorting, Trajectory


def plot_trajectories(
    trajectories: list[Trajectory],
    plot_settings: PlotSettings = PlotSettings(),
    dim: int = 2,
) -> Tuple[Figure, Figure, Figure | None]:
    """
    Plots Trajectories
    """
    fig_pos = plot_pos(trajectories=trajectories, plot_settings=plot_settings, dim=dim)
    fig_xyz = plot_xyz(trajectories=trajectories, plot_settings=plot_settings)
    fig_rpy = plot_rpy(trajectories=trajectories, plot_settings=plot_settings)
    return fig_pos, fig_xyz, fig_rpy


def plot_pos(trajectories: list[Trajectory], plot_settings: PlotSettings = PlotSettings(), dim: int = 2) -> Figure:
    if dim == 2:
        fig_pos, ax_pos = plt.subplots()
        ax_pos.axis("equal")
    elif dim == 3:
        fig_pos = plt.figure()
        ax_pos: plt.Axes = fig_pos.add_subplot(111, projection="3d")
        ax_pos.set_zlabel("z [m]")  # type: ignore
    else:
        raise ValueError(f"Unknown dimension: {dim}")
    ax_pos.set_xlabel("x [m]")
    ax_pos.set_ylabel("y [m]")

    legend_names = []
    image_requester = TIMImageRequester()
    for i, traj in enumerate(trajectories):
        legend_names.append(traj.name)

        if plot_settings.request_aerial_image and dim == 2 and traj.pos.local_transformer is not None:
            if i == 0:
                image, extent = image_requester.request(
                    pointset=traj.pos.mean(), width=plot_settings.image_width, height=plot_settings.image_height
                )
                plt.imshow(np.array(image), aspect="auto", extent=extent)
                ax_pos.axis("equal")
            traj = traj.copy()
            traj.pos.to_epsg(target_epsg=image_requester.request_epsg, inplace=True)

        # pos fig
        if dim == 2:
            ax_pos.plot(traj.pos.x, traj.pos.y)
        elif dim == 3:
            ax_pos.plot(traj.pos.x, traj.pos.y, traj.pos.z)

    if dim == 3:
        set_aspect_equal_3d(ax_pos)

    fig_pos.legend(legend_names, ncol=4, loc="upper center")
    return fig_pos


def plot_xyz(trajectories: list[Trajectory], plot_settings: PlotSettings = PlotSettings()) -> Figure:
    fig_xyz, axs_xyz = plt.subplots(3, 1, sharex=True)

    legend_names = []
    for traj in trajectories:
        legend_names.append(traj.name)
        xyz = traj.pos.xyz

        # xyz fig
        ylabels = ["x [m]", "y [m]", "z [m]"]
        for j, (ax, yl) in enumerate(zip(axs_xyz, ylabels)):
            ax.plot(traj.function_of, xyz[:, j])
            ax.set_ylabel(yl)
            if j == 2:
                if traj.sorting == Sorting.CHRONO:
                    ax.set_xlabel("time [s]")
                else:
                    ax.set_xlabel("trajectory length [m]")

    fig_xyz.legend(legend_names, ncol=4, loc="upper center")
    return fig_xyz


def plot_rpy(trajectories: list[Trajectory], plot_settings: PlotSettings = PlotSettings()) -> Figure | None:
    fig_rpy, axs_rpy = plt.subplots(3, 1, sharex=True)

    not_empty = False
    legend_names = []
    for traj in trajectories:
        # rpy fig
        if traj.rot and len(traj.rot) > 0:
            legend_names.append(traj.name)
            rpy = traj.rot.as_euler(seq="xyz")
            ylabels = ["roll [°]", "pitch [°]", "yaw [°]"]
            for j, (ax, yl) in enumerate(zip(axs_rpy, ylabels)):
                rpy_i = np.unwrap(rpy[:, j]) if j < 2 else rpy[:, j]
                ax.plot(traj.function_of, np.rad2deg(rpy_i))
                ax.set_ylabel(yl)
                if j == 2:
                    if traj.sorting == Sorting.CHRONO:
                        ax.set_xlabel("time [s]")
                    else:
                        ax.set_xlabel("trajectory length [m]")
            not_empty = True

    fig_rpy.legend(legend_names, ncol=4, loc="upper center")

    return fig_rpy if not_empty else None


def set_aspect_equal_3d(ax):
    """
    https://stackoverflow.com/a/35126679
    """
    xlim = ax.get_xlim3d()
    ylim = ax.get_ylim3d()
    zlim = ax.get_zlim3d()

    from numpy import mean

    xmean = mean(xlim)
    ymean = mean(ylim)
    zmean = mean(zlim)

    plot_radius = max(
        abs(lim - mean_) for lims, mean_ in ((xlim, xmean), (ylim, ymean), (zlim, zmean)) for lim in lims
    )

    ax.set_xlim3d([xmean - plot_radius, xmean + plot_radius])
    ax.set_ylim3d([ymean - plot_radius, ymean + plot_radius])
    ax.set_zlim3d([zmean - plot_radius, zmean + plot_radius])
