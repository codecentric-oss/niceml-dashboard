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
    test_image_filename: str,
):
    loaded_image = experiment_loader.load_image(
        file_name=test_image_filename,
        image_location=join_location_w_path(
            experiment_loader.experiment_location, "images"
        ),
    )
    assert (np.asarray(loaded_image) == 0).all()
    assert loaded_image.size == (256, 256)
