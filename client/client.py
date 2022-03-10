import uuid
import os
import hashlib
from colorama import Fore, init, Style
init()

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
FILES = os.listdir(CURRENT_PATH+"/files")
alg_cript = input("Algoritmo criptográfico a usar (SHA-256 (default), SHA-512, SHA3-256, SHA3-512): ")

def token():
  token=str(uuid.uuid4()).replace("-","")+str(uuid.uuid4()).replace("-","")
  if(alg_cript=="SHA-512" or alg_cript=="SHA3-512"):
    token=str(uuid.uuid4()).replace("-","")+str(uuid.uuid4()).replace("-","")+str(uuid.uuid4()).replace("-","")+str(uuid.uuid4()).replace("-","")
  return token

def digest(path,alg):
    BLOCK_SIZE = 65536 
    file_hash = hashlib.sha256()
    if alg=="SHA-512":
        file_hash = hashlib.sha512()
    elif alg=="SHA3-256":
        file_hash = hashlib.sha3_256()
    elif alg=="SHA3-512":
        file_hash = hashlib.sha3_512()
    with open(CURRENT_PATH+"/files/"+path, 'rb') as f: 
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
        hash = digest(file,alg_cript)
        filename= file
        tokenization=token()
        mac=challenge(hash,tokenization)

        with open(CURRENT_PATH + '/../communication.txt', 'w') as f:
          f.write("-- CLIENT -- \n")
          f.write("FILE: "+filename+'\n')
          f.write("HASH: "+hash+'\n')
          f.write("TOKEN: "+ tokenization+'\n')
        f.close()
        mac_server=""
        hash_server=""
        error=""
        while True:
          with open(CURRENT_PATH + '/../communication.txt', 'r') as f:
            for linea in f:
              if "-- SERVER --" in linea:
                for linea in f:
                  try:
                    if linea.startswith("VERIFICATION FAILED"):
                      error=linea
                    if linea.startswith("HASH_FROM_SERVER:"):
                      hash_server=linea.split(":")[1].strip()
                    if linea.startswith("MAC_FROM_SERVER:"):
                      mac_server=linea.split(":")[1].strip()
                  except:
                    print("Something went wrong ...")
          if(hash_server!=""):
            break
          f.close()
        if(mac_server==mac and error==""):
          print(Style.RESET_ALL + filename + " →" , Fore.GREEN + "INTEGRITY OK")
        else:
          print(Style.RESET_ALL + filename+" →" , Fore.RED + "INTEGRITY FAIL")