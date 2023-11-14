from pathlib import Path

import click


@click.group()
def cli():
    ...


@cli.command(name="video:validate-csv")
@click.argument(
    "filename", type=click.Path(exists=True, dir_okay=False, path_type=Path)
)
def video_validate_csv(filename):
    ...
