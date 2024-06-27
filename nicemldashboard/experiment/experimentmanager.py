"""
This module provides an Experiment Manager that supports loading and filtering experiments
by their properties.
"""

import logging
from typing import List, Dict, Any

from PIL import Image

from nicemldashboard.utils.exceptions import ExperimentFilterError
from nicemldashboard.experiment.experiment import Experiment
from nicemldashboard.loader.experimentloader import ExperimentLoader


class ExperimentManager:
    """
    Manages experiments by providing functionality to load and filter them.

    Attributes:
        experiment_loader: The loader used to load experiments and related data.
        experiments: A list of loaded experiments.
    """

    def __init__(self, experiment_loader: ExperimentLoader):
        """
        Initializes an ExperimentManager with the provided ExperimentLoader.

        Args:
            experiment_loader: An instance of ExperimentLoader to load experiments.
        """
        self.experiment_loader = experiment_loader
        self.experiments = experiment_loader.load_experiments()

    def load_image(self, experiment: Experiment, image_path: str) -> Image:
        """
        Loads an image of a given experiment.

        Args:
            experiment: The experiment for which to load the image.
            image_path: The path to the image file.

        Returns:
            The loaded image.
        """
        return self.experiment_loader.load_image(
            image_location={"uri": experiment.experiment_id}, file_name=image_path
        )

    def load_data_frame(self, experiment: Experiment, data_frame_path: str) -> Image:
        """
        Loads a data frame of a given experiment.

        Args:
            experiment: The experiment for which to load the data frame.
            data_frame_path: The path to the data frame file.

        Returns:
            The loaded data frame.
        """
        return self.experiment_loader.load_data_frame(
            data_frame_location={"uri": experiment.experiment_id},
            file_name=data_frame_path,
        )

    def filter_by(self, **filters: Dict[str, Any]) -> List[Experiment]:
        """
        Filters the experiments based on the provided filters.

        Args:
            **filters: A dictionary where keys are experiment attribute names
                and values are the values to filter by.

        Returns:
            A list of experiments that match all the provided filters.

        Raises:
            ExperimentFilterError: If there is an error in filtering experiments due to
            incomparable types.
        """
        filtered_experiments = self.experiments
        for experiment_attribute, field_value in filters.items():
            try:
                filtered_experiments = [
                    exp
                    for exp in filtered_experiments
                    if getattr(exp, experiment_attribute, None) == field_value
                ]
            except ExperimentFilterError as e:
                logging.warning(
                    f"Incomparable types between attribute '{experiment_attribute}' "
                    f"with field_value '{field_value}': {e}"
                )
        return filtered_experiments
