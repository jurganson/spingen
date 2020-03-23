import os
from functools import reduce 

def get_directory_structure(root_dir):
    dir = {}
    root_dir = root_dir.rstrip(os.sep)
    start = root_dir.rfind(os.sep) + 1
    for path, _, files in os.walk(root_dir):
        folders = path[start:].split(os.sep)
        sub_dir = dict.fromkeys(files)
        parent = reduce(dict.get, folders[:-1], dir)
        parent[folders[-1]] = sub_dir
    return dir
