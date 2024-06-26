import string
import uuid
from os.path import join, dirname
from tempfile import TemporaryDirectory
from typing import List, Optional

import numpy as np
import pandas as pd
import pytest
from PIL import Image
from niceml.experiments.expfilenames import ExperimentFilenames
from niceml.utilities.fsspec.locationutils import (
    LocationConfig,
    join_location_w_path,
    open_location,
    join_fs_path,
)
from niceml.utilities.ioutils import write_yaml, write_json, write_image, write_parquet
from niceml.utilities.timeutils import generate_timestamp

from nicemldashboard.experiment.experiment import Experiment
from nicemldashboard.experiment.type import ExperimentType
from nicemldashboard.loader.dataframeloader import CacheDataFrameLoader, DataFrameLoader
from nicemldashboard.loader.experimentloader import (
    ExperimentLoader,
    FilesAndFolderLoader,
)
from nicemldashboard.loader.imageloader import CacheImageLoader, ImageLoader

ALPHA_NUMERICS = list(string.ascii_lowercase + string.ascii_uppercase + string.digits)


def get_random_experiments(
    experiment_count: int, seed: Optional[int] = None
) -> List[Experiment]:
    """
    Generate a list of random experiments.

    Args:
        experiment_count: The number of experiments to generate.
        seed: Seed value for random number generation. Defaults to None.

    Returns:
        A list of randomly generated experiments.
    """
    random_generator = np.random.default_rng(seed=seed)
    experiments = []
    for index in range(experiment_count):
        short_id = "".join(
            random_generator.choice(
                a=ALPHA_NUMERICS,
                size=4,
            )
        )
        experiment_types = [experiment_type for experiment_type in ExperimentType]
        experiment_type: ExperimentType = experiment_types[
            random_generator.integers(0, len(experiment_types) - 1, size=1)[0]
        ]
        experiment = Experiment(
            experiment_type=experiment_type,
            name=f"Experiment_{index}",
            description=f"Random generated experiment ('{index}')",
            experiment_id=f"{uuid.uuid4()}-{short_id}",
            short_id=short_id,
            git_version={
                "version": "".join(
                    random_generator.choice(
                        a=ALPHA_NUMERICS,
                        size=20,
                    )
                )
            },
            data_set=f"data_set_{index}",
        )
        experiments.append(experiment)
    return experiments


@pytest.fixture
def tmp_dir() -> str:
    with TemporaryDirectory() as tmp:
        yield tmp


@pytest.fixture
def experiment_location(tmp_dir: str) -> LocationConfig:
    return LocationConfig(uri=join(tmp_dir, "experiments"))


@pytest.fixture
def cache_location(tmp_dir: str) -> LocationConfig:
    return LocationConfig(uri=join(tmp_dir, "cache"))


@pytest.fixture
def image_loader(cache_location: LocationConfig) -> ImageLoader:
    return CacheImageLoader(
        cache_location=join_location_w_path(cache_location, "images")
    )


@pytest.fixture
def data_frame_loader(cache_location: LocationConfig) -> CacheDataFrameLoader:
    return CacheDataFrameLoader(
        cache_location=join_location_w_path(cache_location, "data_frames")
    )


@pytest.fixture
def experiment_loader(
    data_frame_loader: DataFrameLoader,
    image_loader: ImageLoader,
    experiment_location: LocationConfig,
) -> FilesAndFolderLoader:
    return FilesAndFolderLoader(
        data_frame_loader=data_frame_loader,
        image_loader=image_loader,
        experiment_location=experiment_location,
    )


@pytest.fixture
def cached_image_filename(cache_location: LocationConfig) -> str:
    test_cached_image_array = np.ones(shape=(256, 256, 3), dtype=np.uint8)
    cached_image = Image.fromarray(test_cached_image_array)
    filename = "test_cached_image.png"
    with open_location(cache_location) as (cache_file_system, cache_root):
        filepath = join_fs_path(cache_file_system, cache_root, "images", filename)
        write_image(
            image=cached_image, filepath=filepath, file_system=cache_file_system
        )
    return filename


@pytest.fixture
def cached_data_frame_filename(cache_location: LocationConfig) -> str:
    data_frame = pd.DataFrame(
        [
            {"test_column_a": 1, "test_colum_b": "test_cache"},
            {"test_column_a": 2, "test_colum_b": "test_cache"},
        ]
    )
    filename = "test_cached_data_frame.parq"
    with open_location(cache_location) as (cache_file_system, cache_root):
        filepath = join_fs_path(cache_file_system, cache_root, "data_frames", filename)
        write_parquet(
            dataframe=data_frame, filepath=filepath, file_system=cache_file_system
        )
    return filename


@pytest.fixture
def image_filename(experiment_location: LocationConfig) -> str:
    test_image_array = np.zeros(shape=(256, 256, 3), dtype=np.uint8)
    image = Image.fromarray(test_image_array)
    filename = "test_image.png"
    with open_location(experiment_location) as (
        experiment_file_system,
        experiment_root,
    ):
        filepath = join_fs_path(
            experiment_file_system, experiment_root, "images", filename
        )
        write_image(image=image, filepath=filepath, file_system=experiment_file_system)
    return filename


@pytest.fixture
def data_frame_filename(cache_location: LocationConfig) -> str:
    data_frame = pd.DataFrame(
        [
            {"test_column_a": 1, "test_colum_b": "test"},
            {"test_column_a": 2, "test_colum_b": "test"},
        ]
    )
    filename = "test_data_frame.parq"
    with open_location(cache_location) as (cache_file_system, cache_root):
        filepath = join_fs_path(cache_file_system, cache_root, "data_frames", filename)
        write_parquet(
            dataframe=data_frame, filepath=filepath, file_system=cache_file_system
        )
    return filename


@pytest.fixture
def experiments(experiment_loader: ExperimentLoader) -> List[Experiment]:
    experiments = get_random_experiments(experiment_count=10, seed=167)
    with open_location(experiment_loader.experiment_location) as (
        experiment_filesystem,
        root_file_location,
    ):
        for current_experiment in experiments:
            experiment_folder = (
                f"{current_experiment.experiment_type.value.prefix}"
                f"-{generate_timestamp()}-id_{current_experiment.short_id}"
            )
            experiment_filepath = join_fs_path(
                experiment_filesystem,
                root_file_location,
                experiment_folder,
                ExperimentFilenames.EXP_INFO,
            )
            git_versions_filepath = join_fs_path(
                experiment_filesystem,
                root_file_location,
                experiment_folder,
                ExperimentFilenames.GIT_VERSIONS,
            )
            experiment_filesystem.mkdir(dirname(experiment_filepath))
            dict_experiment = current_experiment.to_dict()
            write_yaml(
                data=dict_experiment,
                filepath=experiment_filepath,
                file_system=experiment_filesystem,
            )
            write_json(
                data=current_experiment.git_version,
                filepath=git_versions_filepath,
                file_system=experiment_filesystem,
            )
    return experiments
