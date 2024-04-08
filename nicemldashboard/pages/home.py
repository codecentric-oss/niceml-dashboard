"""
Module to define the home page.

This module provides a function `home` which defines the layout of the home page,
including a sidebar, filters for experiment runs, and a table to display
experiment runs.

Attributes:
    * `home`: A function defining the layout of the home page.

"""

from nicegui import ui

from nicemldashboard.basecomponents.sidebar import sidebar
from nicemldashboard.basecomponents.table import experiment_runs_table
from nicemldashboard.experiment.utils import get_random_experiments


@ui.page("/")
def home():
    """
    Define the layout of the home page.
    """
    ui.add_style("nicemldashboard/assets/style.scss")

    experiments = get_random_experiments(experiment_count=20)

    sidebar()
    with ui.grid().classes("content"):
        with ui.card().style("width:100%"):
            with ui.column(wrap=False).style("width:100%"):
                with ui.row():
                    ui.input(label="Experiment run", placeholder="Search for run")
                ui.separator()
                experiment_runs_table(experiments=experiments)
