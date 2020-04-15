import random


def sanitize(dictonary, allowed_chars):
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

        self.dictonary = sanitize(
            dictonary,
            "qwertyuiop[]asdfghjkl;'\zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:\"|ZXCVBNM<>?`1234567890-=~!@#$%^&*()_+",
        )

    def generateText(self, minLength):
        d = self.dictonary
        text = ""
        while len(text) < minLength + 1:
            text += (
                random.choices(
                    population=list(d.keys()), weights=list(d.values()), k=1
                )[0]
                + " "
            )
        text = text[:-1]  # cut last space
        return text
