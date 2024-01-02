import subprocess
from datetime import timedelta
from pathlib import Path


def cut(source: Path, start: int, end: int) -> Path:
    # ffmpeg -ss 00:01:00 -to 00:02:00 -i input.mp4 -c copy output.mp4
    start = str(timedelta(seconds=start))
    end = str(timedelta(seconds=end))
    output = source.parent / "output.mp4"
    command = (
        "ffmpeg -hide_banner -loglevel error "
        f"-ss {start} -to {end} -i {source} -c copy {output}"
    )
    try:
        subprocess.run(command, shell=True)
        return output
    except subprocess.CalledProcessError:
        return None


def join(source: Path, prefix: Path) -> Path:
    # ffmpeg -i input1.mp4 -i input2.mp4 -filter_complex "[0:v] [0:a] [1:v] [1:a] concat=n=2:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" output.mp4
    command_template = (
        "ffmpeg -hide_banner -loglevel error -i {intro} -i {talk} "
        '-filter_complex "[0:v] [0:a] [1:v] [1:a] concat=n=2:v=1:a=1 [v] [a]" '
        '-map "[v]" -map "[a]" {output}'
    )
    output = source.parent / "output.mp4"

    command = command_template.format(
        intro=prefix,
        talk=source,
        output=output,
    )

    try:
        subprocess.run(command, shell=True)
        return output
    except subprocess.CalledProcessError:
        return None
