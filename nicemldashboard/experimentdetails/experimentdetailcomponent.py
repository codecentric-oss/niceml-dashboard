"""Module for handling the experiment detail component."""
from abc import ABC, abstractmethod

from nicemldashboard.state import appstate


class BaseExperimentDetailComponent(ABC):
    """
    Abstract base class for a tab in the dashboard.
    """

    def __init__(self, name):
        """Initializes the BaseExperimentDetailComponent with a given name.

        Args:
            name (str): The name of the component.
        """
        self.name = name
        self._state_manager = appstate.get_state_manager()

    def render(self, dashboard_state):
        """
        Render the tab based on the current state of the dashboard.

        Args:
            dashboard_state: The current state of the dashboard.
        """
        if self.should_render(dashboard_state):
            self._render(dashboard_state)

    @abstractmethod
    def _render(self, dashboard_state) -> None:
        """
        Render the tab based on the current state of the dashboard. This method should be
        implemented by subclasses.
        Args:
            self:
            dashboard_state:

        Returns:

        """
        pass

    @abstractmethod
    def should_render(self, dashboard_state):
        """
        Decide whether this tab should be rendered based on the current state of the dashboard.

        Args:
            dashboard_state: The current state of the dashboard.

        Returns:
            bool: True if the tab should be rendered, False otherwise.
        """
        pass
