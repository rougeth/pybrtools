from pathlib import Path

import click

from .models.talk import read_from_csv
from .video.step_download import step_download


@click.group()
def cli():
    ...


@cli.command(name="video:pipeline-download")
@click.option(
    "-s",
    "--status",
    default=Path("/tmp/pybrtools-pipeline-download"),
    type=click.Path(dir_okay=False, path_type=Path),
    help="File to store list of downloaded talks",
)
@click.option(
    "-b",
    "--bucket",
    required=True,
)
@click.option(
    "-o",
    "--output",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    required=True,
)
@click.argument(
    "csv-database",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    required=True,
)
def video_step_download(csv_database: Path, output: Path, bucket: str, status: Path):
    talks, _ = read_from_csv(csv_database)
    step_download(talks, status, output, bucket)
