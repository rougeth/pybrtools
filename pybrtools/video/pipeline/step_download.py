"""
Step - Download

1. Lê planilha de palestras
2. Cria arquivo `downloads` para manter lista de arquivos já baixados
3. Se pasta destino tiver menos que x arquivos, baixa próximo da lista
"""

from pathlib import Path
from time import sleep

import boto3
from botocore.exceptions import ClientError
from rich.console import Console

from pybrtools.models.talk import Talk

from .config import DownloadStageConfig

console = Console()


def update_status(filenames: list[str], status_file: Path):
    with status_file.open(mode="w") as file:
        file.write("\n".join(filenames))


def check_talks_downloaded(status_file: Path) -> list[str]:
    if not status_file.exists():
        return []

    with status_file.open() as status:
        files = status.readlines()
        return [filename.strip() for filename in files]


def should_download_next(output: Path, limit=3) -> bool:
    files = list(output.iterdir())
    return len(files) < limit


def download_talk(talk, bucket, output) -> bool:
    s3 = boto3.client("s3")
    path = output / talk.source_filename
    try:
        s3.download_file(bucket, talk.source_filename, path)
        return True
    except ClientError as e:
        error = e.response["Error"]["Message"]
        console.log(
            f"Failed to download file. bucket={bucket!r}, file={talk.source_filename!r}, error={error!r}"
        )
        try:
            path.unlink()
        except FileNotFoundError:
            pass
        return False


def step_download(config: DownloadStageConfig, talks: list[Talk]):
    if not config.output.exists():
        config.output.mkdir()

    talks_downloaded = check_talks_downloaded(config.tracking_file)
    if talks_downloaded:
        console.log(f"{len(talks_downloaded)} talks already downloaded")

    with console.status("[bold blue] Downloading talks") as log:
        while talks:
            log.update("[bold yellow] Waiting next steps")
            while not should_download_next(config.output):
                sleep(1)

            next_talk = talks.pop()
            if next_talk.source_filename in talks_downloaded:
                continue

            log.update(f"[bold blue] Downloading: {next_talk.source_filename}")
            if download_talk(next_talk, config.bucket, config.output):
                talks_downloaded.append(next_talk.source_filename)
                update_status(talks_downloaded, config.tracking_file)
                console.log(
                    f"File downloaded: {config.output / next_talk.source_filename}"
                )
