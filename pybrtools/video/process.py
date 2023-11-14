from pathlib import Path

import boto3

from pybrtools.models.talk import Talk


def download_from_s3(talk: Talk, dir: Path, bucket: str) -> Path:
    s3 = boto3.client("s3")
    path = dir / talk.source_filename
    with path.open(mode="wb") as file:
        s3.download_fileobj(bucket, talk.source_filename, file)
    return path


def upload_to_s3(talk: Talk, dir: Path, bucket: str) -> Talk:
    s3 = boto3.client("s3")
    path = dir / talk.filename
    with path.open(mode="rb") as file:
        s3.upload_fileobj(file, bucket, talk.filename)


def process_video(
    talk: Talk, input: Path, output: Path, prefix: Path, suffix: Path
) -> Talk:
    ...
