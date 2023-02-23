from rich.progress import Progress, BarColumn, TimeRemainingColumn, TimeElapsedColumn
from rich.traceback import install
from rich.console import Console
from time import sleep
from os.path import join, basename
from decrypt import decrypt
import os,blessed 

# Remove pygame welcome message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

# Install rich.traceback
install()

console = Console()

INPUT_DIR = join("..", "input")
OUTPUT_DIR = join("..", "output")
AUDIO_COVER_ART = "APIC:cover"
AUDIO_TITLE = "TIT2"
AUDIO_ARTIST = "TPE1"

term = blessed.Terminal()

def play_audio(input_stream):
    audio_metadata = input_stream[1]
    
    pygame.mixer.init()
    
    audio = pygame.mixer.Sound(input_stream[0])
    audio.set_volume(1.0)
    audio_stream = audio.play()
    
    length = int(audio.get_length())
    
    song_title = audio_metadata[AUDIO_TITLE]
    song_artist = audio_metadata[AUDIO_ARTIST]
    
    with term.fullscreen():
        
        width = term.width // 2
        height = term.height // 2

        print(term.move_x(width) + term.move_y(height))
        with Progress("[progress.description]{task.description}", f"{song_artist} - {song_title}", BarColumn(), TimeElapsedColumn(), "/", TimeRemainingColumn()) as progress:
            
            task = progress.add_task("Playing", total=length)
            
            while audio_stream.get_busy():
                progress.update(task, advance=1)
                sleep(1)
        
        # TODO: Implement a seeking function
        
        
        

def blessed_file_selector(directory):
    files = [f for f in os.listdir(directory) if f.endswith(".enc")]
    
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
        play_audio(decrypted_data)
        
    else:
        print("No file selected.")

if __name__ == "__main__":
    select_file()