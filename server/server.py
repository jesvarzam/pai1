import os
from save_files import saveFiles, get_name, get_extension
FILES = os.listdir('./files')

SERVER_DICC = saveFiles()

def read_client_data():
    data = []
    with open('../communication.txt', 'r') as f:
        for line in f.readlines():
            if line.startswith("-- CLIENT --"):
                continue
            data.append(line.split(":")[1].strip())
    return data


def check_client_data(data):
    file_name = get_name(data[0])
    file_extension = get_extension(data[0])
    file_hash_from_client = data[1]

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
    file_name = get_name(data[0])
    file_extension = get_extension(data[0])
    file_hash_from_server = SERVER_DICC[file_extension][file_name]

    with open('../communication.txt', 'a') as f:
        f.write("-- SERVER -- \n")
        f.write("VERIFICATION SUCCESSFUL\n")
        f.write("HASH_FROM_SERVER: "+file_hash_from_server+'\n')
        f.write("MAC: "+ "MAC_TEST" +'\n')
        f.close()


def write_txt_failed_mod(data):
    file_name = get_name(data[0])
    file_extension = get_extension(data[0])
    file_hash_from_server = SERVER_DICC[file_extension][file_name]
    with open('../communication.txt', 'a') as f:
        f.write("-- SERVER -- \n")
        f.write("VERIFICATION FAILED, FILE HAS BEEN MODIFIED\n")
        f.write("HASH_FROM_SERVER: "+file_hash_from_server+'\n')
        f.close()


def write_txt_failed_not_exist(check):
    with open('../communication.txt', 'a') as f:
        f.write("-- SERVER -- \n")
        f.write("VERIFICATION FAILED, FILE DOES NOT EXIST\n")
        f.close()

if __name__=='__main__':
    
    data = read_client_data()
    check = check_client_data(data)
    send_info(check, data)

