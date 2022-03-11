import os
import time
from save_files import saveFiles, get_name, get_extension
import sys
import signal
import threading
from datetime import datetime

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
communication_path = CURRENT_PATH + '/../communication.txt'
FILES = os.listdir(CURRENT_PATH+"/files")
SERVER_DICC = saveFiles()
tokens=[]

def timer():
    while True:
        time.sleep(5)
        try:
            tokens.remove(tokens[0])
        except:
            pass

def token_utils(token):
    res=False
    if token not in tokens:
        tokens.append(token)
        res=True
    return res

def sig_handler(sig, frame):
	print("\n\n[!] Exiting...\n")
	sys.exit(0)

signal.signal(signal.SIGINT, sig_handler)

def rotar_izquierda(cadena, posiciones):
  return cadena[posiciones:] + cadena[:posiciones]


def challenge(hash,token):
        mac = hex(int(hash, 16) + int(token, 16))[2:]
        mac_rot13= rotar_izquierda(mac, 13)
        mac_par=mac_rot13[1::2]
        mac_sim=''.join(reversed(mac_par))
        return mac_sim

def read_client_data():
    data = {}
    with open(communication_path, 'r') as f:
        for line in f.readlines():
            if 'CLIENT' in line:
                continue
            try:
                data[line.split(":")[0].strip()] = line.split(":")[1].strip()
            except:
                return False
    return data


def check_client_data(data):
    file_name = get_name(data['FILE'])
    file_extension = get_extension(data['FILE'])
    file_hash_from_client = data['HASH']

    if not SERVER_DICC[file_extension]:
        return "File extension not found"
    if not SERVER_DICC[file_extension][file_name]:
        return "File name not found"
    if not file_hash_from_client == SERVER_DICC[file_extension][file_name]:
        return False
    
    return True


def send_info(check, data):
    if check:
        write_txt_ok(data)
    elif not check:
        write_txt_failed_mod(data)
    else:
        write_txt_failed_not_exist()


def write_txt_ok(data):
    token_from_client = data['TOKEN']
    if token_utils(token_from_client):
        file_name = get_name(data['FILE'])
        file_extension = get_extension(data['FILE'])
        file_hash_from_server = SERVER_DICC[file_extension][file_name]

        with open(communication_path, 'a') as f:
            f.write("-- SERVER -- \n")
            f.write("VERIFICATION SUCCESSFUL\n")
            f.write("HASH_FROM_SERVER: "+file_hash_from_server+'\n')
            f.write("MAC_FROM_SERVER: "+ challenge(file_hash_from_server, token_from_client) +'\n')
            f.close()
    else:
        write_txt_failed_replay()

def write_txt_failed_mod(data):
    file_name = get_name(data['FILE'])
    file_extension = get_extension(data['FILE'])
    file_hash_from_server = SERVER_DICC[file_extension][file_name]
    with open(communication_path, 'a') as f:
        f.write("-- SERVER -- \n")
        f.write("VERIFICATION FAILED, FILE HAS BEEN MODIFIED\n")
        f.write("HASH_FROM_SERVER: "+file_hash_from_server+'\n')
        f.close()


def write_txt_failed_not_exist():
    with open(communication_path, 'a') as f:
        f.write("-- SERVER -- \n")
        f.write("VERIFICATION FAILED, FILE DOES NOT EXIST\n")
        f.close()

def write_txt_failed_replay():
    with open('../communication.txt', 'a') as f:
        f.write("-- SERVER -- \n")
        f.write("VERIFICATION FAILED, TOKEN ALREADY EXIST\n")
        f.close()


def main():
    if 'CLIENT' and 'TOKEN' in open(communication_path, 'r').read():
        data = read_client_data()
        if not data:
            print("Waiting for connection...", end="\r")
            return False
        print("Connection established with client at {}".format(datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")))
        check = check_client_data(data)
        send_info(check, data)
    else:
        print("Waiting for connection...", end="\r")

t = threading.Thread(target=timer)
t.start()
while True:
    main()