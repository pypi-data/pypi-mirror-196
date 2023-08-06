from .config import ConfigManager
from.themes_manager import ThemeManager
from .theme_model import Theme
from pathlib import Path

class Controller():
    def __init__(self, custom_user_config_path: None | Path = None) -> None:
        self.config: ConfigManager = ConfigManager(custom_user_config_path)
        self.themes: ThemeManager = ThemeManager(
            self.config.get_themes_path(),
            self.config
        )

    def apply_theme(self, theme_name: str | None) -> str:
        """
        Apply an existing theme
        Leave theme_name None to try to use the last theme applied
        Return the theme applied
        """
        self.themes.get_theme(theme_name).apply_theme()

        return self.themes.get_theme(theme_name).get_theme_name()

    def create_theme(self, theme_name: str) -> None:
        """Create a new theme"""
        self.themes.create_theme(theme_name)

    def delete_theme(self, theme_name: str) -> None:
        """Delete an existing theme"""
        self.themes.delete_theme(theme_name)

    def move_theme_config(self, theme_name: str) -> None:
        """Only moves the directories indicated in the theme and not run the 'before' and 'after' scripts"""
        self.themes.get_theme(theme_name).move_configs()

    def run_before_script(self, theme_name: str) -> None:
        """Run the 'before' script of the selected theme"""
        selected_theme: Theme = self.themes.get_theme(theme_name)

        selected_theme.run_script(
            selected_theme.before_script_path
        )

    def run_after_script(self, theme_name: str) -> None:
        """Run the 'after' script of the selected theme"""
        selected_theme: Theme = self.themes.get_theme(theme_name)

        selected_theme.run_script(
            selected_theme.after_script_path
        )

    def get_theme_config(self, theme_name: str) -> dict:
        """Return all the config of the theme"""
        return self.themes.get_theme(theme_name).get_theme_config()

    def get_theme_config_head(self, theme_name: str) -> dict:
        """Return the head of the config of the theme"""
        return self.themes.get_theme(theme_name).get_theme_internal_config()

    def get_theme_config_body(self, theme_name: str) -> dict:
        """Return the body of the config of the theme"""
        return self.themes.get_theme(theme_name).get_theme_guidelines_config()

    def get_themes_dict(self) -> dict:
        """Return a dict with the names of all themes and its internal object"""
        return self.themes.get_themes_dict()

    def set_last_theme_used(self, theme_name: str) -> str:
        """Set the last theme to a custom one"""
        self.config.set_last_theme_used(theme_name)

    def get_last_theme_used(self) -> str:
        """Return the last theme used by the user"""
        return self.config.get_last_theme_used()

    def get_clear_terminal(self, theme_name: str) -> bool:
        """Return if the theme selected should clear the terminal"""
        return self.themes.get_theme(theme_name).get_clear_terminal()
