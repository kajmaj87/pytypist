import random
import log

from focus import probabilities


def sanitize(
    dictonary,
    allowed_chars="qwertyuiop[]asdfghjkl;'\\zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:\"|ZXCVBNM<>?`1234567890-=~!@#$%^&*()_+",
):
    log.debug("Sanitazing dictionary for: {}".format(allowed_chars))
    all_letters_allowed = lambda word: all([letter in allowed_chars for letter in word])

    return {k: v for k, v in dictonary.items() if all_letters_allowed(k)}


def increase_letter_probability(dictionary, min_relative_probability=0.5):
    """ 
    Guarantees that each letter has at least the given relative probability of occuring.
    1 is the theoretic maximum and would mean that the letters are uniformly distributed, 
    but would probably cause this method to loop indifinetely so do not use it.
    """
    prob = probabilities(dictionary)
    total_letters = len(prob)
    new_dictionary = dictionary

    log.debug("Starting probabilities: {}".format(prob))

    def letters_with_low_probability(probabilities):
        return {
            k: v
            for k, v in probabilities.items()
            if v < 1 / total_letters * min_relative_probability
        }

    letters = letters_with_low_probability(prob)
    iterations = 0

    while len(letters) > 0 and iterations < 20:
        iterations += 1
        new_dictionary = {
            k: v * 4 if any([letter in k for letter in letters.keys()]) else v
            for k, v in new_dictionary.items()
        }
        prob = probabilities(new_dictionary)
        letters = letters_with_low_probability(prob)
    log.info(
        "Finished reasigning probabilies upto {} after {} iterations.".format(
            min_relative_probability, iterations
        )
    )
    log.debug("Ending probabilities: {}".format(prob))
    return new_dictionary


class FrequencyBasedGenerator:
    """Provides text based on the given dictonary with words and frequencies.
    :param dictonary: keys are words, values are relative probabilities of given word
    :type dictonary: dict
    """

    def __init__(self, dictonary):
        assert (
            len(dictonary) > 0
        ), "FrequencyBasedGenerator needs non-empty generator to work!"
        assert any(
            i > 0 for i in dictonary.values()
        ), "Dictionary needs at least one positive weight to work"

        self.dictonary = dictonary

    def generateText(self, minLength):
        d = self.dictonary
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
