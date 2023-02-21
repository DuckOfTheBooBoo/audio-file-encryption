from rich.progress import Progress, BarColumn, TimeRemainingColumn
from rich.traceback import install
import os, blessed
import playsound

install()

INPUT_DIR = os.path.join("..", "input")
OUTPUT_DIR = os.path.join("..", "output")
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

def blessed_file_selector(directory):
    term = blessed.Terminal()
    with term.fullscreen(), term.cbreak():
        current_selection = 0
        files = [f for f in os.listdir(directory) if f.endswith(".enc")]
        max_selection = len(files) - 1
        
        while True:
            print(term.clear())
            print(term.center("Select a file:"))
            
            for i, f in enumerate(files):
                if i == current_selection:
                    print(term.center(f" > {f} < "))
                else:
                    print(term.center(f"   {f}   "))
                    
            key = term.inkey()
            
            if key.is_sequence:
                if key.name == "KEY_UP":
                    current_selection = max(current_selection - 1, 0)
                    
                elif key.name == "KEY_DOWN":
                    current_selection = min(current_selection + 1, max_selection)
                    
                elif key.name == "KEY_ENTER":
                    return os.path.join(directory, files[current_selection])
                
            elif key == "q":
                return None

def select_file():
    # files = [file for file in os.listdir(INPUT_DIR) if file.endswith(".enc")]
    file_path = blessed_file_selector(OUTPUT_DIR)
    
    if file_path is not None:
        print("Selected file:", file_path)
        
    else:
        print("No file selected.")

    
    
    

if __name__ == "__main__":
    select_file()