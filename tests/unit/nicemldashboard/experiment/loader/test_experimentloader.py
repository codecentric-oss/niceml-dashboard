

from typing import List
from nicemldashboard.experiment.experiment import Experiment
from nicemldashboard.loader.experimentloader import ExperimentLoader


def test_load_experiments(experiment_loader:ExperimentLoader,experiments:List[Experiment]):
    found_experiments = experiment_loader.load_experiments()
    assert sorted(found_experiments) == sorted(experiments)
    



