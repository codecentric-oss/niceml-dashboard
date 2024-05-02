"""
This module defines the state management for the NiceML dashboard.
It includes the EventManager class for handling event dictionaries and observable dictionaries.
Also includes helper functions to initialize and get the instance of the Event Manager.
Enums for Dicts are defined for consistency.
"""
from abc import ABC, ABCMeta
from enum import Enum, EnumMeta
from nicegui import context
import logging
from nicegui.observables import ObservableDict

logger = logging.getLogger(__name__)

_EVENT_MNGR_ATTR_NAME = "_nicemldashboard"


class StateKeys(ABCMeta, EnumMeta):
    """
    Provides an abstract class for StateKey management
    """


class EventManager:
    """
    Manages event dictionaries and provides methods to retrieve and manage them.
    """

    _observable_dicts: dict[StateKeys, ObservableDict]

    def __init__(self):
        """
        Initializes the EventManager with an empty dictionary of observable dictionaries.
        """
        self._observable_dicts = {}

    def get_dict(self, dict_name: str) -> ObservableDict:
        """
        Retrieves an observable dictionary by name, creating a new one if it doesn't exist.

        Args:
            dict_name (str): The name of the dictionary to retrieve.

        Returns:
            ObservableDict: The retrieved or newly created observable dictionary.
        """
        if dict_name in self._observable_dicts:
            return self._observable_dicts[dict_name]
        else:
            new_dict = ObservableDict()
            self._observable_dicts[dict_name] = new_dict
            return new_dict


def _get_event_manager() -> EventManager:
    """
    Retrieves the EventManager instance from the current client context.

    Returns:
        EventManager: The EventManager instance.

    Raises:
        RuntimeError: If Event Manager is not initialized.
    """
    client = context.get_client()
    if not hasattr(client, _EVENT_MNGR_ATTR_NAME):
        raise RuntimeError("Event Manager needs to be initialized with init_store")
    return getattr(client, _EVENT_MNGR_ATTR_NAME)


def init_event_manager(event_manager: EventManager):
    """
    Initializes the EventManager for the current client context.
    If already initialized, gives back a console output.

    Args:
        event_manager (EventManager): The EventManager instance to initialize.
    """
    try:
        client = context.get_client()
        if getattr(client, _EVENT_MNGR_ATTR_NAME, None) is None:
            setattr(client, _EVENT_MNGR_ATTR_NAME, event_manager)
    except RuntimeError:
        logger.debug("Event Manager cannot be initialized in a background task")

class StateEvent(ABCMeta, EnumMeta):
    """
    Manages the keys for the observable dictionaries
    """


class ExperimentEvents(StateEvent):
    """
    Manages the experimente events in the observable dictionaries
    """

    ON_EXPERIMENT_PREFIX_CHANGE = "on_experiment_prefix_change"


class ExperimentStateKeys(StateKeys):
    """
    Manages the observable dictionaries
    """

    EXPERIMENT_DICT = "experiment_dict"
