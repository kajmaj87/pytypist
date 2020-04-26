import log
from transition_aggregator import TransitionAggregator
from statistics import mean
from generators import sanitize  # TODO move to this class
from game_state import save_level_info, load_level_info


min_occurences = 10
min_wpm = 30
min_accuracy = 0.9


def wpm(key_time_in_seconds):
    return 60 / key_time_in_seconds / 5


class LevelController:
    chars_allowed = [
        "asdflkjh",
        "ru",
        "ei",
        "wo",
        "qp",
        "ty",
        "gh",
        "vm",
        "c,",
        "x.",
        "z/",
        "bn",
        "[]",
        "'\\",
        "-=",
        "10",
        "29",
        "38",
        "47",
        "56",
    ]

    from level_controller import wpm

    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.aggregator = TransitionAggregator()
        self.current_level = load_level_info(default=1)["level"]

    def occurences(self, key_stats):
        return {
            k: len(key_stats[k]) if k in key_stats else 0 for k in self.current_chars()
        }

    def mean_wpm_for_keys(self, key_stats):
        return {
            k: wpm(mean(v)) for k, v in key_stats.items() if k in self.current_chars()
        }

    def time_accuracy(self, transitions):
        return {
            k: v
            for k, v in self.aggregator.time_accuracy_for_keys(transitions).items()
            if k in self.current_chars()
        }

    def advance_to_next_level_if_possible(self, transitions):
        key_stats = self.aggregator.adjusted_key_stats(transitions)
        all_occured = all(
            [v >= min_occurences for v in self.occurences(key_stats).values()]
        )
        all_fast = all(
            [v > min_wpm for v in self.mean_wpm_for_keys(key_stats).values()]
        )
        all_accurate = all(
            [v > min_accuracy for v in self.time_accuracy(transitions).values()]
        )
        if not all_occured:
            log.debug(
                "Won't advance as not all yet occured {} times: {}".format(
                    min_occurences,
                    {
                        k: v
                        for k, v in self.occurences(key_stats).items()
                        if v < min_occurences
                    },
                )
            )
        if not all_fast:
            log.debug(
                "Won't advance as not yet fast enough (>{}WPM): {}".format(
                    min_wpm,
                    {
                        k: v
                        for k, v in self.mean_wpm_for_keys(key_stats).items()
                        if v < min_wpm
                    },
                )
            )
        if not all_accurate:
            log.debug(
                "Won't advance as not yet accurate enough (>{:0.1f}%): {}".format(
                    min_accuracy * 100,
                    {
                        k: v
                        for k, v in self.time_accuracy(transitions).items()
                        if v < min_accuracy
                    },
                )
            )

        if all_occured and all_fast and all_accurate:
            self.current_level += 1
            save_level_info({"level": self.current_level})
            log.info("Advancing to level {}".format(self.current_level))

    def main_focus_for_level(self, transitions):
        log.debug(
            "Calculating focus for level {} (letters: {})".format(
                self.current_level, self.current_chars()
            )
        )

        key_stats = self.aggregator.adjusted_key_stats(transitions)
        if len(key_stats) == 0:
            log.warn("No key stats in given transitions, won't calclulate focus")
            return "", "", ""

        min_occurence = min(self.occurences(key_stats).items(), key=lambda x: x[1],)
        worst_accuracy = min(
            self.time_accuracy(transitions).items(), key=lambda x: x[1]
        )
        slowest = min(self.mean_wpm_for_keys(key_stats).items(), key=lambda x: x[1],)

        if min_occurence[1] < min_occurences:
            log.info(
                "Focus on occurences: [{}]: {}".format(
                    min_occurence[0], min_occurence[1]
                )
            )
            return (min_occurence[0], min_occurence[1], "COUNT")
        if worst_accuracy[1] < min_accuracy:
            log.info(
                "Focus on accuracy: [{}]: {:0.1f}%".format(
                    worst_accuracy[0], worst_accuracy[1] * 100
                )
            )
            return (worst_accuracy[0], worst_accuracy[1], "ACCURACY")
        if slowest[1] < min_wpm:
            log.info("Focus on speed: [{}]: {:0.1f} WPM".format(slowest[0], slowest[1]))
            return (slowest[0], slowest[1], "SPEED")
        # no focus needed
        log.info("No focus needed as all stats are fine.")
        return "", "", ""

    def current_chars(self):
        return "".join(self.chars_allowed[: self.current_level])

    def new_chars(self):
        return self.chars_allowed[self.current_level - 1]

    def dictionary_for_current_level(self):
        return sanitize(self.dictionary, self.current_chars())
