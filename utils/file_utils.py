import json
import os
from pathlib import Path
import sys
from unicodedata import name
import yaml
import glob
import os.path


def load_json_file(path):
    file = open(path, encoding='utf-8')
    data = None
    try:
        data = json.load(file)
    except:
        data = None

    return data


def save_json_to_file(path, data):
    file = open(path, encoding='utf-8', mode='w')
    try:
        json.dump(data, file)
    except:
        data = None

def get_files_in_folder(path, file_type=None):
    list_of_files = list()
    path = Path(path)
    for entry in path.iterdir():
        if entry.suffix  == file_type:
            if entry.name.find("$") == -1 and entry.name.find("~") == -1:
                list_of_files.append(entry)

    return list_of_files


def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def file_exists(path):
    return os.path.exists(path)


def delete_file(path):
    os.remove(path)


def load_yaml(path):
    config = None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    except Exception as exception:
        print(exception)
        config = None

    return config


def find_newest_file_in_folder(path, file_type=r'\*txt'):

    folder_path = os.path.abspath(path)
    files = glob.glob(folder_path + file_type)
    max_file = max(files, key=os.path.getctime)

    print(max_file)

    return max_file
