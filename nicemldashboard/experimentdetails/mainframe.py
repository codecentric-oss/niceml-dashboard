"""Module for rendering the experiment details view page based on the url."""

from nicegui import ui

from nicemldashboard.pages.navigable import Navigable


class ExperimentDetailsFrame(Navigable):
    """
    Represents a frame to display experiment details
    """

    def __init__(self):
        """
        Initializes a TabsView with the provided experiment.

        Args:

            experiment: An instance of the Experiment class.
        """

        self.experiment_url = ""
        self.components_config = []  # Placeholder

    def _render_tabs_view(self):
        with ui.tabs().classes("w-full") as tabs:
            one = ui.tab("One")
            two = ui.tab("Two")
        with ui.tab_panels(tabs, value=two).classes("w-full"):
            with ui.tab_panel(one):
                ui.label("First tab")
            with ui.tab_panel(two):
                ui.label("Second tab")

    def render(self):
        """Renders the main frame page based on the url .
        Args:
            None

        Returns:
            None

        """
        ui.page(f"{self.experiment_url}")(self._render_tabs_view)()

    def update_url(self, url):
        """Updates the URL of the page that the app plans to navigate to.

        Args:
            url: The new URL.

        Returns:
            None
        """
        self.experiment_url = url
