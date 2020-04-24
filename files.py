from collections import defaultdict
import os
import log
from glob import glob
import json
from entities import Transition
from datetime import datetime

transition_path = "stats/transitions"
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


def save_transitions(transitions):
    def current_timestamp():
        return str(round(datetime.now().timestamp()))

    prepare_directory(transition_path)
    with open(os.path.join(transition_path, current_timestamp()), "w") as f:
        json.dump(transitions, f, indent=2)


def load_transitions(char_limit=100):
    files = [f for f in glob(os.path.join(*transition_path.split("/"), "*"))]
    transitions = []
    letters = defaultdict(int)
    for f in reversed(files):  # read newest files first
        with open(f) as current:
            new = json.load(current)
            only_ending = [t[1] for t in new if t[2] == "CORRECT"]
            new_letters = defaultdict(int)
            new_letters.update({t: only_ending.count(t) for t in only_ending})
            log.debug("New letters found: {}".format(new_letters))
            transitions.extend(new)
            letters.update(
                {
                    k: letters[k] + new_letters[k]
                    for k in letters.keys() | new_letters.keys()
                }
            )
            log.debug("All letters so far: {}".format(letters))

        # end early if read enough
        if all([v > char_limit for v in letters.values()]):
            return [Transition(t[0], t[1], t[2], t[3]) for t in transitions]
    return [Transition(t[0], t[1], t[2], t[3]) for t in transitions]


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
        return default
