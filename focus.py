import log
import random
from collections import defaultdict
from transition_aggregator import TransitionAggregator


def calculate_main_focus(errors, threshold=1):
    candidates_squared = [
        [e] * errors.count(e)
        for e in errors.replace(" ", "")
        if errors.count(e) >= threshold
    ]
    candidates = [item for sublist in candidates_squared for item in sublist]
    candidates.append("")
    return random.choice(candidates)


def calculate_main_focus_transitions(transitions):
    p95 = TransitionAggregator().p95_for_keys(transitions)
    if len(p95) > 0:
        return max(p95.items(), key=lambda x: x[1])[0]
    else:
        return ""


def calculate_secondary_focus(keys, limit=5):
    # letters that appeared the least often
    candidates = [k[0] for k in sorted(keys.items(), key=lambda x: len(x[1]))]
    log.debug(candidates)
    log.debug(sorted(keys.items(), key=lambda x: len(x[1])))
    return "".join(candidates[:limit])


def focus(dictonary, main="", secondary="", gain=10):
    has_main_letter = lambda t: any([l in t for l in main]) or len(main) == 0
    has_secondary_letter = lambda t: any([l in t for l in secondary])
    amount_of_secondary_letters = lambda word: sum([l in word for l in secondary])
    result = {
        k: max(1, amount_of_secondary_letters(k) * gain) * v
        for k, v in dictonary.items()
        if has_main_letter(k)
    }
    if len(result) == 0:
        log.warn(
            "Dictonary is empty after applying main focus [{}]. Returning full dictionary.".format(
                main
            )
        )
        return dictonary
    log.debug("Probabilities: {}".format(probabilities(result)))
    return result


def probabilities(dictonary):
    letters = set()
    result = defaultdict(int)
    total = sum([v for (k, v) in dictonary.items()])
    for k in dictonary.keys():
        letters.update(list(k))
    for l in letters:
        result[l] = sum([v for (k, v) in dictonary.items() if l in k]) / total
    return {k: v for k, v in sorted(result.items(), key=lambda item: -item[1])}
