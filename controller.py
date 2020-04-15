from key_logger import KeyLogger
from transition_aggregator import TransitionAggregator
from generators import FrequencyBasedGenerator
from files import create_dict, save_transitions, load_transitions
from focus import focus


class Controller:
    n = 1
    current_text = ""

    def __init__(self, output):
        self.start_next_stage()
        self.output = output
        self.logger = KeyLogger()
        self.aggregator = TransitionAggregator()
        self.output.write(self.text)

    def start_next_stage(self):
        self.current_text = ""
        self.text = FrequencyBasedGenerator(
            focus(create_dict("data/moby-dick.txt"), ";:,./!?-", gain=100)
        ).generateText(15)
        return self.text

    def get_stage_text(self):
        return self.text

    def sendKey(self, key):
        if key.char:
            self.current_text += key.char
            self.output.write_char(key)
            if self.current_text == self.text[: self.n]:
                self.logger.log_key(key, "CORRECT")
                self.n += 1
            else:
                self.logger.log_key(key, "ERROR")
        elif key.special == "ERASE":
            self.current_text = self.current_text[:-1]
            self.logger.log_key(key, "ERASE")

        if self.current_text == self.text:
            self.output.redraw()
            self.start_next_stage()
            save_transitions(self.logger.keys)
            self.output.write("\nKey stats:\n")
            self.output.write(self.aggregator.summary(load_transitions()))
