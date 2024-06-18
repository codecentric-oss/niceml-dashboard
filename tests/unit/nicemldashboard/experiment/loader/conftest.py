
import datetime
from os.path import join,dirname
import string
from tempfile import TemporaryDirectory
import uuid
import numpy as np
from typing import List, Optional
import pytest
from niceml.experiments.expfilenames import ExperimentFilenames
from nicemldashboard.experiment.experiment import Experiment
from nicemldashboard.experiment.type import ExperimentType
from nicemldashboard.loader.dataframeloader import CacheDataFrameLoader, DataFrameLoader
from nicemldashboard.loader.experimentloader import ExperimentLoader, FilesAndFolderLoader
from nicemldashboard.loader.imageloader import CacheImageLoader, ImageLoader
from niceml.utilities.fsspec.locationutils import LocationConfig, join_location_w_path, open_location, join_fs_path
from niceml.dagster.ops.experiment import create_exp_settings
from niceml.utilities.ioutils import write_yaml,write_json
from niceml.utilities.timeutils import generate_timestamp

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
            git_version="".join(
                random_generator.choice(
                    a=ALPHA_NUMERICS,
                    size=20,
                )
            ),
            data_set = f"data_set_{index}"
        )
        experiments.append(experiment)
    return experiments


@pytest.fixture
def tmp_dir() -> str:
    with TemporaryDirectory() as tmp:
        yield tmp
        
@pytest.fixture
def experiment_location(tmp_dir: str) -> LocationConfig:
    return LocationConfig(uri=join(tmp_dir,"experiments"))

@pytest.fixture
def cache_location(tmp_dir: str) -> LocationConfig:
    return LocationConfig(uri=join(tmp_dir,"cache"))

@pytest.fixture
def image_loader(cache_location: LocationConfig) -> ImageLoader:
    return CacheImageLoader(cache_location=join_location_w_path(cache_location,"image"))


@pytest.fixture
def data_frame_loader(cache_location: LocationConfig) -> CacheDataFrameLoader:
    return CacheDataFrameLoader(cache_location=join_location_w_path(cache_location,"data_frame"))

@pytest.fixture
def experiment_loader(data_frame_loader: DataFrameLoader,image_loader: ImageLoader, experiment_location: LocationConfig) -> FilesAndFolderLoader:
    return FilesAndFolderLoader(data_frame_loader=data_frame_loader,image_loader=image_loader,experiment_location=experiment_location)


@pytest.fixture
def experiments(experiment_loader:ExperimentLoader) -> List[Experiment]:
    experiments = get_random_experiments(experiment_count=10, seed=167)
    with open_location(experiment_loader.experiment_location) as (experimentfilesystem,rootfilelocation):
        for current_experiment in experiments :
            experiment_folder = f"{current_experiment.experiment_type.value.prefix}-{generate_timestamp()}-id_{current_experiment.short_id}"
            experiment_filepath = join_fs_path(experimentfilesystem,rootfilelocation,experiment_folder,ExperimentFilenames.EXP_INFO)
            git_versions_filepath = join_fs_path(experimentfilesystem,rootfilelocation,experiment_folder,ExperimentFilenames.GIT_VERSIONS)
            experimentfilesystem.mkdir(dirname(experiment_filepath))
            dict_experiment = current_experiment.to_dict()
            write_yaml(data=dict_experiment,filepath=experiment_filepath,file_system=experimentfilesystem)
            write_json(data=current_experiment.git_version,filepath=git_versions_filepath,file_system=experimentfilesystem)
    return experiments