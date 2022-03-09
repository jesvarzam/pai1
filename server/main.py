from report import *
from save_files import *
import os
import threading
from time import time
start_time = time()
global dicc
dicc=saveFiles()
elapsed_time = time() - start_time
print("Elapsed time: %.10f seconds." % elapsed_time)
FILES = os.listdir('./files')
def timer():
    threading.Timer(2, timer).start()
    for file in FILES:
        check_data = check_digest(file, dicc)
        if len(check_data) > 0:
            write_log(check_data)


remove_log_content()
timer()
populate_html()