# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['themizer']

package_data = \
{'': ['*'], 'themizer': ['.vscode/*']}

install_requires = \
['colorama>=0.4.6,<0.5.0']

entry_points = \
{'console_scripts': ['themizer = themizer.args:process_args']}

setup_kwargs = {
    'name': 'themizer',
    'version': '1.1.2',
    'description': 'An easy and fast CLI app to change between custom themes in Unix-like systems.',
    'long_description': "# Themizer\n> An easy and fast CLI app to change between custom themes in Unix-like systems\n\n## Installation\n```bash\n> pip install themizer # Install with pip\n> themizer -v # Check if themizer has been installed correctly\n```\n\n## Usage\n**Create a theme:**\n```bash\n> themizer create foo\n```\n\n**Apply a theme:**\n```bash\n> themizer apply bar\n```\n\n**Apply the last used theme:**  \n_When you not specify the theme to use themizer will try to use the last applied theme._\n```bash\n> themizer apply\n```\n\n**Delete a theme:**\n```bash\n> themizer delete baz\n```\n> Note: you can use quotes for themes with spaces in its name. E.g. `themizer apply 'Space Plumber'`\n\n\n## Creating a theme\nIf you create a theme and apply it directly it will raise this error:\n```\n[ ERROR ] The theme config body is empty\n```\nThis happens because you should configure your theme manually, this little guide will help you in the process of create a new one.  \n\n### Theme structure\n\nAll the themes are saved in `~/.config/themizer/themes/` by default, and the structure of a theme looks like this:\n```\n'theme-name/'\n ├── after-execute\n ├── before-execute\n ├── theme.config\n └── ...\n```\n\n| Directory / File |\xa0Description |\n| --- | --- |\n| `theme.config` | Here is stored all info about the theme and the instructions to apply it, more info below. |\n| `before-execute` | This file will be execute before Themizer actually moves the themes and applies it. Use its shebang to execute anything you want. |\n| `after-execute` | The same as `before-execute` but after the theme is actually applied. |\n\n### Configuration of the theme\nThe `theme.config` is spliced in two parts, the header and the body.\n\n\n#### The header:\nThe header stores optional information about the theme itself and the body what directories should move from the theme and where they should go. Looking like this:\n```toml\n[theme] # Header of the theme config\nname = 'custom_name' # The default name is the name of the directory\nclear_terminal = true # By default is false, if is true the theme will clear the terminal after applying the theme\n```\n\n#### The body:\nThe body is former for the relative path of the config to move `theme-name/super-config` and the destination `~/.config/super-app`. Looking like this:\n```toml\n['foobar'] # Relative directory from the theme path\ndest = '~/.config/super-app' # Absolute path (can use ~to refer the home path)\n```\n#### Example:\nDirectory structure:\n```bash\nfoo-theme/\n ├── after-execute\n ├── before-execute\n ├── theme.config\n ├── fish/... # Some config for fish shell\n └── htop/... # Some config for htop\n```\nConfiguration file:\n```toml\n[theme]\nname = 'Kanagawa Theme'\n\n['fish']\ndest = '~/.config/fish'\n\n['htop/htop.config']\ndest = '~/.htop'\n```\n\nWhen you run `themizer apply 'Kanagawa Theme'` themizer will execute `before-script`, copy `foo-theme/fish/` to `~/.config/fish/`, copy `foo-theme/htop.config` to `~/.htop` and finally execute `after-script`.\n\n> Note: The subdirectory `theme` will not work correctly as its name is used to refer the header of the configuration.'\n\n## Configuration\nYour configuration directory is located by default in `~/.config/themizer/`.\n\n### Custom config path\nYou can use your custom path for the config using `--config`:\n```\n> themizer --config /path/to/config/directory\n```\n\n## Scripting\nYou can automatize all the things you can do with Themizer this way:\n```python\nfrom themizer import App\n\ntheme_manager: App = App()\n# You can also set a custom config path\nfrom pathlib import Path\ncustom_theme_manager: App = App(Path('/your/custom/path/'))\n```\nThe `App` class has this set of useful methods to interact with Themizer:\n| Method | Description |\n| --- | --- |\n| `apply_theme(theme_name: str)` | Apply an existing theme. Leave theme_name None to try to use the last theme applied. Return the theme applied. |\n| `create_theme(theme_name: str)` | Create a new theme. |\n| `delete_theme(theme_name: str)` | Delete an existing theme. |\n| `move_theme_config` | Only moves the directories indicated in the theme and not run the 'before' and 'after' scripts. |\n| `run_before_script(theme_name: str)` | Run the 'before' script of the selected theme. |\n| `run_after_script(theme_name: str)` | Run the 'after' script of the selected theme. |\n| `get_theme_config(theme_name: str)` | Return all the config of the theme. |\n| `get_theme_config_head(theme_name: str)` | Return the head of the config of the theme. |\n| `get_theme_config_body(theme_name: str)` | Return the body of the config of the theme. |\n| `get_themes_dict)` | Return a dict with the names of all themes and its internal object. |\n| `set_last_theme_used(theme_name: str)` | Set the last theme to a custom one. |\n| `get_last_theme_used)` | Return the last theme used by the user. |\n| `get_clear_terminal(theme_name: str)` | Return if the theme selected should clear the terminal. |\n\n## Contributing\nFeel free to report a bug or request a branch merge, I appreciate any contribution.\n\n## Author\n\nCreated with :heart: by [Kutu](https://kutu-dev.github.io/).\n> - GitHub - [kutu-dev](https://github.com/kutu-dev)\n> - Twitter - [@kutu_dev](https://twitter.com/kutu_dev)\n",
    'author': 'kutu-dev',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kutu-dev/themizer',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
