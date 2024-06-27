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
from nicemldashboard.pages.navigable import Navigable
from nicemldashboard.state.appstate import ExperimentEvents


def navigateToExperimentDetail(e, navigable: Navigable):
    """Navigates to the detail view based on the event data.

    Args:
        e: The event containing the data.
        navigable: The navigable object to be updated and rendered.
    """
    row_data = e.args[1]  # Get the row data from the event arguments
    short_id = row_data["short_id"]
    prefix = row_data["experiment_type"]["prefix"]
    experiment_url = f"/detail-view/{prefix}/{short_id}"
    navigable.update_url(experiment_url)
    navigable.render()
    ui.navigate.to(experiment_url)


@ui.refreshable
def experiment_runs_table(
    experiment_manager: ExperimentManager, exp_dic: ObservableDict, navigable: Navigable
):
    """
    Create a table for displaying experiment runs.

    Args:
        experiments: List of experiment runs to display in the table.
    """

    experiments = experiment_manager.filter_by(
        experiment_type=exp_dic.get(ExperimentEvents.ON_EXPERIMENT_PREFIX_CHANGE)
    )

    table = (
        ui.table(
            columns=Experiment.get_columns(),
            rows=[run.get_row() for run in experiments],
            row_key="short_id",
            selection="multiple",
            title="Experiment runs",
        )
        .style("width:100%")
        .props("flat")
    )

    table.add_slot(
        "body-cell-title",
        r'<td><a :href="props.row.url">{{ props.row.title }}</a></td>',
    )
    table.on("rowClick", lambda e: navigateToExperimentDetail(e, navigable))
