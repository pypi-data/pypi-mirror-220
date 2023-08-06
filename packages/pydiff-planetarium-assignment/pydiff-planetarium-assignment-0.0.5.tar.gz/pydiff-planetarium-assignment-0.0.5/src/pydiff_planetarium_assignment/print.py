# built-in
from os import system

system('')


def RGB(red=None, green=None, blue=None, bg=False):  # pylint: disable=invalid-name
    '''Colorize stdout text using ANSI Escape Codes

    Args:
        red (int, optional): Red. Defaults to None.
        green (int, optional): Green. Defaults to None.
        blue (int, optional): Blue. Defaults to None.
        bg (bool, optional): Background. Defaults to False.

    Returns:
        str: colorize stdout text with ANSI Escape Codes
    '''
    # TODO: Change into class
    if (not bg and red is not None and green is not None and blue is not None):
        return f'\u001b[38;2;{red};{green};{blue}m'
    elif (bg and red is not None and green is not None and blue is not None):
        return f'\u001b[48;2;{red};{green};{blue}m'
    elif (red is None and green is None and blue is None):
        return '\u001b[0m'


DEFAULT_COLOR = RGB()
RED_COLOR = RGB(255, 0, 0)
GREEN_COLOR = RGB(0, 255, 0)


def diff_print(output: str):
    '''Print diff with colors

    Args:
        output (str): diff text
    '''
    for line in output:
        if line and line[0] == '+':
            print(GREEN_COLOR, end='')
            print(line, end='')
            print(DEFAULT_COLOR)
        elif line and line[0] == '-':
            print(RED_COLOR, end='')
            print(line, end='')
            print(DEFAULT_COLOR)
        else:
            print(line)
    return
