import log
from collections import defaultdict
from entities import Transition
from files import save, load_arrays

transition_path = "stats/transitions"


def save_transitions(transitions):
    log.debug("Saving transitions")
    save(transitions, transition_path)


def load_transitions(max_chars=100):
    log.debug("Loading transitions")
    result = load_arrays(
        transition_path, transform=lambda t: Transition(t[0], t[1], t[2], t[3])
    )
    log.debug("Done loading transitions")
    return limit(result, max_chars)


def limit(transitions, max_chars):
    counts = defaultdict(int)
    result = []
    skipped = 0
    log.debug("Looking through {} records".format(len(transitions)))
    for t in reversed(transitions):
        if t.state == "CORRECT":
            should_record_chars = counts[t.end] < max_chars
            log.debug("Will record: {} record: {}".format(should_record_chars, t))
        if should_record_chars:
            if t.state == "CORRECT":
                counts[t.end] += 1
            result.insert(0, t)
        else:
            log.debug("Skipping record: {}".format(t))
            log.debug("Counts {}".format(counts))
            skipped += 1
    log.debug("Skipped {} records when analysing transitions".format(skipped))
    return result
