import click

from pybrtools.models.talk import read_from_csv

from .pipeline.config import PipelineConfig
from .pipeline.step_cut import step_cut
from .pipeline.step_download import step_download
from .pipeline.step_join import step_join
from .pipeline.step_process import execute_step


@click.group(name="video")
def video_cli():
    ...


@video_cli.command("pipeline:download")
@click.argument("config", type=click.File())
def pipeline_download(config):
    pipeline_config = PipelineConfig.from_toml(config.read())
    if not pipeline_config.stages.download:
        click.secho("Missing configuration for Download Stage", fg="red")
        raise click.exceptions.Exit(2)

    talks, _ = read_from_csv(pipeline_config.data)
    step_download(pipeline_config.stages.download, talks)


@video_cli.command("pipeline:cut")
@click.argument("config", type=click.File())
def pipeline_cut(config):
    pipeline_config = PipelineConfig.from_toml(config.read())
    if not pipeline_config.stages.cut:
        click.secho("Missing configuration for Cut Stage", fg="red")
        raise click.exceptions.Exit(2)

    talks, _ = read_from_csv(pipeline_config.data)
    execute_step(pipeline_config.stages.cut, talks, step_cut)


@video_cli.command("pipeline:join")
@click.argument("config", type=click.File())
def pipeline_join(config):
    pipeline_config = PipelineConfig.from_toml(config.read())
    if not pipeline_config.stages.join:
        click.secho("Missing configuration for Join Stage", fg="red")
        raise click.exceptions.Exit(2)

    talks, _ = read_from_csv(pipeline_config.data)
    execute_step(pipeline_config.stages.join, talks, step_join)
