"""CLI interface for video_tools project.

Be creative! do whatever you want!

- Install click or typer and create a CLI app
- Use builtin argparse
- Start a web application
- Import things from your .base module
"""
import argparse
import logging
from pathlib import Path

from tqdm.contrib.logging import logging_redirect_tqdm

from video_tools.aggregate import Aggregator


def main():
    parser = argparse.ArgumentParser(
        description="CLI interface for ai4vl video_tools.",
    )
    parser.add_argument("--verbose", "-v", action="count", default=0, help="Verbose output")

    subparsers = parser.add_subparsers(help="Subcommand help", required=True, dest="subcommand")

    aggregate_parser = subparsers.add_parser("aggregate", help="Aggregate case videos")
    aggregate_parser.add_argument(
        "--input-folder",
        "-i",
        required=True,
        type=Path,
        help="where to find the study folders containing input videos",
    )
    aggregate_parser.add_argument(
        "--output-folder",
        "-o",
        required=True,
        type=Path,
        help="where to store the output videos",
    )
    aggregate_parser.add_argument(
        "--input-extension", default=".mp4", help="Input extension (e.g. .mp4)"
    )
    aggregate_parser.add_argument(
        "--output-extension",
        default=".mp4",
        help="Output extension (e.g. .mp4)",
    )
    aggregate_parser.add_argument(
        "--seperator-frames",
        "-s",
        default=30,
        type=int,
        help="Number of frames to insert between snippets",
    )
    aggregate_parser.add_argument(
        "--dry-run",
        "-d",
        action="store_true",
        help="Dry run (do not run ffmpeg nor generate output)",
    )
    aggregate_parser.add_argument(
        "--overwrite",
        "-y",
        action="store_true",
        help="Overwrite existing output files. By default, existing files are skipped.",
    )

    args = parser.parse_args()
    logging.basicConfig(
        level={
            0: logging.WARNING,
            1: logging.INFO,
            2: logging.DEBUG,
        }[args.verbose]
    )

    with logging_redirect_tqdm():
        if args.subcommand == "aggregate":
            cli_aggregate(args)


def cli_aggregate(args):
    aggregator = Aggregator(
        input_folder=args.input_folder,
        output_folder=args.output_folder,
        input_extension=args.input_extension,
        output_extension=args.output_extension,
        seperator_frames=args.seperator_frames,
        dry_run=args.dry_run,
        overwrite=args.overwrite,
    )
    aggregator.run()
