import shutil
from pathlib import Path


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
