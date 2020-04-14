import time


class StageStats:

    total_chars = 0
    total_presses = 0
    start_time = None
    total_time = 0
    correct = 0
    errors = 0
    erases = 0

    def __init__(self, text):
        self.total_chars = len(text)

    def registerKey(self, key, state):
        if self.start_time is None:
            self.start_time = time.time_ns() / 1000000000
        self.total_presses += 1
        self.correct += 1 if state == "CORRECT" else 0
        self.errors += 1 if state == "ERROR" else 0
        self.erases += 1 if state == "ERASE" else 0

    def registerStageEnd(self):
        self.total_time = time.time_ns() / 1000000000 - self.start_time

    def summary(self):
        return """Statistics:
            chars: {}
            presses: {}
            total time: {:0.1f}s 
            time/keypress: {:0.2f}ms

            Accuracy: {:0.1f}%
            Correct: {}
            Errors: {}
            Erases: {}

            Total WPM: {:0.1f}
            Correct WPM: {:0.1f}""".format(
            self.total_chars,
            self.total_presses,
            self.total_time,
            self.total_time / self.total_presses * 1000,
            self.total_chars / (self.total_chars + self.errors) * 100,
            self.correct,
            self.errors,
            self.erases,
            self.total_presses / (self.total_time) / 5 * 60,
            self.total_chars / (self.total_time) / 5 * 60,
        )
