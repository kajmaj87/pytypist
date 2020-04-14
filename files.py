from collections import defaultdict
import logging as log


def create_dict(path):
    """
    Creates a dictonary with word frequency based on the file from path
    """
    d = defaultdict(int)
    with open(path) as fp:
        line = fp.readline()
        tokens = line.split()
        for t in tokens:
            d[t] += 1
    log.debug(d)
    return d
