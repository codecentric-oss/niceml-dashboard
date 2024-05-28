import pytest
from unittest.mock import MagicMock

from nicemldashboard.basecomponents.buttons.sidebartogglebutton import (
    ARROW_RIGHT_ICON,
    ARROW_LEFT_ICON,
    MAX_WIDTH,
    MIN_WIDTH,
)
from nicemldashboard.basecomponents.buttons.sidebartogglebutton import (
    SidebarToggleButton,
)


@pytest.fixture
def mock_left_drawer() -> MagicMock:
    """
    Fixture to mock the LeftDrawer instance.
    """
    return MagicMock()


def test_sidebar_toggle_button_initialization(mock_left_drawer):
    """
    Test initialization of SidebarToggleButton.
    """
    button = SidebarToggleButton(left_drawer=mock_left_drawer)
    assert button.max_width == MAX_WIDTH
    assert button.min_width == MIN_WIDTH
    assert button.left_drawer == mock_left_drawer


@pytest.mark.parametrize(
    "initial_state, expected_width, expected_icon",
    [(False, MAX_WIDTH, ARROW_RIGHT_ICON), (True, MIN_WIDTH, ARROW_LEFT_ICON)],
)
def test_toggle_method(
    mock_left_drawer: MagicMock,
    initial_state: bool,
    expected_width: int,
    expected_icon: str,
):
    """
    Test toggle method of SidebarToggleButton.
    """
    button = SidebarToggleButton(left_drawer=mock_left_drawer)
    button._state = initial_state
    button.toggle()
    assert mock_left_drawer.props.call_args[0][0] == f"width={expected_width}"
    assert button._state == (not initial_state)
    assert button.get_props()["icon"] == expected_icon


def test_is_expanded_method():
    """
    Test is_expanded method of SidebarToggleButton.
    """
    button = SidebarToggleButton(left_drawer=MagicMock())
    assert button.is_expanded() == False
    button._state = True
    assert button.is_expanded() == True
