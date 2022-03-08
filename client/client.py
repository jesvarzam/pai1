import uuid
import os
import hashlib
from colorama import Fore, init, Style
init()
token=str(uuid.uuid4()).replace("-","")+str(uuid.uuid4()).replace("-","")
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
        with open('../communication.txt', 'w') as f:
          f.write("-- CLIENT -- \n")
          f.write("FILE: "+filename+'\n')
          f.write("HASH: "+hash+'\n')
          f.write("TOKEN: "+ token+'\n')
        f.close()
        mac_server=""
        hash_server=""
        while True:
          with open('../communication.txt', 'r') as f:
            for linea in f:
              if "-- SERVER --" in linea:
                for linea in f:
                  try:
                    if linea.startswith("HASHS:"):
                      hash_server=linea.split(": ")[1]
                      print(hash_server)
                    if linea.startswith("MACS:"):
                      mac_server=linea.split(": ")[1]
                      print(mac_server)
                  except:
                    print("Something went wrong ...")
          if(mac_server!=""):
            break
          f.close()
        if(mac_server==mac):
          print(Style.RESET_ALL + filename + " →" , Fore.GREEN + "INTEGRITY OK")
        else:
          print(Style.RESET_ALL + filename+" →" , Fore.RED + "INTEGRITY FAIL")
                