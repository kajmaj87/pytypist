import log
from generators import sanitize  # TODO move to this class

chars_allowed = ["asdfjkl;", "ur", "ei", "wo", "qp"]


min_occurences = 10
min_wpm = 30
min_accuracy = 0.95


class LevelController:

    current_level = 1

    def __init__(self, dictionary):
        self.dictionary = dictionary

    def advance_to_next_level_if_possible(self, key_stats):
        all_occured = all(
            [len(occurences) >= min_occurences for occurences in key_stats.values()]
        )
        if all_occured:
            self.current_level += 1
            log.info("Advancing to level {}".format(self.current_level))

    def current_chars(self):
        return "".join(chars_allowed[: self.current_level])

    def dictionary_for_current_level(self):
        return sanitize(self.dictionary, self.current_chars())
