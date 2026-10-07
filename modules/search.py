"""
That module contains function that find substrings in string by
Boyer-Moore-Horspool method
"""
from typing import Optional, Union

from modules.logtime import log_time #pylint: disable=E0401


def _fill_table(string: str) -> tuple:
    """
    That function create table of offset for substring
    """
    table_search = []
    skip_elements = []
    string_last_idx = len(string) - 1

    table_search.append(['**', string_last_idx + 1])
    table_search.append([string[string_last_idx], string_last_idx + 1])

    for idx in range(string_last_idx, -1, -1):
        element = string[idx]
        if idx == string_last_idx or element in skip_elements:
            continue

        if string[string_last_idx] == string[idx]:
            table_search[1] = [element, string_last_idx - idx]
            skip_elements.append(element)
            continue

        table_search.append([element, string_last_idx - idx])
        skip_elements.append(element)

    return tuple(table_search)

def _find_element(string: str, sub_string: str, case_sensitivity: bool) -> tuple[int, ...]:
    """
    that function find substring in string with use table of offset
    """
    if string == "" or sub_string == "":
        return tuple("")

    if not case_sensitivity:
        string = string.lower()
        sub_string = sub_string.lower()

    located_elements = []
    table = _fill_table(sub_string)

    word_len = table[0][1] - 1
    idx = 0

    while idx + word_len < len(string):
        sub_idx = word_len

        while sub_idx >= 0 and string[idx + sub_idx] == sub_string[sub_idx]:
            sub_idx -= 1

        if sub_idx < 0:
            located_elements.append(idx)
            idx += 1

        else:
            idx += min(el[1] if el[0] == string[idx + word_len] else word_len + 1 for el in table)

    return tuple(located_elements)

@log_time
def search(
        string: str, sub_string: Union[str, list[str]],
        case_sensitivity: bool=False,  method: str='first', count: Optional[int]=None
        ) -> Optional[Union[tuple[int, ...], dict[str, tuple[int, ...]]]]:
    """
    Find all occurrences of substrings in a string by BMH algorithm.

    args:
        string: source text.
        sub_string: one substring or list of substrings.
        case_sensitivity: whether to consider case.
        method: 'first' or 'last' order.
        count: max number of occurrences.

    returns:
        Tuple of indices, dict {substring: tuple} or None
    """
    is_only = isinstance(sub_string, str)
    if is_only:
        sub_string = [sub_string]

    per_sub = {s: _find_element(string, s, case_sensitivity) for s in sub_string}

    if all(value == () for value in per_sub.values()):
        return None

    events = []
    for s, positions in per_sub.items():
        for pos in positions:
            events.append((pos, s))

    events.sort()
    if method == 'last':
        events.reverse()
    if count is not None:
        events = events[:count]

    answer = {s: [] for s in sub_string}
    for pos, s in events:
        answer[s].append(pos)

    answer = {s: (tuple(p) if p else None) for s, p in answer.items()}

    return answer[sub_string[0]] if is_only else answer
