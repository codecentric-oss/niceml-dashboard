"""
This module provides a class for the buttons on the sidebar.
"""
from nicegui import ui
from nicemldashboard.experiment.type import ExperimentType

from nicemldashboard.state.appstate import (
    get_event_manager,
    ExperimentStateKeys,
    ExperimentEvents,
)


class SidebarButton(ui.button):
    """
    This class describes a sidebarbutton and has methods to handle on click events.
    """

    def __init__(
        self,
        *args,
        experiment_type: ExperimentType,
        **kwargs,
    ) -> None:
        """
        Inits SidebarButton class with the provided experiment type
        Args:
            *args:
            experiment_type:
            **kwargs:
        """
        super().__init__(*args, **kwargs)
        self.experiment_type = experiment_type
        self.on("click", self._change_experiment_type)

    def _change_experiment_type(self):
        experiment_state_data = get_event_manager().get_dict(
            ExperimentStateKeys.EXPERIMENT_DICT
        )
        experiment_state_data[
            ExperimentEvents.ON_EXPERIMENT_PREFIX_CHANGE
        ] = self.experiment_type
