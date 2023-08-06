from importlib.metadata import version
from pathlib import Path

from .. import hookimpl


@hookimpl(tryfirst=True)
def cantaloupe_addoption(parser) -> None:
    """
    Called to add arguments to the parser.

    :param parser: the parser to add arguments to
    :type parser: argparse.ArgumentParser
    :return:
    :rtype:
    """

    parser.add_argument(
        "-w",
        "--workflows",
        type=lambda p: Path(p).absolute(),
        help="Path to the workflows directory.",
        required=True,
    )
    parser.add_argument(
        "-c",
        "--context",
        type=lambda p: Path(p).absolute(),
        help="Path to an alternate context file.",
        required=False,
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s {}".format(version("cantaloupe")),
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode.",
        required=False,
    )
    parser.add_argument(
        "-ff",
        "--failfast",
        action="store_true",
        help="Stop on first failure.",
        required=False,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry run mode.",
        required=False,
    )
