from collections import defaultdict
import os
import log
from glob import glob
import json
from key_logger import Transition
from datetime import datetime

transition_path = "stats/transitions"


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


def save_transitions(transitions):
    def prepare_directory(path):
        if not os.path.exists(path):
            os.makedirs(path)

    def current_timestamp():
        return str(round(datetime.now().timestamp()))

    prepare_directory(transition_path)
    with open(os.path.join(transition_path, current_timestamp()), "w") as f:
        json.dump(transitions, f, indent=2)


def load_transitions():
    files = [f for f in glob(os.path.join(*transition_path.split("/"), "*"))]
    transitions = []
    for f in files:
        with open(f) as current:
            transitions.extend(json.load(current))
    return [Transition(t[0], t[1], t[2], t[3]) for t in transitions]
