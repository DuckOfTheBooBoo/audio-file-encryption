from os.path import join, isfile, isdir
from os import remove, rename, environ, listdir, mkdir
from io import BytesIO
from cryptography.fernet import Fernet
import uuid

INPUT_DIR = "input"
OUTPUT_DIR = "output"
AUDIO_FILE_EX = (".mp3", ".wav", ".ogg")

# Get filelist
files = [file for file in listdir(INPUT_DIR) if file.endswith(AUDIO_FILE_EX)]

# Get encryption key from environment variable and encode it
env_key = environ.get("en_key").encode("utf-8")
key = Fernet(env_key)

def encrypt():
    for file in files:
        
        audiofile = join(INPUT_DIR, file)
        with open(audiofile, 'rb') as infile:
            data = infile.read()
            
        encrypted_data = key.encrypt(data)
        filename = str(uuid.uuid4()) + ".enc"
        
        with open(join(OUTPUT_DIR, filename), 'wb') as outfile:
            print(f"out -> {join(OUTPUT_DIR, filename)}")
            outfile.write(encrypted_data)
            
if __name__ == "__main__":
    encrypt()