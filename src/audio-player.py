from rich.progress import Progress, BarColumn, TimeRemainingColumn
from rich.traceback import install
import os
import playsound

install()

AUDIO_COVER_ART = "APIC:cover"
AUDIO_TITLE = "TIT2"
AUDIO_ARTIST = "TPE1"

class AudioFile:
    def __init__(self, path, ):
        self.path = path
        self.filename = os.path.basename(path)
    
    def __repr__(self) -> str:
        return self.filename

def play_audio(file_path):
    
    length = playsound.playsound(file_path, True) // 1000
    
    with Progress("[progress.description]{task.description}", BarColumn(), "{task.completed}/{task.total}", TimeRemainingColumn()) as progress:
        task = progress.add_task("Playing audio...", total=length)
        playsound.playsound(file_path, False)
        for i in range(length):
            progress.update(task, advance=1)

if __name__ == "__main__":
    file_path = r"..\input\NewJeans - OMG.wav"
    play_audio(file_path)