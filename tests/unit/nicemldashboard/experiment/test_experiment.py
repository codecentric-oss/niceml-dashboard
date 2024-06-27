from nicemldashboard.experiment.experiment import Experiment, format_string
from nicemldashboard.experiment.type import ExperimentType


def test_experiment_instance():
    """
    Test instantiation of Experiment class.
    """
    experiment = Experiment(
        experiment_type=ExperimentType.SEM_SEG,
        name="Test Experiment",
        description="Description of the test experiment",
        experiment_id="123456",
        short_id="ABC",
        git_version={"nicemldashboard": "v1.0"},
        data_set="test datasets",
    )
    assert isinstance(experiment, Experiment)


def test_experiment_get_row():
    """
    Test get_row method of Experiment class.
    """
    experiment = Experiment(
        experiment_type=ExperimentType.SEM_SEG,
        name="Test Experiment",
        description="Description of the test experiment",
        experiment_id="123456",
        short_id="ABC",
        git_version={"nicemldashboard": "v1.0", "niceml": "v0.11.0"},
        data_set="test datasets",
    )
    row = experiment.get_row()
    assert row["git_version"] == "nicemldashboard:v1.0, niceml:v0.11.0"
    assert row["short_id"] == "ABC"
    assert row["experiment_id"] == "123456"
    assert row["description"] == "Description of the test experiment"
    assert row["name"] == "Test Experiment"
    assert row["experiment_type"] == ExperimentType.SEM_SEG
    assert row["data_set"] == "test datasets"


def test_experiment_get_columns():
    """
    Test get_columns method of Experiment class.
    """
    columns = Experiment.get_columns()
    expected_columns = [
        {
            "name": "name",
            "label": "Name",
            "field": "name",
            "align": "left",
            "sortable": True,
        },
        {
            "name": "description",
            "label": "Description",
            "field": "description",
            "align": "left",
            "sortable": True,
        },
        {
            "name": "experiment_id",
            "label": "Experiment id",
            "field": "experiment_id",
            "align": "left",
            "sortable": True,
        },
        {
            "name": "short_id",
            "label": "Short id",
            "field": "short_id",
            "align": "left",
            "sortable": True,
        },
        {
            "name": "git_version",
            "label": "Git version",
            "field": "git_version",
            "align": "left",
            "sortable": True,
        },
        {
            "name": "data_set",
            "label": "Data set",
            "field": "data_set",
            "align": "left",
            "sortable": True,
        },
    ]
    assert columns == expected_columns


def test_format_string():
    """
    Test format_string function.
    """
    formatted_string = format_string("test_string_with_underscores")
    assert formatted_string == "Test string with underscores"
