from report import *
from save_files import *
import os
import threading

global dicc
dicc=saveFiles()
FILES = os.listdir('./files')


def timer():
    threading.Timer(2, timer).start()
    for file in FILES:
        check_data = check_digest(file, dicc)
        if len(check_data) > 0:
            write_log(check_data)


timer()
populate_html()