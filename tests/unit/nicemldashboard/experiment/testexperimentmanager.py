import pytest
from nicemldashboard.experiment.experiment_manager import ExperimentManager
from nicemldashboard.experiment.utils import get_random_experiments


@pytest.fixture
def experiments():
    return get_random_experiments(50, seed=42)


@pytest.fixture
def experiment_manager(experiments):
    return ExperimentManager(experiments)


def test_filter_by_name(experiment_manager, experiments):
    name_to_test = experiments[0].name
    filtered = experiment_manager.filter_by(name=name_to_test)
    assert len(filtered) == 1

    non_filtered_experiments = [exp for exp in experiments if exp.name != name_to_test]
    assert all(exp.name != name_to_test for exp in non_filtered_experiments)


def test_filter_by_id(experiment_manager, experiments):
    id_to_test = experiments[0].experiment_id
    filtered = experiment_manager.filter_by(experiment_id=id_to_test)
    assert len(filtered) == 1

    non_filtered_experiments = [
        exp for exp in experiments if exp.experiment_id != id_to_test
    ]
    assert all(exp.experiment_id != id_to_test for exp in non_filtered_experiments)


def test_filter_by_experiment_type(experiment_manager, experiments):
    experiment_type_to_test = experiments[0].experiment_type
    filtered = experiment_manager.filter_by(experiment_type=experiment_type_to_test)
    assert all(exp.experiment_type == experiment_type_to_test for exp in filtered)

    experiments_not_filtered = [exp for exp in experiments if exp not in filtered]
    assert all(
        exp.experiment_type != experiment_type_to_test
        for exp in experiments_not_filtered
    )


def test_filter_by_nonexistent_field(experiment_manager):
    filtered = experiment_manager.filter_by(nonexistent_field="dummy")
    assert len(filtered) == 0


def test_filter_by_multiple_fields_name_and_id(experiment_manager, experiments):
    first_experiment = experiments[0]
    filtered = experiment_manager.filter_by(
        name=first_experiment.name, experiment_id=first_experiment.experiment_id
    )
    assert len(filtered) == 1
    experiments_not_filtered = [exp for exp in experiments if exp not in filtered]
    assert all(
        exp.name != first_experiment.name
        and exp.experiment_id != first_experiment.experiment_id
        for exp in experiments_not_filtered
    )


def test_filter_by_multiple_fields_experiment_type_and_git_version(
    experiment_manager, experiments
):
    first_experiment = experiments[0]
    filtered = experiment_manager.filter_by(
        experiment_type=first_experiment.experiment_type,
        git_version=first_experiment.git_version,
    )
    assert all(
        exp.experiment_type == first_experiment.experiment_type for exp in filtered
    )
    assert all(exp.git_version == first_experiment.git_version for exp in filtered)

    experiments_not_filtered = [exp for exp in experiments if exp not in filtered]
    assert all(
        not (
            exp.experiment_type == first_experiment.experiment_type
            and exp.git_version == first_experiment.git_version
        )
        for exp in experiments_not_filtered
    )


def test_filter_with_no_criteria(experiment_manager, experiments):
    filtered = experiment_manager.filter_by()
    assert len(filtered) == len(experiments)
    assert filtered == experiments
