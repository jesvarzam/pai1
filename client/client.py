import uuid
import os
import hashlib

token=str(uuid.uuid4()).replace("-","")+str(uuid.uuid4()).replace("-","")
print(token)
FILES = os.listdir('./files')

def digest(path):
    BLOCK_SIZE = 65536 
    file_hash = hashlib.sha256()
    with open("files/"+path, 'rb') as f: 
        fb = f.read(BLOCK_SIZE) 
        while len(fb) > 0: 
            file_hash.update(fb) 
            fb = f.read(BLOCK_SIZE)
    return file_hash.hexdigest()

def rotar_izquierda(cadena, posiciones):
  return cadena[posiciones:] + cadena[:posiciones]

def challenge(hash,token):
        mac = hex(int(hash, 16) + int(token, 16))[2:]
        mac_rot13= rotar_izquierda(mac, 13)
        mac_par=mac_rot13[1::2]
        mac_sim=''.join(reversed(mac_par))
        return mac_sim

for file in FILES:
        hash = digest(file)
        filename= file
        mac=challenge(hash,token)



#pares del token
#impares del hash