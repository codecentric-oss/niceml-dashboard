"""
Module to define a sidebar toggle button for the niceml dashboard.

This module provides a class `SidebarToggleButton` that creates a button for toggling
the visibility of the left sidebar.


Attributes:
    * `SidebarToggleButton`: A class for creating a sidebar toggle button.

"""

from nicegui import ui
from nicegui.page_layout import LeftDrawer


ARROW_LEFT_ICON: str = "o_chevron_left"
ARROW_RIGHT_ICON: str = "o_navigate_next"
MIN_WIDTH: int = 70
MAX_WIDTH: int = 120


class SidebarToggleButton(ui.button):
    """
    A button widget for toggling the visibility of a left sidebar.

    Args:
        *args: Positional arguments to be passed to the base class constructor.
        left_drawer: The left drawer to be toggled.
        min_width: The minimum width of the sidebar. Defaults to 70.
        max_width: The maximum width of the sidebar. Defaults to 120.
        **kwargs: Keyword arguments to be passed to the base class constructor.
    """

    def __init__(
        self,
        *args,
        left_drawer: LeftDrawer,
        min_width: int = MIN_WIDTH,
        max_width: int = MAX_WIDTH,
        **kwargs,
    ) -> None:
        """
        Initialize the SidebarToggleButton.

        Args:
            *args: Positional arguments to be passed to the base class constructor.
            left_drawer: The left drawer to be toggled.
            min_width: The minimum width of the sidebar. Defaults to 70.
            max_width: The maximum width of the sidebar. Defaults to 120.
            **kwargs: Keyword arguments to be passed to the base class constructor.
        """
        super().__init__(*args, **kwargs)
        self.max_width = max_width
        self.min_width = min_width
        self.left_drawer = left_drawer
        self._state = False
        self.classes("sidebar-toggle")
        self.props("flat")
        self.on("click", self.toggle)

    def toggle(self) -> None:
        """
        Toggle the visibility of the sidebar.
        """
        if self._state:
            self.left_drawer.props(f"width={self.min_width}")
        else:
            self.left_drawer.props(f"width={self.max_width}")

        self._state = not self._state
        self.update()

    def is_expanded(self) -> bool:
        """
        Check if the sidebar is currently expanded.

        Returns:
            bool: True if the sidebar is expanded, False otherwise.
        """
        return self._state

    def update(self) -> None:
        """
        Update the button's icon based on the current state of the sidebar.
        """
        self.props(f"icon={ARROW_LEFT_ICON if self._state else ARROW_RIGHT_ICON}")
        super().update()

    def get_props(self) -> dict:
        """
        Get the current props of the `SidebarToggleButton`.

        Returns:
            Props of the `SidebarToggleButton`
        """
        return self._props
