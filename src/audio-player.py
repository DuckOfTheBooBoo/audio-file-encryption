from rich.progress import Progress, BarColumn, TimeRemainingColumn
from rich.traceback import install
from playsound import playsound

install()

def play_audio(file_path):
    
    length = playsound(file_path, True) // 1000
    
    with Progress("[progress.description]{task.description}", BarColumn(), "{task.completed}/{task.total}", TimeRemainingColumn()) as progress:
        task = progress.add_task("Playing audio...", total=length)
        playsound(file_path, False)
        for i in range(length):
            progress.update(task, advance=1)

if __name__ == "__main__":
    file_path = r"input\NewJeans - OMG.wav"
    play_audio(file_path)