"""
Module to define an Experiment class for a NiceML Dashboard.

This module provides a class `Experiment` to represent an experiment with various
attributes such as experiment type, name, description, experiment ID, short ID, and git version.
It also includes methods to retrieve the attributes as a row and to get the columns
for a table representation.


Attributes:
    * `Experiment`: A class to represent an experiment for a NiceML Dashboard.
"""

import inspect
from typing import Dict

from nicemldashboard.experiment.type import ExperimentType


class Experiment:
    """
    Represents an experiment for a NiceML Dashboard.

    Args:
        experiment_type: The type of the experiment.
        name: The name of the experiment.
        description: The description of the experiment.
        experiment_id: The ID of the experiment.
        short_id: The short ID of the experiment.
        git_version: The version of the experiment's git repository.

    """

    def __init__(
        self,
        experiment_type: ExperimentType,
        name: str,
        description: str,
        experiment_id: str,
        short_id: str,
        git_version: Dict[str, str],
    ):
        """
        Initializes an `Experiment`

        Args:
            experiment_type: The type of the experiment.
            name: The name of the experiment.
            description: The description of the experiment.
            experiment_id: The ID of the experiment.
            short_id: The short ID of the experiment.
            git_version: The version of the experiment's git repository.

        """
        self.git_version = git_version
        self.short_id = short_id
        self.experiment_id = experiment_id
        self.description = description
        self.name = name
        self.experiment_type = experiment_type

    def get_row(self):
        """
        Get the attributes of the experiment as a dictionary.

        Returns:
            A dictionary containing the attributes of the experiment.
        """
        row = {}
        for attribute in vars(self):
            row[attribute] = getattr(self, attribute)
        return row

    @classmethod
    def get_columns(cls):
        """
        Get the columns for representing the experiment in a table.

        Returns:
            A list of dictionaries representing the columns of the table.
        """
        rows = []
        for attribute in inspect.get_annotations(cls.__init__).keys():
            if attribute in ["experiment_type"]:
                continue
            rows.append(
                {
                    "name": attribute,
                    "label": format_string(attribute),
                    "field": attribute,
                    "align": "left",
                    "sortable": True,
                }
            )

        return rows


def format_string(input_string: str):
    """
    Format the input string by replacing underscores with whitespaces and capitalizing
    the first letter.

    Args:
        input_string: The input string to be formatted.

    Returns:
        str: The formatted string.
    """
    # Replace underscores with whitespaces
    formatted_string = input_string.replace("_", " ")

    # Capitalize the first letter
    formatted_string = formatted_string.capitalize()

    return formatted_string