import hashlib
import os
from datetime import datetime

# Global variables
FILES = os.listdir('./files')
global DICC_HASH
DICC_HASH = dict()

def get_name(file):
    return os.path.splitext(file)[0]


def get_extension(file):
    return os.path.splitext(file)[1]


def saveFiles():
    for file in FILES:
        file_path = './files/' + file
        extension = get_extension(file)
        name = get_name(file)
        if not DICC_HASH.get(extension):
            DICC_HASH[extension] = {name: digest(file_path)}
        else:
            DICC_HASH[extension][name] = digest(file_path)
    return DICC_HASH


def check_digest(file, dicc):
    file_path = './files/' + file
    extension = get_extension(file)
    name = get_name(file)
    actual_hexdigest = digest(file_path)
    original_hexdigest = dicc[extension][name]
    if actual_hexdigest != original_hexdigest:
        dateTimeObj = datetime.now()
        timestamp = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S)")
        return [timestamp, name+extension, actual_hexdigest]
    return []


def write_log(check_data):
    try:
        with open('changes.log', 'r+') as f:
            line_found = any(check_data[1] + ', ' + check_data[2] + '\n' in line for line in f)
            if not line_found:
                f.seek(0, os.SEEK_END)
                f.write(check_data[0] + ', ' + check_data[1] + ', ' + check_data[2] + '\n')
    except:
        with open('changes.log', 'a') as f:
            f.write(check_data[0] + ', ' + check_data[1] + ', ' + check_data[2] + '\n')

def digest(path):
    BLOCK_SIZE = 65536 
    file_hash = hashlib.sha256()
    with open(path, 'rb') as f: 
        fb = f.read(BLOCK_SIZE) 
        while len(fb) > 0: 
            file_hash.update(fb) 
            fb = f.read(BLOCK_SIZE)
    return file_hash.hexdigest()


def create_table_html(headers,report, data):
    pre_existing_template="<!DOCTYPE html>" + "<html>" + "<head>" + "<style>"
    pre_existing_template+="table, th, td {border: 1px solid black;border-collapse: collapse;border-spacing:8px}"
    pre_existing_template+="</style>" + "</head>"
    pre_existing_template+="<body>" + "<strong>" + "REPORT DATE: " + report + "</strong>" 
    pre_existing_template+="<table style='width:50%'>"
    pre_existing_template+='<tr>'
    for header_name in headers:
        pre_existing_template+="<th style='background-color:#3DBBDB;width:85;color:white'>" + header_name + "</th>"
    pre_existing_template+="</tr>"
    for d in data:
        sub_template="<tr style='text-align:center'>"
        sub_template+="<td>" + str(d[0]) + "</td>"
        sub_template+="<td>" + str(d[1]) + "</td>"
        sub_template+="<td>" + str(d[2]) + "</td>"
        sub_template+="<tr/>"
        pre_existing_template+=sub_template
    pre_existing_template+="</table>" + "</body>" + "</html>"
    return(pre_existing_template)


#TODO ORDENAR CLAVES DEL DICCIONARIO PARA POSTERIORMENTE REALIZAR EL DIVIDE Y VENCERAS