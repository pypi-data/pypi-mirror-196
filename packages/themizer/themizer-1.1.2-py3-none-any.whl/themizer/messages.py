import typing
import colorama
from colorama import Fore, Style

colorama.init()

def info(message: str, *args, **kwargs) -> None:
    """Print a decorated info message"""
    print(f'[ {Fore.BLUE}INFO{Style.RESET_ALL} ] {message}', *args, **kwargs)

def ok(message: str, *args, **kwargs) -> None:
    """Print a decorated info message"""
    print(f'[ {Fore.GREEN}OK{Style.RESET_ALL} ] {message}', *args, **kwargs)

def warn(message: str, *args, **kwargs) -> None:
    """Print a decorated warning message"""
    print(f'[ {Fore.YELLOW}WARN{Style.RESET_ALL} ] {message}', *args, **kwargs)

def error(message: str, *args, **kwargs) -> None:
    """Print a decorated error message"""
    print(f'[ {Fore.RED}ERROR{Style.RESET_ALL} ] {message}', *args, **kwargs)

def raw_error(message: str) -> str:
    return f'[ {Fore.RED}ERROR{Style.RESET_ALL} ] {message}'

def ask(
    question: str,
    default: bool,
    print_function: typing.Callable[[], None] = print
    ) -> bool:
    """Print a question and return the user answer"""

    if default:
        print_function(f'{question} [Y/n]? ', end='')
    else:
        print_function(f'{question} [y/N]? ', end='')

    answer: str = input().lower()

    match answer:
        case 'y' | 'yes' | 'true':
            return True
        case 'n' | 'no' | 'false':
            return False
        case '':
            return default
        case _:
            error('Invalid answer')
            return ask(question, default, print_function)
