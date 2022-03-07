import importlib
import platform
import sys
from argparse import ArgumentParser
from typing import Iterable, List, Optional, Sequence, Set, Tuple

from . import __version__
from .config import Config
from .linter import Linter
from .problem import ProblemType

IGNORABLE_TYPES = [t.name for t in (ProblemType.URI, ProblemType.FLOAT)]


def main(argv: Optional[Sequence[str]] = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    parser = _make_arg_parser()
    args = parser.parse_args(argv)
    config = Config(args.ignore, args.yaml)

    if config.is_yaml and not _is_pyyaml_installed():
        print("Missing optional dependency 'PyYAML'.", file=sys.stderr)
        return 2

    all_problems = dict(_get_problems(args.filepath_or_text, config))

    if not all_problems:
        return 0

    printing_input = len(args.filepath_or_text) > 1
    for key, problems in all_problems.items():
        if printing_input:
            print(key)

        problems_count = len(problems)
        header = "One error" if problems_count == 1 else f"{problems_count} errors"
        print(f"{header}:")

        for problem in problems:
            print(f" {problem}")

    return 1


def _get_problems(
    input_list: List[str], config: Config
) -> Iterable[Tuple[str, List[str]]]:
    for filepath_or_text in input_list:
        problems = Linter.validate(filepath_or_text, config)
        if problems:
            yield filepath_or_text, problems


def _is_pyyaml_installed() -> bool:
    try:
        importlib.import_module("yaml")
    except ImportError:
        return False
    return True


def _make_arg_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument(
        "filepath_or_text",
        nargs="+",
        help="ASL file path or ASL JSON/YAML text.",
    )

    parser.add_argument(
        "--ignore",
        type=_ignore_types,
        help="Comma-separated list of errors to ignore (or skip)."
        " For example, `--ignore=URI,FLOAT`."
        f" Supported values are {IGNORABLE_TYPES}.",
    )

    parser.add_argument(
        "--yaml",
        action="store_true",
        help="Parse as YAML instead of JSON.",
    )

    parser.add_argument(
        "--version",
        "-V",
        action="version",
        version=f"{__version__} {_get_python_version()}",
    )
    return parser


def _ignore_types(value: str) -> Set[ProblemType]:
    values = set(v.strip() for v in value.split(","))
    if values - set(IGNORABLE_TYPES):
        raise ValueError()
    return set(ProblemType[v] for v in values)


def _get_python_version() -> str:
    return (
        f"{platform.python_implementation()} "
        f"{platform.python_version()} on {platform.system()}"
    )
