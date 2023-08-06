#!/usr/bin/env python3
"""
Put a set of ZeroC/ICE slice files (.ice) into python distribution package.
"""

from __future__ import annotations

import sys
from typing import Any, Optional, cast

import configargparse  # pyright: ignore[reportMissingTypeStubs]

from slice_to_py_dist.build_sdist import build_sdist
from slice_to_py_dist.types import DistPackageInfo


def parse_args(argv: list[str]) -> configargparse.Namespace:
    parser = configargparse.ArgumentParser(
        description=__doc__,
        epilog=None,
        formatter_class=configargparse.RawDescriptionHelpFormatter,
        add_help=False,
        config_file_parser_class=configargparse.TomlConfigParser(["main"]),
    )

    parser.add_argument(
        "--help",
        action="help",
        default=configargparse.SUPPRESS,
        help="Show this help message and exit.",
    )

    parser.add_argument(
        "-c",
        "--config",
        type=str,
        is_config_file=True,
        help="""Config file path.""",
    )

    parser.add_argument(
        "--slice-source-dir",
        required=True,
        type=str,
        help="""Path to the directory which contains input slice files.""",
    )

    parser.add_argument(
        "--dist-name",
        required=True,
        type=str,
        help="""Name of the output python distribution package.""",
    )

    parser.add_argument(
        "--dist-version",
        required=True,
        type=str,
        help="""Version of the output python distribution package.""",
    )

    parser.add_argument(
        "--dist-authors",
        required=True,
        type=str,
        nargs="+",
        help=(
            """Authors name and/or email for the distribution package metadata"""
            """ (e.g. "John Smith" or "John Smith <email@domain.com>" or "email@domain.com")."""
        ),
    )

    parser.add_argument(
        "--dist-summary",
        required=True,
        type=str,
        help="""Summary line for the distribution package metadata.""",
    )

    parser.add_argument(
        "--dist-python",
        required=True,
        type=str,
        help="""Python version that distribution package requires, e.g. ">=3.8".""",
    )

    parser.add_argument(
        "--slice-storage-package",
        required=True,
        type=str,
        help="""The name of the additional import package which will store input slice files.""",
    )

    args: Any = parser.parse_args(argv)  # pyright: ignore[reportUnknownMemberType]
    return cast(configargparse.Namespace, args)


def main(argv: Optional[list[str]] = None) -> int:
    "Main function."

    if argv is None:
        argv = sys.argv[1:]

    args = parse_args(argv)

    dist_info = DistPackageInfo(
        name=args.dist_name,
        version=args.dist_version,
        authors=args.dist_authors,
        summary=args.dist_summary,
        requires_python=args.dist_python,
    )

    build_sdist(
        slice_source_dir=args.slice_source_dir, slice_storage_package=args.slice_storage_package, dist_info=dist_info
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
