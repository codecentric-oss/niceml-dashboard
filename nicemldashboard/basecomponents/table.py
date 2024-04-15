"""
Module to define a table for displaying experiment runs.

This module provides a function `experiment_runs_table` to create a table
for displaying experiment runs.

Attributes:
    * `experiment_runs_table`: A function to create a table for displaying experiment runs.

"""

from typing import List
from nicegui import ui
from nicemldashboard.experiment.experiment import Experiment


def experiment_runs_table(experiments: List[Experiment]):
    """
    Create a table for displaying experiment runs.

    Args:
        experiments: List of experiment runs to display in the table.
    """
    ui.table(
        columns=Experiment.get_columns(),
        rows=[run.get_row() for run in experiments],
        row_key="short_id",
        selection="multiple",
        title="Experiment runs",
    ).style("width:100%").props("flat")
