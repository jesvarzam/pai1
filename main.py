from save_files import *
import os
import threading
import time

global dicc
dicc=saveFiles()
FILES = os.listdir('./files')


def timer(temp):
    while True:
        for file in FILES:
            check_data = check_digest(file, dicc)
            if len(check_data) > 0:
                write_log(check_data)
        time.sleep(temp)  

t = threading.Thread(target=timer(2))
t.start()