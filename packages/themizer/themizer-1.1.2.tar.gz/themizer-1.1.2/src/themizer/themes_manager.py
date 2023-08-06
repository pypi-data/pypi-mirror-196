from .exceptions import ThemeNotFound, ThemeAlreadyExists, DuplicatedThemeName, except_handler
from .theme_model import Theme
from .config import ConfigManager
from .messages import error, info
from pathlib import Path
import shutil
import sys

class ThemeManager():
    def __init__(self, themes_path: Path, config: ConfigManager) -> None:
        self.themes_path: Path = themes_path
        self.config: ConfigManager = config
        self.set_themes()

    def set_themes(self) -> None:
        """Iterate the themes directory and assign each theme to a path in a dict"""
        self.themes: dict[str, Theme] = {}

        # Generate a list with all files and directories inside the themes directory
        for i in self.themes_path.glob('*'):
            if not i.is_dir():
                continue

            current_theme: Theme = Theme(i, self.config)

            try:
                self.themes[current_theme.get_theme_name()]
            except KeyError:
                self.themes[
                    # Get the directory name as set as the key of a dict
                    current_theme.get_theme_name()
                ] = current_theme
            else:
                # If a theme with the same name already exist raise an exception
                with except_handler():
                    raise DuplicatedThemeName

    def create_theme(self, theme_name: str) -> None:
        try:
            self.themes[theme_name]
        except KeyError as e:
            self.themes[theme_name] = Theme(Path(self.themes_path, theme_name), self.config)
        else:
            with except_handler():
                raise ThemeAlreadyExists

    def delete_theme(self, theme_name: str) -> None:
        try:
            requested_theme: Theme = self.themes[theme_name]
            shutil.rmtree(
                requested_theme.theme_path
            )
        except KeyError:
            with except_handler():
                raise ThemeNotFound from None
        else:
            return requested_theme

    def get_theme(self, theme_name: str | None) -> Theme:
        """Return a reference to the object of the theme requested"""
        last_theme_mode: bool = (theme_name == None)

        # Get the last theme applied
        if last_theme_mode:
            theme_name = self.config.get_last_theme_used()

        try:
            # Try get the selected theme
            return self.themes[theme_name]
        except KeyError:
            with except_handler():
                # Check if it's a normal theme request
                if not last_theme_mode:
                    raise ThemeNotFound from None

                # Check if exists data in the file theme.last
                if theme_name != '':
                    error('The last used theme is not available')
                    self.config.regenerate_last_theme_used()
                    sys.exit(1)

                if theme_name == '':
                    error('You have never used a theme')
                    self.config.regenerate_last_theme_used()
                    sys.exit(1)

    
    def get_themes_dict(self) -> dict:
        """Return a list with the name of all themes available"""
        return self.themes
