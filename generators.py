import random
import log


def sanitize(
    dictonary,
    allowed_chars="qwertyuiop[]asdfghjkl;'\\zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:\"|ZXCVBNM<>?`1234567890-=~!@#$%^&*()_+",
):
    log.debug("Sanitazing dictionary for: {}".format(allowed_chars))
    all_letters_allowed = lambda word: all([letter in allowed_chars for letter in word])

    return {k: v for k, v in dictonary.items() if all_letters_allowed(k)}


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
