from datetime import date
from csv import DictReader
from pathlib import Path

from loguru import logger
from pydantic import BaseModel, ValidationError
from click import File


YOUTUBE_TITLE_MAX_LENGTH = 60


class Talk(BaseModel):
    title: str
    author: str
    description: str
    date: date
    source_filename: str
    # Timestamps in seconds
    source_starttime: int | None
    source_endtime: int | None
    youtube_id: str | None
    youtube_suffix: str | None

    @property
    def youtube_video_title(self):
        title = f"{self.title.strip()} - {self.author.strip()}"
        title += self.youtube_suffix or ""
        return title


def read_from_csv(
    file: Path,
) -> tuple[list[Talk], list]:
    errors = []
    talks = []
    with file.open() as fp:
        reader = DictReader(fp)
        for row in reader:
            data = {field: row.get(field) for field in Talk.__fields__.keys()}

            try:
                talk = Talk(**data)
            except ValidationError as e:
                errors.append((data, e.errors()))
            else:
                talks.append(talk)

    return talks, errors
