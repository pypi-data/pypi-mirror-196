from .exceptions import SavedConfigNotFound, ConfigBodyIsEmpty, DestNotFound, InvalidClearTerminalStatus, except_handler
from .messages import ask, info, error, ok
from .config import ConfigManager
from pathlib import Path
from enum import Enum
from os import access, X_OK
import subprocess
import tomllib
import shutil
import getpass
import stat
import sys

# Generate the message of the scripts
def GENERIC_SCRIPT_MESSAGE_GENERATOR(when: str) -> list[str]:
    return [
            '#!/usr/bin/env sh\n',
            '\n'
            f'# This file will be executed {when} this theme is applied.\n',
            '# You can change the shebang to anything you need and it will work.\n'
    ]

class SCRIPT_MESSAGE(Enum):
    BEFORE: list[str] = GENERIC_SCRIPT_MESSAGE_GENERATOR('before')
    AFTER: list[str] = GENERIC_SCRIPT_MESSAGE_GENERATOR('after')

class Theme():
    def __init__(self, theme_path: Path, config: ConfigManager) -> None:
        self.theme_path: Path = theme_path
        self.config: ConfigManager = config
    
        # A script that should be executed before applying the theme
        self.before_script_path: Path = Path(theme_path, 'before-execute')
        # A script that should be executed after applying the theme
        self.after_script_path: Path = Path(theme_path, 'after-execute')

        self.theme_config_path: Path = Path(theme_path, 'theme.config')

        # Check if all the paths and permissions are set
        self.check_theme()

        # After all checks all done set the theme config
        self.set_theme_config()

    def check_theme(self) -> None:
        # Check if the theme itself exist
        if not self.theme_path.is_dir():
            self.theme_path.mkdir(
                exist_ok=True,
                parents=True
            )

        # Check if the scripts exists
        self.check_script(self.before_script_path, SCRIPT_MESSAGE.BEFORE.value)
        self.check_script(self.after_script_path, SCRIPT_MESSAGE.AFTER.value)

        # Check if the config is set up
        self.check_config()

    def check_script(self, script_to_check: Path, message: list[str]) -> None:
        if not script_to_check.is_file():
            self.generate_script(script_to_check, message)

        # Check and set if the script is executable
        # Using os library is easier than using pathlib
        if not access(script_to_check, X_OK):
            # Get the current permissions of the file and add the user permission of execute
            script_permissions: int = stat.S_IMODE(script_to_check.stat()[0])
            script_to_check.chmod(script_permissions + 0o100)


    def generate_script(self, script_to_generate: Path , message: list[str]):
        script_to_generate.touch()

        with open(script_to_generate, 'w') as file:
            file.writelines(
                message
            )

    def check_config(self) -> None:
        self.theme_config_path.touch(exist_ok=True)

        with open(self.theme_config_path, 'rb') as file:
            try:
                tomllib.load(file)
            except tomllib.TOMLDecodeError as e:
                # If the file is not a valid TOML file overwrite it with only a newline char
                info(f'Invalid TOML config file in for the theme \'{self.get_theme_name()}\' in \'{self.theme_config_path}\'')
                if ask('You want to regenerate the default config', True):
                    self.generate_default_config()
                    ok('Config regenerated')
                else:
                    error('Not possible to continue without a valid config')
                    sys.exit(1)

    def generate_default_config(self) -> None:
        with open(self.theme_config_path, 'w') as file:
            file.write('\n')

    def set_theme_config(self) -> None:
        with open(self.theme_config_path, 'rb') as file:
            self.raw_theme_config: dict = tomllib.load(file)

            # The header of the config file with some metadata values
            self.theme_internal_config: dict
            try:
                self.theme_internal_config = self.raw_theme_config['theme']
            except KeyError as e:
                self.theme_internal_config = {}

            # The body of the config file where is indicated where each directory should be
            self.theme_guidelines_config: dict = {x: self.raw_theme_config[x] for x in self.raw_theme_config if x != 'theme'}

    def get_theme_config(self) -> dict:
        return self.raw_theme_config

    def get_theme_internal_config(self) -> dict:
        return self.theme_internal_config

    def get_theme_guidelines_config(self) -> dict:
        return self.theme_guidelines_config

    def get_theme_name(self) -> str:
        try:
            return self.theme_internal_config['name']
        except (KeyError, AttributeError):
            return str(self.theme_path.parts[-1])

    def get_clear_terminal(self) -> bool:
        try:
            clear_terminal: bool = self.theme_internal_config['clear_terminal']
        except KeyError:
            return False

        if not clear_terminal in (True, False):
            with except_handler():
                raise InvalidClearTerminalStatus

        return clear_terminal

    def apply_theme(self) -> None:
        self.run_script(self.before_script_path)
        self.move_configs()
        if self.get_clear_terminal():
            subprocess.Popen('clear')
        self.run_script(self.after_script_path)
        self.config.set_last_theme_used(self.get_theme_name())

    def run_script(self, script_to_execute) -> None:
        # Convert the path to a string and execute it
        subprocess.call([str(script_to_execute)])

    def move_configs(self) -> None:
        if self.theme_guidelines_config == {}:
                with except_handler():
                   raise ConfigBodyIsEmpty

        # Iterate each directory/file the user want to copy
        for i in self.theme_guidelines_config:
            # Get the file or directory the user has provided
            current_config_path: Path = Path(self.theme_path, i)

            if not current_config_path.is_dir() and not current_config_path.is_file():
                with except_handler():
                    raise SavedConfigNotFound
            
            try:
                dest_config_path: Path = Path(self.theme_guidelines_config[i]['dest'])
            except KeyError as e:
                with except_handler():
                    raise DestNotFound from None

            # Convert Unix home char to absolute path
            if dest_config_path.parts[0] == '~':
                dest_config_path = Path(
                    Path.home(),
                    Path(*dest_config_path.parts[1::])
                )

            if current_config_path.is_dir():
                # If is a directory
                self.move_directory(current_config_path, dest_config_path)
            else:
                # If is a file
                self.move_file(current_config_path, dest_config_path)

    def move_directory(self, from_directory_path: Path, dest_directory_path) -> None:
        # Delete the destination directory if it already exists
        if dest_directory_path.is_dir():
            shutil.rmtree(dest_directory_path)

        # Copy all content from theme to destination
        shutil.copytree(from_directory_path, dest_directory_path)

    def move_file(self, from_file_path: Path, dest_file_path: Path) -> None:
        # Delete the destination file if it already exists
        if dest_file_path.is_dir():
            shutil.unlink(dest_file_path)

        # Copy the from file to the destination file
        shutil.copy(from_file_path, dest_file_path)
