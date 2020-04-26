from collections import defaultdict
import os
import log
from glob import glob
import json
from datetime import datetime
from util import flatten


def prepare_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)


def file_exists(path, file_path):
    return os.path.exists(os.path.join(path, file_path))


def current_timestamp():
    return str(round(datetime.now().timestamp()))


def save(obj, path, file_name=None):
    """
    Saves the given object under the path + filename location. 
    If filename is ommited an unique name will be generated.
    """
    if file_name is None:
        file_name = current_timestamp()
        log.debug("Genereting unique name for file to save: ".format(file_name))

    log.debug("Saving file {}/{}".format(path, file_name))
    prepare_directory(path)
    with open(os.path.join(path, file_name), "w") as f:
        json.dump(obj, f, indent=2)


def load_raw(path, file_name=None, transform=lambda x: x):
    """
    Reads the given file into a list of strings optionally applying transform to each line.
    Returns an array of strings/or results from transform.
    """
    process_file = lambda f: [transform(line) for line in f]
    return load_bulk(path, file_name, process_file)


def load_bulk(path, file_name=None, transform=lambda x: json.load(x)):
    """
    Loads all the the files in given path or just one file if file_name is not ommited and 
    then packs each object found into one array.

    Treats all files as json by default, provide the transform method to change this.

    When transform is given it will be applied on each file before appending to resulting array.
    """
    if file_name is None:
        files = [f for f in glob(os.path.join(*path.split("/"), "*"))]
    else:
        files = [os.path.join(path, file_name)]

    log.debug("Will load {} files: {}".format(len(files), files))
    result = []
    for f in files:
        with open(f) as current:
            result.append(transform(current))
    return result


def load_arrays(path, file_name=None, transform=lambda x: x):
    """
    Load all the files in path or just one file if file_name is given and then flatten all of 
    the arrays found into one resulting array. Applies transform method at the end to each entry.
    """
    return list(map(transform, flatten(load_bulk(path, file_name))))


def load(path, file_name):
    """
    Loads one file in the given path + file_name.
    You can also provide full path to file instead.
    """
    return load_bulk(path, file_name)[0]
