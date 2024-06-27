"""Module for handling the navigation between pages."""

from abc import ABC, abstractmethod


class Navigable(ABC):
    """Abstract base class for navigable pages."""

    @abstractmethod
    def render(self):
        """Renders the page before the user is navigated to the page"""
        pass

    @abstractmethod
    def update_url(self, url):
        """Updates the URL of the page that the app plans to navigate to.

        Args:
            url: The new URL.
        """
        pass
