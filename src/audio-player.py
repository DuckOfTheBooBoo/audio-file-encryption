from rich.progress import Progress, BarColumn, TimeRemainingColumn
from rich.traceback import install
from os.path import join, basename
from decrypt import decrypt
import os,blessed 

# Remove pygame welcome message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

# Install rich.traceback
install()


INPUT_DIR = join("..", "input")
OUTPUT_DIR = join("..", "output")
AUDIO_COVER_ART = "APIC:cover"
AUDIO_TITLE = "TIT2"
AUDIO_ARTIST = "TPE1"


class AudioFile:
    def __init__(self, path, ):
        self.path = path
        self.filename = basename(path)
    
    def __repr__(self) -> str:
        return self.filename

def play_audio(file_path):
    # TODO: Use mutagen to know the length of audio
    # length = playsound.playsound(file_path, True) // 1000
    
    pygame.mixer.init()
    
    audio = pygame.mixer.Sound(file_path)
    audio.set_volume(1.0)
    audio_stream = audio.play()
    
    while audio_stream.get_busy():
        pygame.time.wait(100)        
    
    
    # with Progress("[progress.description]{task.description}", BarColumn(), "{task.completed}/{task.total}", TimeRemainingColumn()) as progress:
    #     task = progress.add_task("Playing audio...", total=length)
        
        
        
    #     for i in range(length):
    #         progress.update(task, advance=1)

def blessed_file_selector(directory):
    files = [f for f in os.listdir(directory) if f.endswith(".enc")]
    term = blessed.Terminal()
    
    with term.fullscreen(), term.cbreak():
        current_selection = 0
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
                    return join(directory, files[current_selection])
                
            elif key == "q":
                return None

def select_file():
    # files = [file for file in os.listdir(INPUT_DIR) if file.endswith(".enc")]
    file_path = blessed_file_selector(OUTPUT_DIR)
    
    if file_path is not None:
        print("Selected file:", os.path.basename(file_path))
        
        decrypted_data = decrypt(file_path)
        play_audio(decrypted_data[0])
        
    else:
        print("No file selected.")

if __name__ == "__main__":
    select_file()