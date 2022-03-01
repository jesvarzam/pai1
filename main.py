from save_files import DICC_HASH
from save_files import saveFiles
import hashlib
import os

global dicc
dicc=saveFiles(DICC_HASH)
FILES = os.listdir('./files')

import threading
import time

def timer(temp):
    while True:
        for file in FILES:
            file_path = './files/' + file
            BLOCK_SIZE = 65536 
            file_hash = hashlib.sha256()
            with open(file_path, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    file_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE)
                print(file_hash.hexdigest())       
        time.sleep(temp)  

t = threading.Thread(target=timer(2))
t.start()