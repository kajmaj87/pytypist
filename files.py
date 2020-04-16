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
        log.debug("Processing {}".format(file_path))
        with open(file_path) as fp:
            for line in fp:
                line = fp.readline()
                tokens = line.split()
                log.debug("Processing line ({} tokens): {}".format(len(tokens), line))
                for t in tokens:
                    d[t] += 1
    # log.debug({k: v for k, v in sorted(d.items(), key=lambda item: -item[1])})
    return d


def save_transitions(transitions):
    def prepare_directory(path):
        if not os.path.exists(path):
            os.makedirs(path)

    def current_timestamp():
        return str(datetime.now())

    prepare_directory(transition_path)
    with open(transition_path + "/" + current_timestamp(), "w") as f:
        json.dump(transitions, f, indent=2)


def load_transitions():
    files = [f for f in glob(transition_path + "/*")]
    transitions = []
    for f in files:
        with open(f) as current:
            transitions.extend(json.load(current))
    return [Transition(t[0], t[1], t[2], t[3]) for t in transitions]
