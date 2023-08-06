from .messages import raw_error
from contextlib import contextmanager
import sys

@contextmanager
def except_handler():
    """Sets a custom exception handler with the 'with' keyword"""
    
    def custom_excepthook(type, value, traceback) -> None:
        print(value)
    sys.excepthook = custom_excepthook
    
    yield
    sys.excepthook = sys.__excepthook__

class CustomBaseException(Exception):
    """A base exception to print all the exceptions with the correct text format and color"""
    def __init__(self) -> None:
        super().__init__()
        self.error_message: str

    def __str__(self) -> str:
        return raw_error(self.error_message)

class ThemeNotFound(CustomBaseException):
    """The theme has not found in the themes directory"""

    def __init__(self) -> None:
        super().__init__()
        self.error_message = 'The theme has not found in the themes directory'

class ThemeAlreadyExists(CustomBaseException):
    """The theme already exist in the themes directory"""
    
    def __init__(self) -> None:
        super().__init__()
        self.error_message = 'The theme already exist in the themes directory'

class DuplicatedThemeName(CustomBaseException):
    """Already exist a theme with the same name"""
    
    def __init__(self) -> None:
        super().__init__()
        self.error_message = 'Already exist a theme with the same name'

class ConfigBodyIsEmpty(CustomBaseException):
    """The theme config body is empty"""
    
    def __init__(self) -> None:
        super().__init__()
        self.error_message = 'The theme config body is empty'

class SavedConfigNotFound(CustomBaseException):
    """The selected configuration does not exist"""

    def __init__(self) -> None:
        super().__init__()
        self.error_message = 'The selected configuration does not exist'

class DestNotFound(CustomBaseException):
    """The destination directory does not exist"""

    def __init__(self) -> None:
        super().__init__()
        self.error_message = 'The destination directory does not exist'

class InvalidClearTerminalStatus(CustomBaseException):
    """The value in clear_terminal is invalid"""

    def __init__(self) -> None:
        super().__init__()
        self.error_message = 'The value in clear_terminal is invalid'
