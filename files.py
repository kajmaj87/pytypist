from collections import defaultdict
import log


def create_dict(path):
    """
    Creates a dictonary with word frequency based on the file from path
    """
    d = defaultdict(int)
    log.debug("Starting dictionary processing")
    with open(path) as fp:
        for line in fp:
            line = fp.readline()
            tokens = line.split()
            for t in tokens:
                d[t] += 1
    log.debug({k: v for k, v in sorted(d.items(), key=lambda item: -item[1])})
    return d
