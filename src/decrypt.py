from os.path import join, isfile
from os import environ, listdir
from io import BytesIO
from mutagen.id3 import ID3, APIC
from cryptography.fernet import Fernet, InvalidToken

INPUT_DIR = "input"
OUTPUT_DIR = "output"

# Get filelist
files = [file for file in listdir(OUTPUT_DIR) if file.endswith(".enc")]

# Get encryption key from environment variable and encode it
try:
    env_key = environ["en_key"].encode("utf-8")
except KeyError:
    print("en_key doesn't exist in your environment.")
key = Fernet(env_key)


def decrypt(file):
        
    try:    
        audiofile = join(OUTPUT_DIR, file)
        
        with open(audiofile, 'rb') as infile:
            encrypted_data = infile.read()
            
            decrypted_data = key.decrypt(encrypted_data)

            data = BytesIO(decrypted_data)
            
            audio = ID3(data)
            
        return (data, audio)
            
    except InvalidToken:
        print("The key does not match with the key that used when encrypting the file, thus cannot be used.")

        return None

if __name__ == "__main__":
    decrypt()