"""
Module to define the home page.

This module provides a function `home` which defines the layout of the home page,
including a sidebar, filters for experiment runs, and a table to display
experiment runs.

Attributes:
    * `home`: A function defining the layout of the home page.

"""


from nicegui import ui
from nicegui.observables import ObservableDict


from nicemldashboard.State.State import (
    EventManager,
    ExperimentStateKeys,
    ExperimentEvents,
    init_event_manager,
)

from nicemldashboard.basecomponents.sidebar import sidebar
from nicemldashboard.basecomponents.table import experiment_runs_table
from nicemldashboard.experiment.utils import get_random_experiments
from nicemldashboard.experiment.experiment_manager import ExperimentManager


@ui.page("/")
def home():
    """
    Define the layout of the home page.
    """

    ui.add_scss("nicemldashboard/assets/style.scss")
    _instance = EventManager()

    init_event_manager(_instance)
    exp_dict = _instance.get_dict(ExperimentStateKeys.EXPERIMENT_DICT)
    exp_dict.on_change(_experiment_runs_table.refresh)

    experiments = get_random_experiments(experiment_count=20)
    experiment_manager = ExperimentManager(experiments)

    sidebar()
    with ui.grid().classes("content"):
        with ui.card().style("width:100%"):
            with ui.column(wrap=False).style("width:100%"):
                with ui.row():
                    ui.input(label="Experiment run", placeholder="Search for run")
                ui.separator()
                _experiment_runs_table(experiment_manager, exp_dict)


@ui.refreshable
def _experiment_runs_table(
    experiment_manager: ExperimentManager, exp_dic: ObservableDict
):
    experiments = experiment_manager.filter_by(
        experiment_type=exp_dic.get(ExperimentEvents.ON_EXPERIMENT_PREFIX_CHANGE)
    )
    experiment_runs_table(experiments=experiments)
