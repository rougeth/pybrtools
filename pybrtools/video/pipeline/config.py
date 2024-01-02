import tomllib
from pathlib import Path
from typing import Optional, Self

from pydantic import BaseModel


class VideoProcessingConfig(BaseModel):
    source: Path
    output: Path


class DownloadStageConfig(BaseModel):
    source: str
    bucket: str
    output: Path
    tracking_file: Path


class CutStageConfig(VideoProcessingConfig):
    ...


class JoinStageConfig(VideoProcessingConfig):
    prefix: Path


class StagesConfig(BaseModel):
    download: Optional[DownloadStageConfig] = None
    cut: Optional[CutStageConfig] = None
    join: Optional[JoinStageConfig] = None


class PipelineConfig(BaseModel):
    data: Path
    stages: StagesConfig

    @classmethod
    def from_toml(cls, config: str) -> Self:
        parsed_config = tomllib.loads(config)
        return cls.model_validate(parsed_config)
