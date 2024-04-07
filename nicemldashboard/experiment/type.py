"""
Module to define experiment types.

This module provides an enumeration `ExperimentType` representing different types
of experiments, each with a name, prefix, and icon.

Attributes:
    * `ExperimentType`: An enumeration representing different types of experiments.

"""

from dataclasses import dataclass
from enum import Enum


@dataclass
class _ExperimentType:
    """
    Represents an experiment type with a name, prefix, and icon.

    Attributes:
        name: The name of the experiment type.
        prefix: The prefix for the experiment type.
        icon: The icon representing the experiment type.
    """

    name: str
    prefix: str
    icon: str


class ExperimentType(Enum):
    """
    Enumeration representing different types of experiments.

    Attributes:
        SEM_SEG: Semantic Segmentation experiment type.
        OBJ_DET: Object Detection experiment type.
        CLS: Image Classification experiment type.
    """

    SEM_SEG = _ExperimentType(name="Semantic Segmentation", prefix="SEG", icon="o_apps")
    OBJ_DET = _ExperimentType(
        name="Object Detection", prefix="OBD", icon="o_filter_center_focus"
    )
    CLS = _ExperimentType(
        name="Image Classification", prefix="CLS", icon="o_image_search"
    )