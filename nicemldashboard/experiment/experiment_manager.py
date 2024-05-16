"""
This module provides an experiment manager. Currently, experiment manager
supports filtering experiments by their properties.
"""
import logging
from typing import List

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
        :param filters:
        :return:
        """
        filtered_experiments = self.experiments.copy()
        for key, value in filters.items():
            try:
                if isinstance(value, dict):
                    filtered_experiments = [
                        exp
                        for exp in filtered_experiments
                        if all(
                            item in getattr(exp, key, {}).items()
                            for item in value.items()
                        )
                    ]
                else:
                    filtered_experiments = [
                        exp
                        for exp in filtered_experiments
                        if getattr(exp, key, None) == value
                    ]
            except TypeError as e:
                # Log the error message with details of which experiment and filter caused it.
                logging.error(
                    f"Incomparable types between attribute '{key}' with value '{value}' "
                    f"and filter value '{value}': {e}"
                )
        return filtered_experiments
