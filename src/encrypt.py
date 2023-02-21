from os.path import join, isfile, isdir
from os import remove, rename, environ, listdir, mkdir
from cryptography.fernet import Fernet
import uuid

INPUT_DIR = "input"
OUTPUT_DIR = "output"
AUDIO_FILE_EX = (".mp3", ".wav", ".ogg")

# Get filelist
files = [file for file in listdir(INPUT_DIR) if file.endswith(AUDIO_FILE_EX)]

# Get encryption key from environment variable and encode it
try:
    env_key = environ["en_key"].encode("utf-8")
except KeyError:
    print("en_key doesn't exist in your environment.")
    
key = Fernet(env_key)

def encrypt():
    """
    Encrypt all file within input directory.
    """
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