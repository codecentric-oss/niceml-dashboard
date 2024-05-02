"""
Module to define a sidebar for the niceml dashboard.

This module provides a function `sidebar` to create a sidebar with toggle button
and buttons for different experiment types.


Attributes:
    * `sidebar`: A function to create a sidebar for the niceml dashboard.

"""

from typing import Optional, List

from nicegui import ui
from nicegui.observables import ObservableDict

from nicemldashboard.State.State import _get_event_manager, ExperimentStateKeys, ExperimentEvents
from nicemldashboard.basecomponents.buttons import SidebarToggleButton
from nicemldashboard.experiment.type import ExperimentType


def sidebar(experiment_types: Optional[List[ExperimentType]] = None):
    """
    Create a sidebar for the dashboard.

    Args:
        experiment_types:   List of experiment types to display buttons for.
                            Defaults to None, in which case buttons for all available
                            experiment types will be displayed.
    """
    experiment_types = experiment_types or [
        exp_type.value for exp_type in ExperimentType.__members__.values()
    ]

    with ui.left_drawer(top_corner=False, bottom_corner=True, fixed=True).classes(
        "sidebar"
    ).props("width=70") as left_drawer:
        side_bar_toggle = SidebarToggleButton(left_drawer=left_drawer)

        for experiment_type in experiment_types:
            button_callback = lambda e, et=experiment_type: (
                on_stage_change(
                    _get_event_manager().get_dict(ExperimentStateKeys.EXPERIMENT_DICT),
                    get_enum(experiment_type),
                )
            )

            with ui.button(
                color="transparent", icon=experiment_type.icon, on_click=button_callback
            ).props("flat").classes("exp-type-btn").bind_text_from(
                experiment_type,
                "prefix",
                backward=lambda x: ("" if not side_bar_toggle.is_expanded() else x),
            ):
                ui.tooltip(experiment_type.name)


def on_stage_change(observable_dict: ObservableDict, value: str):
    """
    Updates the Events.on_experiment_change key with the value given.
    :param observable_dict:
    :param value:
    :return:
    """
    observable_dict[ExperimentEvents.ON_EXPERIMENT_PREFIX_CHANGE] = value

def get_enum(experiment_type: ExperimentType):
    """
    Provides a way to easily compare the experiment type with the ExperimentType Enums
    :param experiment_type:
    :return:
    """
    if experiment_type.prefix == "SEG":
        return ExperimentType.SEM_SEG
    elif experiment_type.prefix == "CLS":
        return ExperimentType.CLS
    elif experiment_type.prefix == "OBD":
        return ExperimentType.OBJ_DET
    else:
        raise Exception("The event type is not available in the ExperimentType Enum")
