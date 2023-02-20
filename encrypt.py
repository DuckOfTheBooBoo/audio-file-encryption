from os.path import join, isfile
from os import remove, rename, environ, listdir
from io import BytesIO

INPUT_DIR = "input"
OUTPUT_DIR = "output"
AUDIO_FILE_EX = (".mp3", ".wav", ".ogg")

# Get filelist
files = [file for file in listdir(INPUT_DIR) if isfile(file) and file.endswith(AUDIO_FILE_EX)]

# Get encryption key from environment variable
en_key = environ.get("en_key")

def encrypt():
    pass    

if __name__ == "__main__":
    encrypt()