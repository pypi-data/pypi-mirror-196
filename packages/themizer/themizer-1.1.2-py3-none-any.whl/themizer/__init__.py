# themizer - Created with ♥ by Kutu (https://kutu-dev.github.io/)

# Define global variables
__version__: str = '1.1.2'
APP_NAME: str = 'themizer'

# Change the controller name to a more pleasant one
from .controller import Controller as App
