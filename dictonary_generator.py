import random

class DictonaryGenerator:
    """Provides text based on the given dictonary with words and frequencies.
    :param dictonary: keys are words, values are relative probabilities of given word
    :type dictonary: dict
    """

    def __init__(self, dictonary):
        self.dictonary = dictonary

    def generateText(self, minLength):
        d = self.dictonary
        text = "" 
        while len(text) < minLength:
           text += random.choices(population=list(d.keys()),\
                                      weights=list(d.values()),\
                                      k=1)[0] + " "
        text = text[:-1] # cut last space
        return text
