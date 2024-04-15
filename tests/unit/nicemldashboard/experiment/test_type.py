from nicemldashboard.experiment.type import ExperimentType


def test_experiment_type_attributes():
    """
    Test attributes of ExperimentType enumeration members.
    """
    assert ExperimentType.SEM_SEG.value.name == "Semantic Segmentation"
    assert ExperimentType.SEM_SEG.value.prefix == "SEG"
    assert ExperimentType.SEM_SEG.value.icon == "o_apps"

    assert ExperimentType.OBJ_DET.value.name == "Object Detection"
    assert ExperimentType.OBJ_DET.value.prefix == "OBD"
    assert ExperimentType.OBJ_DET.value.icon == "o_filter_center_focus"

    assert ExperimentType.CLS.value.name == "Image Classification"
    assert ExperimentType.CLS.value.prefix == "CLS"
    assert ExperimentType.CLS.value.icon == "o_image_search"
