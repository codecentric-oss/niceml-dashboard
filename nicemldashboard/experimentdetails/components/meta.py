"""Module for handling the meta component of experiment details."""


from nicemldashboard.experimentdetails.experimentdetailcomponent import (
    BaseExperimentDetailComponent,
)


class MetaComponent(BaseExperimentDetailComponent):
    """
    A tab that provides an overview of an experiment.
    """

    def _render(self):
        """Renders the UI elements for the MetaComponent.

        Returns:
            None
        """
        pass

    def should_render(self, dashboard_state):
        """Checks if the rendering of the MetaComponent is necessary.

        Returns:
            None
        """
        return True
