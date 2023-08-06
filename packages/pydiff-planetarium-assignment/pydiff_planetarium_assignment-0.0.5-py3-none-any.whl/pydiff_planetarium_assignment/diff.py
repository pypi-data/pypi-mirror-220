import difflib


def built_in_diff(old: str, new: str) -> str:
    '''Implement diff with difflib

    Args:
        old (str): Original old string
        new (str): New string

    Returns:
        str: unixdiff-like output
    '''
    delta = difflib.unified_diff(old, new)
    return ''.join(delta).split('\n')


def new_diff(old: str, new: str) -> str:
    return ''
