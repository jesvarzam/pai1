import uuid
import os
import hashlib

token=str(uuid.uuid4()).replace("-","")
print(token)
FILES = os.listdir('./files')

def digest(path):
    BLOCK_SIZE = 65536 
    file_hash = hashlib.sha256()
    with open(path, 'rb') as f: 
        fb = f.read(BLOCK_SIZE) 
        while len(fb) > 0: 
            file_hash.update(fb) 
            fb = f.read(BLOCK_SIZE)
    return file_hash.hexdigest()

for file in FILES:
        check_data = digest(file)