"""
This module provides an experiment manager. Currently, experiment manager
supports filtering experiments by their properties.
"""
import logging
from typing import List

from nicemldashboard.exceptions import ExperimentFilterError
from nicemldashboard.experiment.experiment import Experiment


class ExperimentManager:
    """
    Allows filtering experiments by making the filter_by method available
    """

    def __init__(self, experiments: List[Experiment]):
        """
        Initializes an ExperimentManager with the provided list of experiments.
        """
        self.experiments = experiments

    def filter_by(self, **filters) -> List[Experiment]:
        """
        Filters the experiment list after filtering with the provided filters

        Args:
            **filters: A dictionary of filters to filter by

        Returns:
            List of filtered experiments
        """
        filtered_experiments = []
        for experiment_attribute, field_value in filters.items():
            try:
                filtered_experiments = [
                    exp
                    for exp in self.experiments
                    if getattr(exp, experiment_attribute, None) == field_value
                ]
            except ExperimentFilterError as e:
                # Log the error message with details of which experiment and filter caused it.
                logging.warning(
                    f"Incomparable types between attribute '{experiment_attribute}' "
                    f"with field_value '{field_value}' "
                    f"and filter field_value '{field_value}': {e}"
                )
        return filtered_experiments
