import log
from collections import namedtuple, defaultdict
from statistics import mean, median, quantiles

KeyStat = namedtuple("KeyStat", ["key", "time"])


class TransitionAggregator:
    def wpm(self, key_time_in_seconds):
        return 60 / key_time_in_seconds / 5

    def stages(self, transitions):
        return sum([1 for t in transitions if t.start == "START"])

    def errors(self, transitions):
        return len(self.last_errors(transitions))

    def adjusted_key_stats(self, transitions):
        """
        Gives the total time in seconds it took to write the given character correctly. Accounts for error correction.
        """
        result = defaultdict(list)
        current_time = 0
        for t in transitions:
            if t.start == "START":
                continue
            if t.state != "CORRECT":
                current_time += t.time / 1000
            else:
                result[t.end].append(current_time + t.time / 1000)
                current_time = 0

        return result

    def calculate_for_adjusted_keys(self, adjusted_key_stats, function):
        return {
            k: function(v)
            for k, v in sorted(
                adjusted_key_stats.items(), key=lambda x: function(x[1]),
            )
        }

    def calculate_for_transitions(self, transitions, function):
        return self.calculate_for_adjusted_keys(
            self.adjusted_key_stats(transitions), function
        )

    def total_time_for_keys(self, transitions):
        return self.calculate_for_transitions(transitions, sum)

    def count_for_keys(self, transitions):
        return self.calculate_for_transitions(transitions, len)

    def mean_for_keys(self, transitions):
        return self.calculate_for_transitions(
            transitions, function=lambda x: self.wpm(mean(x))
        )

    def median_for_keys(self, transitions):
        return self.calculate_for_transitions(
            transitions, function=lambda x: self.wpm(median(x))
        )

    def p95_for_keys(self, transitions):
        stats = {
            k: v for k, v in self.adjusted_key_stats(transitions).items() if len(v) > 9
        }
        result = {}
        for k, v in stats.items():
            result[k] = quantiles(v, n=20, method="inclusive")[-1]

        log.debug("P95: {}".format(result))

        return {
            k: self.wpm(v)
            for k, v in sorted(result.items(), key=lambda x: x[1], reverse=True)
            if v > 0
        }

    def time_accuracy_for_keys(self, transitions):
        total = self.total_time_for_keys(transitions)
        # TODO needs fixing. use normal error counting method without limit based on adjusted key stats?
        error = self.total_error_time_for_keys(transitions)
        log.debug(
            "Counting time accuracy 1 - error/total: 1 - {}/{}".format(error, total)
        )
        return {k: (v - error[k]) / v if k in error else 1 for k, v in total.items()}

    def total_error_time_for_keys(self, transitions):
        # TODO rewrite this method, it should not take limit into account anymore with new transition system
        limit = 100
        result = defaultdict(int)
        keypresses = defaultdict(int)
        last_correct_key = None

        for t in reversed(transitions):
            if t.state == "CORRECT" and (keypresses[t.end] <= limit or limit == 0):
                keypresses[t.end] += 1
            if t.state == "CORRECT":
                last_correct_key = t.end
            if (
                keypresses[last_correct_key] > 0
                and (keypresses[last_correct_key] <= limit or limit == 0)
                and t.state != "CORRECT"
                and len(last_correct_key) == 1
                and last_correct_key is not None
            ):
                # TODO unify everything to seconds
                result[last_correct_key] += t.time / 1000

        return {
            k: v for k, v in sorted(result.items(), key=lambda x: x[1], reverse=True)
        }

    def last_errors(self, transitions, max_errors=None):
        """
        Gives back sorted string of length max_errors (or all of it if ommited).
        Error means the character that the user wanted to type but mistyped.
        """
        original_error = False
        result = ""
        for t in transitions:
            if t.state == "ERROR" and not original_error:
                original_error = True
            if t.state == "CORRECT" and original_error:
                original_error = False
                result += t.end
        if max_errors is not None:
            limit = min(max_errors, len(result))
        else:
            limit = len(result)
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

    def total_wpm(self, transitions):
        return self.correct(transitions) / self.total_time(transitions) * 60 / 5

    def format_dict(self, dictonary, max_entries, format_string="'{}' {:.1f}s "):
        result = ""
        entries = 0
        for k, v in dictonary.items():
            result += format_string.format(k, v)
            entries += 1
            if entries == max_entries:
                return result
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

            WPM:                {:.1f}
            WPM if w/o error:   {:.1f} (if you typed at your current speed but without errors)
            Least perfect WPM:  {:.1f} (if you typed without error, but slower, this will be enough to reach your speed)

            Total time:         {:.1f}s
            Time fixing errors: {:.1f}s
            Time w/o error:     {:.1f}s

            Accuracy:           {:.1f}%
            Time Accuracy:      {:.1f}%  (% time spent on correct chars)

            Last Errors:        {}

            Keys:
            Counts:             {}
            Total Times:        {}
            Mean   [WPM]:       {}
            Median [WPM]:       {}
            P95    [WPM]:       {}
            Errors:             {}
           """.format(
            self.stages(transitions),
            self.key_presses(transitions),
            self.correct(transitions),
            len(self.last_errors(transitions)),
            self.erases(transitions),
            self.total_wpm(transitions),
            self.correct(transitions)
            / self.time_if_without_errors(transitions)
            * 60
            / 5,
            self.time_if_without_errors(transitions)
            / self.total_time(transitions)
            * (self.correct(transitions) / self.total_time(transitions) * 60 / 5),
            self.total_time(transitions),
            self.time_fixing_errors(transitions),
            self.time_if_without_errors(transitions),
            self.accuracy(transitions),
            self.time_if_without_errors(transitions)
            / self.total_time(transitions)
            * 100,
            "".join(
                sorted(
                    sorted(errors.replace(" ", "")),
                    key=lambda l: errors.count(l),
                    reverse=True,
                )
            ),
            self.format_dict(self.count_for_keys(transitions), 25, "'{}' {} "),
            self.format_dict(self.total_time_for_keys(transitions), 15),
            self.format_dict(self.mean_for_keys(transitions), 15, "'{}' {:.1f} "),
            self.format_dict(self.median_for_keys(transitions), 15, "'{}' {:.1f} "),
            self.format_dict(self.p95_for_keys(transitions), 15, "'{}' {:.1f} "),
            self.format_dict(self.total_error_time_for_keys(transitions), 15),
        )
