import click

from .video.commands import video_cli


@click.group()
def cli():
    ...


cli.add_command(video_cli)
