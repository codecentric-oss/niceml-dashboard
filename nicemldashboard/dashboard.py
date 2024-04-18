"""
Module to define the main dashboard application for a NiceML Dashboard.

This module provides a class `Dashboard` to initialize the dashboard with settings
and run the main application.

Attributes:
    * `Dashboard`: A class to initialize the dashboard and run the main application.
"""

from nicegui import ui, app
from nicemldashboard.pages.home import home
from nicemldashboard.utils.settings import Settings

app.add_static_files("/fonts", "assets/fonts")


class Dashboard:
    """
    Main dashboard application for a NiceML Dashboard.
    """

    def __init__(self, settings_path: str = "../.niceml/settings.yml"):
        """
        Initialize the Dashboard.

        Args:
            settings_path: Path to the YAML settings file.
        """
        self.settings = Settings(settings_path=settings_path)

    def __call__(self, *args, **kwargs):
        """
        Run the main application.
        """
        home()
        ui.run(*args, **kwargs)


dashboard = Dashboard()

if __name__ in {"__main__", "__mp_main__"}:
    dashboard()
