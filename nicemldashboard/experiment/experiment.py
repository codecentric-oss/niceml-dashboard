"""
Module to define an Experiment class for a NiceML Dashboard.

This module provides a class `Experiment` to represent an experiment with various
attributes such as experiment type, name, description, experiment ID, short ID,
data set, and git version. It also includes methods to retrieve the attributes as a row
and to get the columns for a table representation.

Attributes:
    * `Experiment`: A class to represent an experiment for a NiceML Dashboard.
"""

from typing import Dict, get_type_hints
from niceml.config.envconfig import (
    EXP_NAME_KEY,
    SHORT_ID_KEY,
    DESCRIPTION_KEY,
    RUN_ID_KEY,
    EXP_TYPE_KEY,
)
from nicemldashboard.experiment.type import ExperimentType


class Experiment:
    """
    Represents an experiment for a NiceML Dashboard.

    Attributes:
        experiment_type: The type of the experiment.
        name: The name of the experiment.
        description: The description of the experiment.
        experiment_id: The ID of the experiment.
        short_id: The short ID of the experiment.
        git_version : The version of the experiment's git repository.
        data_set: The data set associated with the experiment.
    """

    def __init__(
        self,
        experiment_type: ExperimentType,
        name: str,
        description: str,
        experiment_id: str,
        short_id: str,
        git_version: Dict[str, str],
        data_set: str,
    ):
        """
        Initializes an `Experiment`

        Args:
            experiment_type : The type of the experiment.
            name: The name of the experiment.
            description: The description of the experiment.
            experiment_id: The ID of the experiment.
            short_id: The short ID of the experiment.
            git_version : The version of the experiment's git repository.
            data_set: The data set associated with the experiment.
        """
        self.git_version = git_version
        self.short_id = short_id
        self.experiment_id = experiment_id
        self.description = description
        self.name = name
        self.experiment_type = experiment_type
        self.data_set = data_set

    def get_row(self) -> Dict[str, str]:
        """
        Get the attributes of the experiment as a dictionary.

        Returns:
            A dictionary containing the attributes of the experiment.
        """
        row = {}
        for attribute in vars(self):
            value = getattr(self, attribute)
            if isinstance(value, dict):
                value = ", ".join(
                    [f"{name}:{version}" for name, version in value.items()]
                )
            row[attribute] = value
        return row

    @classmethod
    def get_columns(cls) -> list:
        """
        Get the columns for representing the experiment in a table.

        Returns:
            A list of dictionaries representing the columns of the table.
        """
        columns = []
        for attribute in get_type_hints(cls.__init__).keys():
            if attribute in ["experiment_type"]:
                continue
            columns.append(
                {
                    "name": attribute,
                    "label": format_string(attribute),
                    "field": attribute,
                    "align": "left",
                    "sortable": True,
                }
            )

        return columns

    def to_dict(self) -> dict:
        """
        Convert the experiment to a dictionary representation.

        Returns:
            A dictionary containing the key attributes of the experiment.
        """
        return {
            EXP_NAME_KEY: self.name,
            SHORT_ID_KEY: self.short_id,
            DESCRIPTION_KEY: self.description,
            RUN_ID_KEY: self.experiment_id,
            EXP_TYPE_KEY: self.experiment_type.value.prefix,
            "data_set": self.data_set,
        }

    def __lt__(self, other: "Experiment") -> bool:
        """
        Less-than comparison based on experiment ID.

        Args:
            other: The other experiment to compare against.

        Returns:
            True if this experiment's ID is less than the other's, False otherwise.
        """
        return self.experiment_id < other.experiment_id

    def __eq__(self, other: "Experiment") -> bool:
        """
        Equality comparison based on experiment ID.

        Args:
            other: The other experiment to compare against.

        Returns:
            True if this experiment's ID is equal to the other's, False otherwise.
        """
        return self.experiment_id == other.experiment_id


def format_string(attribute_name: str) -> str:
    """
    Format the attribute name by replacing underscores with whitespaces and capitalizing
    the first letter.

    Args:
        attribute_name: The attribute name to be formatted.

    Returns:
        The formatted string.
    """

    formatted_string = attribute_name.replace("_", " ")

    formatted_string = formatted_string.capitalize()

    return formatted_string
