import argparse

from .. import __version__, logging
from ..widget import tk_subproj


def setup(subparsers: argparse.Action):
    """
    Sub parser for the ``update`` argument.
    """
    parser = subparsers.add_parser("update", help="update requires in project")
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"subproj {__version__}",
        help="print version and exit",
    )
    parser.add_argument(
        "proj_path",
        type=str,
        default=".",
        help="Project path",
    )
    parser.set_defaults(func=tk_subproj.main)
