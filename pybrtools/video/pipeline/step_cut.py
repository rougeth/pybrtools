from tempfile import TemporaryDirectory

from rich.console import Console

from pybrtools.models.talk import Talk
from pybrtools.video import ffmpeg
from pybrtools.video.pipeline import copy_file
from pybrtools.video.pipeline.config import CutStageConfig

console = Console()


def step_cut(talk: Talk, config: CutStageConfig):
    with TemporaryDirectory() as tmpdirname:
        console.log(f"Temporary directory for process {config.source}: {tmpdirname}")
        source = config.source / talk.source_filename
        file = copy_file(source, tmpdirname)
        destination = config.output / source.name
        processed_file = ffmpeg.cut(file, talk.source_starttime, talk.source_endtime)
        processed_file.rename(destination)
        source.unlink()
        return destination
