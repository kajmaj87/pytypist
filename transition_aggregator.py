from collections import namedtuple, defaultdict
from statistics import mean

KeyStat = namedtuple('KeyStat', ['key','time'])

class TransitionAggregator:

    def stages(self, transitions):
        return sum([1 for t in transitions if t.start == 'START'])

    def errors(self, transitions):
        return sum([1 for t in transitions if t.state == 'ERROR'])

    def key_presses(self, transitions):
        return len(transitions)

    def correct(self, transitions):
        return sum([1 for t in transitions if t.state == 'CORRECT'])

    def erases(self, transitions):
        return sum([1 for t in transitions if t.state == 'ERASE'])
    
    def accuracy(self, transtions):
        return 100*self.correct(transtions)/(self.correct(transtions) + self.errors(transtions))

    def key_stats(self, transitions, filter_function = lambda x: x.start != 'START'):
        d = defaultdict(list)
        for t in transitions:
            if filter_function(t):
                d[t.end].append(t.time)
        return d

    def calculate_stats(self, stats, aggregate):
        result = {}
        for k,v in stats.items():
            result[k] = aggregate(v)
        return result

    def summary(self, transitions):
        def round_dict(d):
            result = {}
            for k,v in d.items():
                result[k] = round(v,1)
            return result
        return """Aggregations:
            Stages:      {}
            Key presses: {}
            Correct:     {}
            Errors:      {}
            Erases:      {}
            Accuracy:    {}%
            Fastest:     {}
            Means:       {}
            Longest:     {}
           """.format(self.stages(transitions), \
                      self.key_presses(transitions), \
                      self.correct(transitions), \
                      self.errors(transitions), \
                      self.erases(transitions), \
                      self.accuracy(transitions), \
                      round_dict(self.calculate_stats(self.key_stats(transitions), min)), \
                      round_dict(self.calculate_stats(self.key_stats(transitions), mean)), \
                      round_dict(self.calculate_stats(self.key_stats(transitions), max)))

