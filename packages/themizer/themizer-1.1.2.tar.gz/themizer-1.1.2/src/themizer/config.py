from . import APP_NAME
from pathlib import Path
import platform

class ConfigManager():
    def __init__(self, custom_user_config_path: None | Path = None) -> None:
        self.set_config_paths(custom_user_config_path)
        self.check_config_paths()

    def set_config_paths(self, custom_user_config_path: None | Path) -> None:
        """Set the config path of the user and set the path for the package config"""
        self.user_config_path: Path
        if custom_user_config_path is not None:
            self.user_config_path = custom_user_config_path
        else:
            self.user_config_path = self.get_default_user_config_path()
        
        self.theme_config_path = Path(self.user_config_path, APP_NAME)

        self.themes_path: Path = Path(self.theme_config_path, 'themes')
        self.last_theme_path: Path = Path(self.theme_config_path, 'theme.last')

    def get_default_user_config_path(self) -> Path:
        if platform.system == 'Windows':
            return Path(
                Path.home(),
                'AppData',
                'Roaming'
            )
        
        return Path(
            Path.home(),
            '.config'
            )

    def check_config_paths(self) -> None:
        """Check if the paths exists and if one of them is missing create it"""

        self.themes_path.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.last_theme_path.is_file():
            self.last_theme_path.touch()
            self.regenerate_last_theme_used()

    def get_themes_path(self) -> Path:
        return self.themes_path

    def get_last_theme_path(self) -> Path:
        return self.last_theme_path

    def get_last_theme_used(self) -> str:
        with open(self.last_theme_path, 'r') as file:
                return file.read().replace('\n', '')

    def set_last_theme_used(self, theme_name: str) -> None:
        with open(self.last_theme_path, 'w') as file:
            file.write(f'{theme_name}\n')

    def regenerate_last_theme_used(self) -> None:
        with open(self.last_theme_path, 'w') as file:
            file.write('\n')
