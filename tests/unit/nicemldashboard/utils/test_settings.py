from os.path import join

import pytest

from nicemldashboard.utils.settings import Theme, Settings


@pytest.fixture
def sample_settings(tmp_path):
    """
    Fixture to create a sample settings YAML file.
    """
    settings_data = """
    theme:
        primary: "#3366FF"
        primary_variant: "#0033CC"
        secondary: "#FF6633"
        secondary_variant: "#CC3300"
        dark: "#000000"
        positive: "#00CC00"
        negative: "#FF0000"
        info: "#0099FF"
        warning: "#FFCC00"
        custom_colors:
            custom_color1: "#6600CC"
            custom_color2: "#CC0066"
    """
    settings_path = join(tmp_path, "settings.yaml")
    with open(settings_path, "w") as settings_file:
        settings_file.write(settings_data)
    return settings_path


def test_theme_attributes():
    """
    Test attributes of Theme data class.
    """
    custom_colors = {"custom_color1": "#6600CC", "custom_color2": "#CC0066"}
    theme = Theme(
        primary="#3366FF",
        primary_variant="#0033CC",
        secondary="#FF6633",
        secondary_variant="#CC3300",
        dark="#000000",
        positive="#00CC00",
        negative="#FF0000",
        info="#0099FF",
        warning="#FFCC00",
        custom_colors=custom_colors,
    )
    _do_theme_assertion(theme=theme)


def test_settings_theme(sample_settings):
    """
    Test reading theme settings from a YAML file.
    """
    settings = Settings(settings_path=sample_settings)
    theme = settings.theme
    _do_theme_assertion(theme=theme)


def _do_theme_assertion(theme: Theme):
    assert theme.primary == "#3366FF"
    assert theme.primary_variant == "#0033CC"
    assert theme.secondary == "#FF6633"
    assert theme.secondary_variant == "#CC3300"
    assert theme.dark == "#000000"
    assert theme.positive == "#00CC00"
    assert theme.negative == "#FF0000"
    assert theme.info == "#0099FF"
    assert theme.warning == "#FFCC00"
    assert theme.custom_colors == {
        "custom_color1": "#6600CC",
        "custom_color2": "#CC0066",
    }
