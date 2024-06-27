"""
Module to define the main dashboard application for a NiceML Dashboard.

This module provides a class `Dashboard` to initialize the dashboard with settings
and run the main application.

Attributes:
    * `Dashboard`: A class to initialize the dashboard and run the main application.
"""

from typing import Optional

from nicegui import ui, app

from nicemldashboard.basecomponents.sidebar import sidebar
from nicemldashboard.basecomponents.table import experiment_runs_table
from nicemldashboard.experiment.experimentmanager import ExperimentManager
from nicemldashboard.loader.dataframeloader import CacheDataFrameLoader
from nicemldashboard.loader.experimentloader import (
    ExperimentLoader,
    FilesAndFolderLoader,
)
from nicemldashboard.loader.imageloader import CacheImageLoader
from nicemldashboard.state.appstate import (
    AppState,
    init_event_manager,
    ExperimentStateKeys,
)
from nicemldashboard.utils.settings import Settings


# Add static files (e.g., fonts) to the application's static file routing
app.add_static_files("/fonts", "nicemldashboard/assets/fonts")


class Dashboard:
    """
    Main dashboard application for a NiceML Dashboard.

    Arguments:
        self.experiment_loader: Optional loader to load experiments.
        self.settings: Settings that are used for a dashboard instance
        self.experiment_manager: Instance of `ExperimentManager` to manage the experiments of a
                                dashboard.
    """

    def __init__(
        self,
        experiment_loader: Optional[ExperimentLoader] = None,
        settings_path: str = ".niceml/settings.yml",
    ):
        """
        Initialize the Dashboard.

        Args:
            experiment_loader: Optional loader to load experiments.
            settings_path: Path to the YAML settings file.
        """
        cache_location = {"uri": "./cache"}
        experiment_location = {"uri": "./experiments"}
        image_loader = CacheImageLoader(cache_location=cache_location)
        data_frame_loader = CacheDataFrameLoader(cache_location=cache_location)
        self.experiment_loader = experiment_loader or FilesAndFolderLoader(
            experiment_location=experiment_location,
            image_loader=image_loader,
            data_frame_loader=data_frame_loader,
        )
        self.experiment_manager = ExperimentManager(
            experiment_loader=self.experiment_loader
        )

        self.settings = Settings(settings_path=settings_path)

    def __call__(self, *args, **kwargs):
        """
        Run the main application.
        """

        @ui.page("/")
        def home():
            """
            Define the layout of the start page.
            """
            ui.add_scss("nicemldashboard/assets/style.scss")
            _instance = AppState()
            init_event_manager(_instance)
            exp_data = _instance.get_dict(ExperimentStateKeys.EXPERIMENT_DICT)
            exp_data.on_change(experiment_runs_table.refresh)

            sidebar()
            with ui.grid().classes("content"):
                with ui.card().style("width:100%"):
                    with ui.column(wrap=False).style("width:100%"):
                        with ui.row():
                            ui.input(
                                label="Experiment run", placeholder="Search for run"
                            )
                        ui.separator()
                        experiment_runs_table(self.experiment_manager, exp_data)

        ui.run(*args, **kwargs)


if __name__ in {"__main__", "__mp_main__"}:
    dashboard = Dashboard()
    dashboard()
