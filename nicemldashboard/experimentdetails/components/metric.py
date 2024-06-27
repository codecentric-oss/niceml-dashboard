"""Module for handling the metric component of experiment details."""

from nicemldashboard.experimentdetails.experimentdetailcomponent import (
    BaseExperimentDetailComponent,
)


class MetricComponent(BaseExperimentDetailComponent):
    """
    A tab that provides graphs of various metrics.
    """

    def should_render(self, dashboard_state):
        """Checks if the rendering of the MetricComponent is necessary.

        Returns:
            None
        """
        pass

    def _render(self, dashboard_state):
        """Renders the UI elements for the MetricComponent.

        Returns:
            None
        """
        pass
