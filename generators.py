import random
import log

from focus import probabilities, weights


def sanitize(
    dictionary,
    allowed_chars="qwertyuiop[]asdfghjkl;'\\zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:\"|ZXCVBNM<>?`1234567890-=~!@#$%^&*()_+",
):
    log.debug("Sanitazing dictionary for: {}".format(allowed_chars))
    all_letters_allowed = lambda word: all([letter in allowed_chars for letter in word])

    return {k: v for k, v in dictionary.items() if all_letters_allowed(k)}


def increase_letter_probability(dictionary, min_relative_probability):
    """ 
    Guarantees that each letter has at least the given relative probability of occuring.
    1 is the theoretic maximum and would mean that the letters are uniformly distributed.
    """
    prob = probabilities(dictionary)

    log.debug("Starting probabilities: {}".format(prob))

    w = weights(dictionary)
    total = sum(w.values())

    def gain(k, v):
        factor = total / len(w) * min_relative_probability
        lowest_weight = min([w[v] for v in k])
        result = max(factor / lowest_weight, 1)
        if result > 1:
            log.debug("lw/gain for {}: {}/{}".format(k, lowest_weight, result))
        return result

    result = {k: v * gain(k, v) for k, v in dictionary.items()}

    log.info(
        "Finished reasigning probabilies upto {}.".format(min_relative_probability)
    )
    prob = probabilities(result)
    log.debug("Ending probabilities: {}".format(prob))
    log.info(
        "Most/Least letter probability: {}".format(
            max(prob.values()) / min(prob.values())
        )
    )
    return result


class FrequencyBasedGenerator:
    """Provides text based on the given dictionary with words and frequencies.
    :param dictionary: keys are words, values are relative probabilities of given word
    :type dictionary: dict
    """

    def __init__(self, dictionary):
        assert (
            len(dictionary) > 0
        ), "FrequencyBasedGenerator needs non-empty generator to work!"
        assert any(
            i > 0 for i in dictionary.values()
        ), "Dictionary needs at least one positive weight to work"

        self.dictionary = dictionary

    def generateText(self, minLength):
        d = self.dictionary
        text = ""
        unique_words_sample = list(
            set(
                random.choices(
                    population=list(d.keys()), weights=list(d.values()), k=1000
                )
            )
        )
        random.shuffle(unique_words_sample)
        while len(text) < minLength + 1 and len(unique_words_sample) > 0:
            text += unique_words_sample.pop() + " "
        text = text[:-1]  # cut last space
        return text
