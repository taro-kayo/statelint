import importlib
import platform
import sys
from argparse import ArgumentParser
from typing import Optional, Sequence, Set

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

    problems = Linter.validate(args.filepath_or_json_text, config)

    if not problems:
        return 0

    problems_count = len(problems)
    header = "One error" if problems_count == 1 else f"{problems_count} errors"
    print(f"{header}:")

    for problem in problems:
        print(f" {problem}")

    return 1


def _is_pyyaml_installed() -> bool:
    try:
        importlib.import_module("yaml")
    except ImportError:
        return False
    return True


def _make_arg_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument(
        "filepath_or_json_text",
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
