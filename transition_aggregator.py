import log
from collections import namedtuple, defaultdict
from statistics import mean

KeyStat = namedtuple("KeyStat", ["key", "time"])


class TransitionAggregator:
    def stages(self, transitions):
        return sum([1 for t in transitions if t.start == "START"])

    def errors(self, transitions):
        return len(self.last_errors(transitions))

    def adjusted_key_stats(self, transitions):
        """
        Gives the total time it took to write the given character correctly. Accounts for error correction.
        """
        result = defaultdict(list)
        current_time = 0
        for t in transitions:
            if t.start == "START":
                continue
            if t.state != "CORRECT":
                current_time += t.time
            else:
                result[t.end].append(current_time + t.time)
                current_time = 0

        return result

    def last_errors(self, transitions, max_errors=None):
        """
        Gives back sorted string of length max_errors (or all of it if ommited).
        Error means the character that the user wanted to type but mistyped.
        """
        original_error = False
        result = ""
        log.debug(transitions)
        for t in transitions:
            if t.state == "ERROR" and not original_error:
                original_error = True
            if t.state == "CORRECT" and original_error:
                original_error = False
                log.debug("Adding error based on: {}".format(t))
                result += t.end
        if max_errors is not None:
            limit = min(max_errors, len(result))
        else:
            limit = len(result)
        log.debug("Errors: {}".format(result))
        return result[:limit]

    def key_presses(self, transitions):
        return len(transitions)

    def correct(self, transitions):
        return sum([1 for t in transitions if t.state == "CORRECT"])

    def erases(self, transitions):
        return sum([1 for t in transitions if t.state == "ERASE"])

    def total_time(self, transitions):
        return sum([t.time for t in transitions]) / 1000

    def time_fixing_errors(self, transitions):
        return (
            sum(
                [
                    t.time
                    for t in transitions
                    if t.state == "ERROR" or t.state == "ERASE"
                ]
            )
            / 1000
        )

    def time_if_without_errors(self, transitions):
        return self.total_time(transitions) - self.time_fixing_errors(transitions)

    def accuracy(self, transitions):
        return (
            100
            * self.correct(transitions)
            / (self.correct(transitions) + self.errors(transitions))
        )

    def key_stats(self, transitions, filter_function=lambda x: x.start != "START"):
        d = defaultdict(list)
        for t in transitions:
            if filter_function(t):
                d[t.end].append(t.time)
        return d

    def calculate_stats(self, stats, aggregate):
        result = {}
        for k, v in stats.items():
            result[k] = aggregate(v)
        return result

    def summary(self, transitions):
        def round_dict(d):
            result = {}
            for k, v in d.items():
                result[k] = round(v, 1)
            return result

        errors = self.last_errors(transitions)
        return """Aggregations:
            Stages:             {}
            Key presses:        {}
            Correct:            {}
            Errors:             {}
            Erases:             {}
            Total time:         {:.1f}s
            Time fixing errors: {:.1f}s
            Time w/o error:     {:.1f}s
            Accuracy:           {:.1f}%
            Time Accuracy:      {:.1f}%  (% time spent on correct chars)
            Last Errors:        {}
           """.format(
            self.stages(transitions),
            self.key_presses(transitions),
            self.correct(transitions),
            len(self.last_errors(transitions)),
            self.erases(transitions),
            self.total_time(transitions),
            self.time_fixing_errors(transitions),
            self.time_if_without_errors(transitions),
            self.accuracy(transitions),
            self.time_if_without_errors(transitions)
            / self.total_time(transitions)
            * 100,
            "".join(
                sorted(sorted(errors), key=lambda l: errors.count(l), reverse=True)
            ),
        )
