from files import load, load_raw, file_exists, save
from collections import defaultdict
from util import flatten
import log


def create_dict(path):
    """
    Creates a dictonary with word frequency based from all files in path
    """
    d = defaultdict(int)
    log.debug("Starting dictionary processing")
    tokens = flatten(flatten(load_raw(path, transform=lambda line: line.split())))
    log.debug("Found {} words".format(len(tokens)))

    for t in tokens:
        d[t] += 1
    log.debug("Done dictonary procesing")
    return d


def lazy_load_dict(dict_path, dictionary_name, source_path, mapper=lambda x: x):
    if file_exists(dict_path, dictionary_name):
        dictionary = load(dict_path, dictionary_name)
    else:
        dictionary = create_dict(source_path)
        save(dictionary, dict_path, dictionary_name)
    return {mapper(k): v for k, v in dictionary.items()}
