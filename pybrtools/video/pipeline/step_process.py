import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
from time import sleep
from typing import Callable

from rich.console import Console

from pybrtools.models.talk import Talk
from .. import ffmpeg
from .config import VideoProcessingConfig, CutStageConfig, JoinStageConfig


console = Console()


def files_to_process(source: Path):
    if not source.exists():
        source.mkdir()
    files = source.iterdir()
    return [file for file in files if file.name.endswith(".mp4")]


def copy_file(source: Path, tmpdirname: str) -> Path:
    tmp = Path(tmpdirname)
    destination = tmp / source.name
    shutil.copy(source, destination)
    return destination


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


def find_talk_by_source(talks: list[Talk], source: Path):
    for talk in talks:
        # List of talks is quite small, I don't care point about performance
        # at this particular point
        if talk.source_filename == source.name:
            return talk


def execute_step(config: VideoProcessingConfig, talks: list[Talk], step: Callable):
    with console.status("[bold blue] Processing videos, step {step}...") as display:
        while not (files := files_to_process(config.source)):
            display.update(f"[bold yellow] Waiting for files at {config.source}")
            sleep(1)

        for file in files:
            talk = find_talk_by_source(talks, file)
            if not talk:
                console.log(f"[bold red] Couldn't file Talk for {file}")
                continue

            display.update(f"Processing {file}")
            destination = step(talk, config)
            console.log(f"Talk processing finished at {destination}")
