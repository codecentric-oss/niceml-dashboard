"""
This module provides an abstract base class and a concrete implementation for loading experiments,
images, and data frames from specified locations.

Classes:
    ExperimentLoader: An abstract base class for loading experiments.
    FilesAndFolderLoader: A concrete implementation of ExperimentLoader that loads experiments
                            from files and folders.

Usage:
    This module is designed to be extended by providing specific loading mechanisms for experiments.
    - ExperimentLoader defines the interface for loading experiments.
    - FilesAndFolderLoader implements the interface for loading experiments from a file system.
"""

from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional, Union

from nicemldashboard.experiment.experiment import Experiment
from nicemldashboard.experiment.type import ExperimentType
from nicemldashboard.loader.dataframeloader import DataFrameLoader
from nicemldashboard.loader.imageloader import ImageLoader
from niceml.utilities.ioutils import list_dir, read_yaml
from niceml.utilities.fsspec.locationutils import (
    LocationConfig,
    open_location,
    join_fs_path,
)
from niceml.experiments.expfilenames import ExperimentFilenames
from niceml.config.envconfig import (
    EXP_NAME_KEY,
    SHORT_ID_KEY,
    DESCRIPTION_KEY,
    RUN_ID_KEY,
    EXP_TYPE_KEY,
)
from PIL import Image
import pandas as pd


class ExperimentLoader(ABC):
    """
    Abstract base class for loading experiments, images, and data frames.

    Attributes:
        image_loader: Loader for images.
        data_frame_loader: Loader for data frames.
        experiment_location: Location for experiments.
        logger: Logger for logging messages.
    """

    def __init__(
        self,
        image_loader: ImageLoader,
        data_frame_loader: DataFrameLoader,
        experiment_location: Union[dict, LocationConfig],
    ) -> None:
        """
        Initializes the ExperimentLoader with the provided loaders and experiment location.

        Args:
            image_loader: An instance of ImageLoader to load images.
            data_frame_loader: An instance of DataFrameLoader to load data frames.
            experiment_location: The location for experiments.
        """
        self.image_loader = image_loader
        self.data_frame_loader = data_frame_loader
        self.experiment_location = experiment_location
        self.logger = getLogger(__name__)

    @abstractmethod
    def load_experiments(self, data_set: Optional[str] = None) -> List[Experiment]:
        """
        Abstract method for loading experiments.

        Args:
            data_set: Optional dataset name to filter experiments by.

        Returns:
            A list of loaded experiments.
        """

        raise NotImplementedError()

    def load_image(self, *args, **kwargs) -> Image.Image:
        """
        Loads an image using the provided arguments and `self.image_loader`.

        Args:
            *args: Positional arguments for loading an image.
            **kwargs: Keyword arguments for loading an image.

        Returns:
            The loaded image.
        """

        return self.image_loader.load_image(*args, **kwargs)

    def load_data_frame(self, *args, **kwargs) -> pd.DataFrame:
        """
        Loads a data frame using the provided arguments and `self.data_frame_loader`.

        Args:
            *args: Positional arguments for loading a data frame.
            **kwargs: Keyword arguments for loading a data frame.

        Returns:
            The loaded data frame.
        """

        return self.data_frame_loader.load_data_frame(*args, **kwargs)


class FilesAndFolderLoader(ExperimentLoader):
    """
    Concrete implementation of ExperimentLoader that loads experiments from files and folders.

    Methods:
        load_experiments: Loads experiments from the specified location.
    """

    def load_experiments(self, data_set: Optional[str] = None) -> List[Experiment]:
        """
        Loads experiments from the specified file system location.

        Args:
            data_set: Optional dataset name to filter experiments by.

        Returns:
            A list of loaded experiments.
        """

        with open_location(self.experiment_location) as (file_system, root_location):
            experiments_paths = join_fs_path(file_system, root_location, data_set or "")
            try:
                experiment_folders = list_dir(
                    path=experiments_paths, file_system=file_system
                )
            except FileNotFoundError as error:
                self.logger.exception("File not found (%s)", error.filename)
                return []

            experiments: List[Experiment] = []
            for experiment_folder in experiment_folders:
                if file_system.isdir(
                    join_fs_path(
                        file_system,
                        root_location,
                        data_set or "",
                        experiment_folder,
                    )
                ):
                    experiment_info_path = join_fs_path(
                        file_system,
                        root_location,
                        data_set or "",
                        experiment_folder,
                        ExperimentFilenames.EXP_INFO,
                    )
                    experiment_info = read_yaml(
                        filepath=experiment_info_path, file_system=file_system
                    )
                    experiments_git_versions_path = join_fs_path(
                        file_system,
                        root_location,
                        data_set or "",
                        experiment_folder,
                        ExperimentFilenames.GIT_VERSIONS,
                    )
                    experiments_git_versions = read_yaml(
                        filepath=experiments_git_versions_path, file_system=file_system
                    )
                    experiment = Experiment(
                        name=experiment_info[EXP_NAME_KEY],
                        experiment_type=ExperimentType.from_prefix(
                            prefix=experiment_info[EXP_TYPE_KEY]
                        ),
                        short_id=experiment_info[SHORT_ID_KEY],
                        description=experiment_info[DESCRIPTION_KEY],
                        experiment_id=experiment_info[RUN_ID_KEY],
                        git_version=experiments_git_versions,
                        data_set="test_data_set",  # TODO : Dataset to experimentset yaml
                    )
                    experiments.append(experiment)
        return experiments
