import log
from collections import defaultdict


def focus(dictonary, main="", secondary="", gain=10):
    has_main_letter = lambda t: any([l in t for l in main]) or len(main) == 0
    has_secondary_letter = lambda t: any([l in t for l in secondary])
    amount_of_secondary_letters = lambda word: sum([l in word for l in secondary])
    result = {
        k: max(1, amount_of_secondary_letters(k) * gain) * v
        for k, v in dictonary.items()
        if has_main_letter(k)
    }
    assert (
        len(result) > 0
    ), "Dictonary is empty after applying main focus. Provide bigger dictonary or less restrictive focus"
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
