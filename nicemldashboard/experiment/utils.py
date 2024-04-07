"""
Module for utility functions for experiments.

This module provides a function `get_random_experiments` to generate a specified
number of random experiments with random experiment types, names, descriptions, etc.

Attributes:
    * `get_random_experiments`: A function to generate random experiments.

"""

import string
import uuid
from typing import List, Optional

import numpy as np

from nicemldashboard.experiment.experiment import Experiment
from nicemldashboard.experiment.type import ExperimentType

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
        )
        experiments.append(experiment)
    return experiments
