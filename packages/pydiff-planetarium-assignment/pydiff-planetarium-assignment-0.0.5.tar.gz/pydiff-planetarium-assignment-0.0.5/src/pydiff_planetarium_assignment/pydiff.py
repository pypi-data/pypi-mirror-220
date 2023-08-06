#!/usr/bin/env python3
import click
from print import (
    DEFAULT_COLOR,
    GREEN_COLOR,
    RED_COLOR,
    diff_print,
)
from diff import (
    built_in_diff,
    new_diff,
)


@click.command()
@click.option(
    '--old_file',
    prompt='Old file',
    type=str,
    help='Original file.',
)
@click.option(
    '--new_file',
    prompt='New file',
    type=str,
    help='Compare target file.',
)
@click.option(
    '--experimental',
    is_flag=True,
    type=bool,
    help='Use new diff. If not set, default to use python built-in function.',
)
def command(
    old_file: str,
    new_file: str,
    experimental: bool,
) -> None:
    '''Reference Application for pydiff'''
    try:
        old_file_data = ''
        with open(old_file, 'r', encoding='utf-8') as _old_file:
            old_file_data = _old_file.readlines()
        with open(new_file, 'r', encoding='utf-8') as _new_file:
            new_file_data = _new_file.readlines()

        if experimental:
            output = new_diff(old=old_file_data, new=new_file_data)
        else:
            output = built_in_diff(old=old_file_data, new=new_file_data)

        diff_print(output=output)
    except Exception as error:  # pylint: disable=broad-exception-caught
        # TODO: Use specific exceptions
        print(f'Failed to load files: {error}')

    return


if __name__ == '__main__':
    command()  # pylint: disable=no-value-for-parameter
