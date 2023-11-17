import subprocess
from pathlib import Path
from datetime import timedelta


def cut(source: Path, start: int, end: int):
    # ffmpeg -ss 00:01:00 -to 00:02:00 -i input.mp4 -c copy output.mp4
    start = str(timedelta(seconds=start))
    end = str(timedelta(seconds=end))
    output = source.parent / "output.mp4"
    command = f"ffmpeg -ss {start} -to {end} -i {source} -c copy {output}"
    try:
        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL)
        return output
    except subprocess.CalledProcessError:
        return None
