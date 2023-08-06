# Themizer
> An easy and fast CLI app to change between custom themes in Unix-like systems

## Installation
```bash
> pip install themizer # Install with pip
> themizer -v # Check if themizer has been installed correctly
```

## Usage
**Create a theme:**
```bash
> themizer create foo
```

**Apply a theme:**
```bash
> themizer apply bar
```

**Apply the last used theme:**  
_When you not specify the theme to use themizer will try to use the last applied theme._
```bash
> themizer apply
```

**Delete a theme:**
```bash
> themizer delete baz
```
> Note: you can use quotes for themes with spaces in its name. E.g. `themizer apply 'Space Plumber'`


## Creating a theme
If you create a theme and apply it directly it will raise this error:
```
[ ERROR ] The theme config body is empty
```
This happens because you should configure your theme manually, this little guide will help you in the process of create a new one.  

### Theme structure

All the themes are saved in `~/.config/themizer/themes/` by default, and the structure of a theme looks like this:
```
'theme-name/'
 ├── after-execute
 ├── before-execute
 ├── theme.config
 └── ...
```

| Directory / File | Description |
| --- | --- |
| `theme.config` | Here is stored all info about the theme and the instructions to apply it, more info below. |
| `before-execute` | This file will be execute before Themizer actually moves the themes and applies it. Use its shebang to execute anything you want. |
| `after-execute` | The same as `before-execute` but after the theme is actually applied. |

### Configuration of the theme
The `theme.config` is spliced in two parts, the header and the body.


#### The header:
The header stores optional information about the theme itself and the body what directories should move from the theme and where they should go. Looking like this:
```toml
[theme] # Header of the theme config
name = 'custom_name' # The default name is the name of the directory
clear_terminal = true # By default is false, if is true the theme will clear the terminal after applying the theme
```

#### The body:
The body is former for the relative path of the config to move `theme-name/super-config` and the destination `~/.config/super-app`. Looking like this:
```toml
['foobar'] # Relative directory from the theme path
dest = '~/.config/super-app' # Absolute path (can use ~to refer the home path)
```
#### Example:
Directory structure:
```bash
foo-theme/
 ├── after-execute
 ├── before-execute
 ├── theme.config
 ├── fish/... # Some config for fish shell
 └── htop/... # Some config for htop
```
Configuration file:
```toml
[theme]
name = 'Kanagawa Theme'

['fish']
dest = '~/.config/fish'

['htop/htop.config']
dest = '~/.htop'
```

When you run `themizer apply 'Kanagawa Theme'` themizer will execute `before-script`, copy `foo-theme/fish/` to `~/.config/fish/`, copy `foo-theme/htop.config` to `~/.htop` and finally execute `after-script`.

> Note: The subdirectory `theme` will not work correctly as its name is used to refer the header of the configuration.'

## Configuration
Your configuration directory is located by default in `~/.config/themizer/`.

### Custom config path
You can use your custom path for the config using `--config`:
```
> themizer --config /path/to/config/directory
```

## Scripting
You can automatize all the things you can do with Themizer this way:
```python
from themizer import App

theme_manager: App = App()
# You can also set a custom config path
from pathlib import Path
custom_theme_manager: App = App(Path('/your/custom/path/'))
```
The `App` class has this set of useful methods to interact with Themizer:
| Method | Description |
| --- | --- |
| `apply_theme(theme_name: str)` | Apply an existing theme. Leave theme_name None to try to use the last theme applied. Return the theme applied. |
| `create_theme(theme_name: str)` | Create a new theme. |
| `delete_theme(theme_name: str)` | Delete an existing theme. |
| `move_theme_config` | Only moves the directories indicated in the theme and not run the 'before' and 'after' scripts. |
| `run_before_script(theme_name: str)` | Run the 'before' script of the selected theme. |
| `run_after_script(theme_name: str)` | Run the 'after' script of the selected theme. |
| `get_theme_config(theme_name: str)` | Return all the config of the theme. |
| `get_theme_config_head(theme_name: str)` | Return the head of the config of the theme. |
| `get_theme_config_body(theme_name: str)` | Return the body of the config of the theme. |
| `get_themes_dict)` | Return a dict with the names of all themes and its internal object. |
| `set_last_theme_used(theme_name: str)` | Set the last theme to a custom one. |
| `get_last_theme_used)` | Return the last theme used by the user. |
| `get_clear_terminal(theme_name: str)` | Return if the theme selected should clear the terminal. |

## Contributing
Feel free to report a bug or request a branch merge, I appreciate any contribution.

## Author

Created with :heart: by [Kutu](https://kutu-dev.github.io/).
> - GitHub - [kutu-dev](https://github.com/kutu-dev)
> - Twitter - [@kutu_dev](https://twitter.com/kutu_dev)
