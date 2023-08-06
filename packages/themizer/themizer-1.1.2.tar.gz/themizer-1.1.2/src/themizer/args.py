from .controller import Controller
from .messages import info, ok, error
from . import __version__, APP_NAME
from argparse import ArgumentParser, Namespace
from pathlib import Path
import sys
import colorama

def process_args() -> None:
    """This function analyze the CLI arguments and start the app according to them"""
    # Define app's metadata
    parser: ArgumentParser = ArgumentParser(
        prog=f'{APP_NAME}',
        description=f'{APP_NAME} - An easy and fast CLI app to change between custom themes in Unix-like systems',
        epilog='Created with ♥ by Kutu (https://kutu-dev.github.io/)'
    )

    parser.add_argument(
        '-v',
        '--version',
        action='store_true',
        help=f'show the current installed version of {APP_NAME}',
        default=False
        )

    parser.add_argument(
        '-c',
        '--config',
        metavar='path',
        default=None,
        type=Path,
        help='Select a custom path equivalent of ~/.config',
    )

    subparsers: ArgumentParser = parser.add_subparsers(
        dest='mode',
    )

    # Apply mode arguments

    apply_subparser: ArgumentParser = subparsers.add_parser(
        'apply',
        help='apply the selected theme globally'
        )

    apply_subparser.add_argument(
        'theme_name',
        help='name of the theme to apply',
        default=None,
        nargs='?'
        )

    apply_subparser.add_argument(
        '-c',
        '--config',
        metavar='path',
        default=None,
        type=Path,
        help='Select a custom path equivalent of ~/.config',
    )

    # Create mode arguments

    create_subparser: ArgumentParser = subparsers.add_parser(
        'create',
        help='create a new theme'
        )

    create_subparser.add_argument(
        'theme_name',
        help='name of the theme to create'
        )

    create_subparser.add_argument(
        '-c',
        '--config',
        metavar='path',
        default=None,
        type=Path,
        help='Select a custom path equivalent of ~/.config',
    )

    # Delete mode arguments

    delete_subparser: ArgumentParser = subparsers.add_parser(
        'delete',
        help='delete the selected theme'
        )

    delete_subparser.add_argument(
        'theme_name',
        help='name of the theme to delete'
        )

    delete_subparser.add_argument(
        '-c',
        '--config',
        metavar='path',
        default=None,
        type=Path,
        help='Select a custom path equivalent of ~/.config',
    )

    # List mode arguments

    list_subparser: ArgumentParser = subparsers.add_parser(
        'list',
        help='List all the themes available'
        )

    list_subparser.add_argument(
        '-c',
        '--config',
        metavar='path',
        default=None,
        type=Path,
        help='Select a custom path equivalent of ~/.config',
    )

    args: Namespace = parser.parse_args()

    if args.version == True:
        info(f'{APP_NAME} {__version__}')
        sys.exit(0)

    controller: Controller = Controller(args.config)

    match args.mode:
        case 'apply':
            applied_theme_name: str = controller.apply_theme(args.theme_name)

            if not controller.get_clear_terminal(args.theme_name):
                ok(f'Theme \'{applied_theme_name}\' applied')
        case 'create':
            controller.create_theme(args.theme_name)
            ok(f'Theme \'{args.theme_name}\' created')
        case 'delete':
            controller.delete_theme(args.theme_name)
            ok(f'Theme \'{args.theme_name}\' deleted')
        case 'list':
            # Get all themes names and print them
            themes: dict = controller.get_themes_dict()

            themes_name: list[str] = [x for x in themes]

            last_theme: str = controller.get_last_theme_used()
            if last_theme == '':
                info('Available themes:')
                for i in themes_name:
                    print(f'\t\t- {i}')
                return

            # Try to remove the last theme used from the theme list
            try:
                themes_name.remove(last_theme)
            except ValueError:
                pass
            
            info('Available themes:')

            colorama.init()
            print(f'{colorama.Style.BRIGHT}\t\t- {last_theme}{colorama.Style.RESET_ALL} (Selected)')

            for i in themes_name:
                print(f'\t\t- {i}')
        case _:
            error('You have not selected a mode, use \'themizer --help\' for more information')
