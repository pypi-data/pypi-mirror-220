"""Command line for leaf focus."""
from __future__ import annotations

import argparse
import logging
import pathlib
import sys

from leaf_focus import app, utils


def main(args: list[str] | None = None) -> int:
    """Run as a command line program.

    Args:
        args: The program arguments.

    Returns:
        int: Program exit code.
    """
    if args is None:
        args = sys.argv[1:]

    logging.basicConfig(
        format="%(asctime)s [%(levelname)-8s] %(message)s",
        level=logging.DEBUG,
    )
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(
        prog="leaf-focus",
        description="Extract structured text from a pdf file.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {utils.get_version()}",
    )
    parser.add_argument(
        "input_pdf",
        type=pathlib.Path,
        help="path to the pdf file to read",
    )
    parser.add_argument(
        "output_dir",
        type=pathlib.Path,
        help="path to the directory to save the extracted text files",
    )
    parser.add_argument(
        "--exe-dir",
        required=True,
        type=pathlib.Path,
        help="path to the directory containing xpdf executable files",
    )
    parser.add_argument(
        "--page-images",
        action="store_true",
        help="save each page of the pdf as a separate image",
    )
    parser.add_argument(
        "--ocr",
        action="store_true",
        help="run optical character recognition on each page of the pdf",
    )
    parser.add_argument(
        "--first",
        type=int,
        default=None,
        help="the first pdf page to process",
    )
    parser.add_argument(
        "--last",
        type=int,
        default=None,
        help="the last pdf page to process",
    )
    parser.add_argument(
        "--log-level",
        default="info",
        choices=["debug", "info", "warning", "error", "critical"],
        help="the log level: debug, info, warning, error, critical",
    )

    parsed_args = parser.parse_args(args)

    app_inst = app.App(exe_dir=parsed_args.exe_dir)

    try:
        app_args = app.AppArgs(
            input_pdf=parsed_args.input_pdf,
            output_dir=parsed_args.output_dir,
            first_page=parsed_args.first,
            last_page=parsed_args.last,
            save_page_images=parsed_args.page_images,
            run_ocr=parsed_args.ocr,
            log_level=parsed_args.log_level,
        )

        logging.getLogger().setLevel((app_args.log_level or "info").upper())

        result = app_inst.run(app_args)
        if result is True:
            return 0
        return 1

    except utils.LeafFocusError as error:
        logger.exception("Error: %s", error.__class__.__name__)
        return 1

    except Exception as error:
        logger.exception("Error: %s", error.__class__.__name__)
        return 2


if __name__ == "__main__":
    sys.exit(main())
