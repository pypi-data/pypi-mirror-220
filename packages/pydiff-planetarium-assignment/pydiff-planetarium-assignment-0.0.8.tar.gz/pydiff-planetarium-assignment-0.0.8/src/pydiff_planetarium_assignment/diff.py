from typing import List
import difflib


def built_in_diff(old_list: List[str], new_list: List[str]) -> str:
    '''Implement diff with difflib

    Args:
        old (str): Original old string
        new (str): New string

    Returns:
        str: unixdiff-like output
    '''
    delta = difflib.unified_diff(old_list, new_list)
    return delta


def new_diff(old_list: List[str], new_list: List[str]) -> str:
    '''Implement diff with simple idea

    Args:
        old_list (str): Original old string
        new_list (str): New string

    Returns:
        str: unixdiff-like output
    '''
    # TODO: Use another well-known algorithm if necessary
    matrix = [[0] * (len(new_list) + 1) for _ in range(len(old_list) + 1)]

    for i in range(len(old_list) + 1):
        matrix[i][0] = i

    for j in range(len(new_list) + 1):
        matrix[0][j] = j

    for i in range(1, len(old_list) + 1):
        for j in range(1, len(new_list) + 1):
            if old_list[i - 1] == new_list[j - 1]:
                matrix[i][j] = matrix[i - 1][j - 1]
            else:
                matrix[i][j] = 1 + min(
                    matrix[i - 1][j],
                    matrix[i][j - 1],
                    matrix[i - 1][j - 1],
                )

    i, j = len(old_list), len(new_list)
    edits = []

    while i > 0 or j > 0:
        if i > 0 and j > 0 and old_list[i - 1] == new_list[j - 1]:
            edits.append(old_list[i - 1])
            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or matrix[i][j - 1] < matrix[i - 1][j]):
            edits.append(f'+{new_list[j - 1]}')
            j -= 1
        else:
            edits.append(f'-{old_list[i - 1]}')
            i -= 1

    return list(reversed(edits))
