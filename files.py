from collections import defaultdict
import os
import log
from glob import glob
import json
from datetime import datetime

level_info_path = "stats"


def create_dict(path):
    """
    Creates a dictonary with word frequency based from all files in path
    """
    d = defaultdict(int)
    log.debug("Starting dictionary processing")
    for file_path in glob(os.path.join(*path.split("/"), "*")):
        with open(file_path) as fp:
            for line in fp:
                line = fp.readline()
                tokens = line.split()
                for t in tokens:
                    d[t] += 1
    log.debug("Done dictonary procesing")
    return d


def lazy_load_dict(dict_path, source_path, mapper=lambda x: x):
    if os.path.exists(dict_path):
        log.debug("Loading precalculated dictionary.")
        with open(dict_path, "r") as f:
            dictionary = json.load(f)
    else:
        dictionary = create_dict(source_path)
        with open(dict_path, "w") as f:
            json.dump(dictionary, f)
    return {mapper(k): v for k, v in dictionary.items()}


def prepare_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)


def current_timestamp():
    return str(round(datetime.now().timestamp()))


def save(obj, path, file_name=current_timestamp()):
    """
    Saves the given object under the path + filename location. 
    If filename is ommited an unique name will be generated.
    """
    prepare_directory(path)
    with open(os.path.join(path, file_name), "w") as f:
        json.dump(obj, f, indent=2)


def load_raw(path, file_name, transform=lambda x: x):
    """
    Reads the given file into a list of strings optionally applying transform to each line.
    Returns an array of strings/or results from transform.
    """
    process_file = lambda f: [transform(line) for line in f]
    return load_bulk(path, file_name, process_file)[0]


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
        files = [os.path.joint(path, file_name)]
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
    # just flatten the array of arrays coming from load_bulk and apply transform
    return [
        transform(item) for sublist in load_bulk(path, file_name) for item in sublist
    ]


def load(path, file_name, transform=lambda x: x):
    """
    Loads one object in the given path + file_name and applies transform to it if given.
    """
    return load_bulk(path, file_name, transform)[0]


def save_level_info(level_info):
    prepare_directory(level_info_path)
    with open(os.path.join(level_info_path, "level.info"), "w") as f:
        json.dump(level_info, f)


def load_level_info(default):
    try:
        with open(os.path.join(level_info_path, "level.info"), "r") as f:
            return json.load(f)
    except:
        log.warn("Couldn't load level file, returning default level {}".format(default))
        return {"level": default}
