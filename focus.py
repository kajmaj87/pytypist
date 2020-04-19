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


def focus(dictonary, main="", secondary=""):
    def apply_main_letter(dictonary, main):
        has_main_letter = lambda t: any([l in t for l in main]) or len(main) == 0
        return {k: v for k, v in dictonary.items() if has_main_letter(k)}

    log.info("Calculating focus for [{}] and [{}]".format(main, secondary))
    main_dictionary = apply_main_letter(dictonary, main)
    if len(main_dictionary) == 0:
        log.warn(
            "Dictonary is empty after applying main focus [{}]. Returning full dictionary.".format(
                main
            )
        )
        return dictonary
    letter_weights = weights(main_dictionary)
    log.debug(
        "Weights in main: {}".format(
            {k: v for k, v in weights(main_dictionary).items()}
        )
    )
    max_weight = max(letter_weights.items(), key=lambda x: x[1])[1]
    log.debug("Total {} letters: {}".format(len(letter_weights), letter_weights))
    secondary_gain = {
        k: max_weight / letter_weights[k]
        for k in letter_weights.keys()
        if k in secondary
    }

    log.debug("Secondary gain: {}".format(secondary_gain))

    result = {
        k: v * max(1, sum([secondary_gain[l] for l in k if l in secondary]))
        for k, v in main_dictionary.items()
    }

    log.debug(
        "Weights: {}".format(
            {k: v for k, v in weights(result).items() if k in secondary}
        )
    )
    log.debug(
        "Most probable words: {}".format(
            {k: v for k, v in sorted(result.items(), key=lambda x: x[1], reverse=True)}
        )
    )

    return result


def weights(dictonary):
    letters = set()
    result = defaultdict(int)
    total = sum([v for (k, v) in dictonary.items()])
    for k in dictonary.keys():
        letters.update(list(k))
    for l in letters:
        result[l] = sum([v for (k, v) in dictonary.items() if l in k])
    return {k: v for k, v in sorted(result.items(), key=lambda item: -item[1])}
