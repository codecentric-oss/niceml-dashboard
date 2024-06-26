"""
Module to define a sidebar for the niceml dashboard.

This module provides a function `sidebar` to create a sidebar with toggle button
and buttons for different experiment types.


Attributes:
    * `sidebar`: A function to create a sidebar for the niceml dashboard.

"""

from typing import Optional, List

from nicegui import ui

from nicemldashboard.basecomponents.buttons.sidebarbutton import SidebarButton
from nicemldashboard.basecomponents.buttons.sidebartogglebutton import (
    SidebarToggleButton,
)
from nicemldashboard.experiment.type import ExperimentType


def sidebar(experiment_types: Optional[List[ExperimentType]] = None):
    """
    Create a sidebar for the dashboard.

    Args:
        experiment_types:   List of experiment types to display buttons for.
                            Defaults to None, in which case buttons for all available
                            experiment types will be displayed.
    """
    with ui.left_drawer(top_corner=False, bottom_corner=True, fixed=True).classes(
        "sidebar"
    ).props("width=70") as left_drawer:
        side_bar_toggle = SidebarToggleButton(left_drawer=left_drawer)

        for experiment_type in ExperimentType.__members__.values():
            with SidebarButton(
                color="transparent",
                icon=experiment_type.value.icon,
                experiment_type=experiment_type,
            ).props("flat").classes("exp-type-btn").bind_text_from(
                experiment_type.value,
                "prefix",
                backward=lambda x: ("" if not side_bar_toggle.is_expanded() else x),
            ):
                ui.tooltip(experiment_type.value.name)
