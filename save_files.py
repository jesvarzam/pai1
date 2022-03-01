import hashlib
import os
import operator

# Global variables
FILES = os.listdir('./files')
global DICC_HASH
DICC_HASH = dict()

def get_name(file):
    return os.path.splitext(file)[0]


def get_extension(file):
    return os.path.splitext(file)[1]


def saveFiles(dict):
    for file in FILES:
        file_path = './files/' + file
        extension = get_extension(file)
        name = get_name(file)
        if not DICC_HASH.get(extension):
            DICC_HASH[extension] = {name: digest(file_path)}
        else:
            DICC_HASH[extension][name] = digest(file_path)
    return DICC_HASH

def digest(path):
    BLOCK_SIZE = 65536 
    file_hash = hashlib.sha256()
    with open(path, 'rb') as f: 
        fb = f.read(BLOCK_SIZE) 
        while len(fb) > 0: 
            file_hash.update(fb) 
            fb = f.read(BLOCK_SIZE)
    return file_hash.hexdigest()


#TODO ORDENAR CLAVES DEL DICCIONARIO PARA POSTERIORMENTE REALIZAR EL DIVIDE Y VENCERAS