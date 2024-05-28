"""
Module to define a table for displaying experiment runs.

This module provides a function `experiment_runs_table` to create a table
for displaying experiment runs.

Attributes:
    * `experiment_runs_table`: A function to create a table for displaying experiment runs.

"""

from nicegui import ui
from nicegui.observables import ObservableDict
from nicemldashboard.experiment.experiment import Experiment
from nicemldashboard.experiment.experimentmanager import ExperimentManager
from nicemldashboard.state.appstate import ExperimentEvents


@ui.refreshable
def experiment_runs_table(
    experiment_manager: ExperimentManager, exp_dic: ObservableDict
):
    """
    Create a table for displaying experiment runs.

    Args:
        experiments: List of experiment runs to display in the table.
    """

    experiments = experiment_manager.filter_by(
        experiment_type=exp_dic.get(ExperimentEvents.ON_EXPERIMENT_PREFIX_CHANGE)
    )

    ui.table(
        columns=Experiment.get_columns(),
        rows=[run.get_row() for run in experiments],
        row_key="short_id",
        selection="multiple",
        title="Experiment runs",
    ).style("width:100%").props("flat")
