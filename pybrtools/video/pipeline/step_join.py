from tempfile import TemporaryDirectory

from rich.console import Console
from slugify import slugify

from pybrtools.models.talk import Talk
from pybrtools.video import ffmpeg
from pybrtools.video.pipeline import copy_file

from .config import JoinStageConfig

console = Console()


def talk_filename(talk):
    prefix = f"{talk.date.year}-{talk.date.day}"
    author = slugify(talk.author[:10].strip())
    title = slugify(talk.title[:15].strip())
    return f"{prefix}--{author}--{title}.mp4"


def step_join(talk: Talk, config: JoinStageConfig):
    with TemporaryDirectory() as tmpdirname:
        console.log(f"Temporary directory for process {config.source}: {tmpdirname}")
        source = config.source / talk.source_filename
        file = copy_file(source, tmpdirname)
        output_filename = talk_filename(talk)
        destination = config.output / output_filename
        processed_file = ffmpeg.join(file, config.prefix)
        processed_file.rename(destination)
        source.unlink()
        return destination
