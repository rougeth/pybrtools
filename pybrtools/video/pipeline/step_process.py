import shutil
from pathlib import Path
from time import sleep
from typing import Callable

from rich.console import Console
from rich.status import Status

from pybrtools.models.talk import Talk
from pybrtools.video.pipeline import files_to_process

from .config import VideoProcessingConfig

console = Console()


def find_talk_by_source(talks: list[Talk], source: Path):
    for talk in talks:
        # List of talks is quite small, I don't care point about performance
        # at this particular point
        if talk.source_filename == source.name:
            return talk


def run(display: Status, config: VideoProcessingConfig, talks: list[Talk], step: Callable):
    files = files_to_process(config.source)
    if not files:
        display.update(f"[bold yellow] Waiting for files at {config.source}")
        sleep(1)
        return

    for file in files:
        talk = find_talk_by_source(talks, file)
        if not talk:
            console.log(f"[bold red] Couldn't file Talk for {file}")
            continue

        display.update(f"Processing {file}")
        destination = step(talk, config)
        console.log(f"Talk processing finished at {destination}")


def execute_step(config: VideoProcessingConfig, talks: list[Talk], step: Callable):
    with console.status("[bold blue] Processing videos, step {step}...") as display:
        try:
            while True:
                run(display, config, talks, step)
        except KeyboardInterrupt:
            console.log("Shutting down...")
