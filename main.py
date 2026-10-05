"""
Entery point in program
"""
import argparse
import sys
from pathlib import Path

from modules.search import search

COLORS = {
    "red": "\033[31m",
    "green": "\033[32m",
    "blue": "\033[34m",
}
COLOR_VALUES = tuple(COLORS.values())

RESET = "\033[0m"


def parse_arg():
    """
    That func parse arguments from call
    """
    parser = argparse.ArgumentParser(
        prog="search",
        description=("Searching for substrings in a string or "
        "file using the Boyer-Moore-Horspool algorithm"),
    )

    source = parser.add_mutually_exclusive_group(required=True)

    source.add_argument("-s", "--string", type=str, help="String")
    source.add_argument("-f", "--file", type=str, help="Filepath")

    parser.add_argument(
        "-p", "--substring", nargs="+", required=True,
        help="Substring or any substrings"
    )
    parser.add_argument(
        "-c", "--case_sensitivity", action="store_false",
        help="Find with case-sensitivity"
    )
    parser.add_argument(
        "-m", "--method", choices=["first", "last"],
        default="first",
        help="search order: first - from the beginning, last - from the end",
    )
    parser.add_argument(
        "-k", "--count", type=int,
        default=None,
        help="how many occurrences to find (all by default)",
    )
    parser.add_argument(
        "--color", action="store_true", help="enable color selection"
    )
    parser.add_argument(
        "--max_lines", type=int, help="Maximum number of rows",
        default=10
    )

    return parser.parse_args()

def colorize(text: str, nums: dict, substrings: list[str]) -> str:
    """Returns text with highlighted occurrences of substrings"""
    marks = [None] * len(text)

    for i, sub in enumerate(substrings):
        positions = nums.get(sub)
        if not positions:
            continue
        color = COLOR_VALUES[i % len(COLOR_VALUES)]
        for pos in positions:
            for j in range(pos, min(pos + len(sub), len(text))):
                marks[j] = color

    parts = []
    current = None
    for ch, mark in zip(text, marks):
        if mark != current:
            if current is not None:
                parts.append(RESET)
            if mark is not None:
                parts.append(mark)
            current = mark
        parts.append(ch)
    if current is not None:
        parts.append(RESET)

    return "".join(parts)

def limit_lines(text: str, max_lines: int = 10) -> str:
    """Limits the output of max_lines to lines"""
    lines = text.splitlines()

    if len(lines) <= max_lines:
        return text

    return "\n".join(lines[:max_lines]) + f"\n... (showed {max_lines} of {len(lines)})"

def run():
    """
    Entry point of program
    """
    args = parse_arg()

    if args.file:
        path = Path(args.file)

        if not path.exists():
            print("File not found")
            sys.exit(1)

        if not path.is_file():
            print("Can't read file")
            sys.exit(1)

        text = path.read_text("utf-8")

    else:
        text = args.string

    answer = search(
        text, args.substring, args.case_sensitivity,
        args.method, args.count
    )

    if answer is None:
        print("Occurrences not found")
        return False

    use_color = args.color

    if isinstance(answer, tuple):
        answer = {args.substring[0]: answer}

    print(limit_lines(str(answer), args.max_lines))

    if use_color:
        answer = colorize(text, answer, args.substring)
        print(limit_lines(answer, args.max_lines))

    return True


if __name__ == "__main__":
    run()
