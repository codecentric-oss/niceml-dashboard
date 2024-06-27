"""
This module provides custom exception implementations.
"""


class ExperimentTypeNotFoundError(BaseException):
    """
    Exception is thrown when prefix is not found
    """


class ExperimentFilterError(TypeError):
    """
    Custom error class for experiment filter errors.

    This exception is raised when there is a type error in the experiment filtering process.
    """
