from typing import List

import numpy as np
from niceml.utilities.fsspec.locationutils import join_location_w_path

from nicemldashboard.experiment.experiment import Experiment
from nicemldashboard.loader.experimentloader import ExperimentLoader


def test_load_experiments(
    experiment_loader: ExperimentLoader,
    experiments: List[Experiment],
):
    found_experiments = experiment_loader.load_experiments()
    assert sorted(found_experiments) == sorted(experiments)


def test_load_image_with_experiment_loader(
    experiment_loader: ExperimentLoader,
    experiments: List[Experiment],
    image_filename: str,
):
    loaded_image = experiment_loader.load_image(
        file_name=image_filename,
        image_location=join_location_w_path(
            experiment_loader.experiment_location, "images"
        ),
    )
    assert (np.asarray(loaded_image) == 0).all()
    assert loaded_image.size == (256, 256)


def test_load_data_frame_with_experiment_loader(
    experiment_loader: ExperimentLoader,
    data_frame_filename: str,
    experiments: List[Experiment],
):
    loaded_data_frame = experiment_loader.load_data_frame(
        file_path=data_frame_filename,
        data_frame_location=join_location_w_path(
            experiment_loader.experiment_location, "data_frames"
        ),
    )
    assert len(loaded_data_frame) == 2
    assert all(loaded_data_frame["test_colum_b"] == "test")
