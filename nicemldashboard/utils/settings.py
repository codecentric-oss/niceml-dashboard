"""
Module to define settings and themes for the dashboard.

This module provides classes `Theme` and `Settings` to define themes and read settings
from a YAML file respectively.

Attributes:
    * `Theme`: A data class representing the theme settings for the dashboard.
    * `Settings`: A class to read settings from a YAML file for the dashboard.

"""

from dataclasses import dataclass
from typing import Dict, Optional

import yaml


@dataclass
class Theme:
    """
    Represents the theme settings for the dashboard.

    Attributes:
        primary: Primary color.
        primary_variant: Variant of primary color.
        secondary: Secondary color.
        secondary_variant: Variant of secondary color.
        dark: Dark color.
        positive: Positive color.
        negative: Negative color.
        info: Info color.
        warning: Warning color.
        custom_colors: Custom colors dictionary. Defaults to None.
    """

    primary: str
    primary_variant: str
    secondary: str
    secondary_variant: str
    dark: str
    positive: str
    negative: str
    info: str
    warning: str
    custom_colors: Optional[Dict[str, str]] = None


class Settings:
    """
    Reads settings from a YAML file for the dashboard.
    """

    def __init__(self, settings_path: str):
        """
        Initialize the Settings object.

        Args:
            settings_path: Path to the YAML settings file.
        """
        with open(settings_path, mode="r") as settings_file:
            self.settings_dict = yaml.safe_load(settings_file)

            self.theme: Theme = self._get_theme()

    def _get_theme(self):
        """
        Get the theme settings from the loaded settings dictionary.

        Returns:
            Theme: The theme settings.
        """
        theme_settings = self.settings_dict.get("theme", {})
        return Theme(
            primary=theme_settings.get("primary", "#22F4AE"),
            primary_variant=theme_settings.get("primary_variant", "#1bc38b"),
            secondary=theme_settings.get("secondary", "#F7EA2D"),
            secondary_variant=theme_settings.get("secondary_variant", "#c5bb24"),
            dark=theme_settings.get("dark", "#063022"),
            positive=theme_settings.get("positive", "#38f5b6"),
            negative=theme_settings.get("negative", "#ff6a6f"),
            info=theme_settings.get("info", "#1aceee"),
            warning=theme_settings.get("warning", "#f7ec42"),
            custom_colors=theme_settings.get("custom_colors"),
        )
