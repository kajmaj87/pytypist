import log
from key_logger import KeyLogger
from transition_aggregator import TransitionAggregator
from generators import FrequencyBasedGenerator
from files import create_dict, save_transitions, load_transitions
from focus import focus


class Controller:
    def __init__(self, output):
        self.output = output
        self.aggregator = TransitionAggregator()
        self.generator = FrequencyBasedGenerator(
            focus(create_dict("data/moby-dick.txt"), ";:,./!?-", gain=100)
        )
        self.start_next_stage()
        self.output.write(self.text)

    def start_next_stage(self):
        self.current_text = ""
        self.n = 1
        self.text = self.generator.generateText(15)
        self.logger = KeyLogger()

    def get_stage_text(self):
        return self.text

    def sendKey(self, key):
        if key.char:
            self.current_text += key.char
            if self.current_text == self.text[: self.n]:
                self.logger.log_key(key, "CORRECT")
                self.output.write_correct_char(key)
                self.n += 1
            else:
                self.logger.log_key(key, "ERROR")
                self.output.write_wrong_char(key)
        elif key.special == "ERASE":
            self.current_text = self.current_text[:-1]
            self.logger.log_key(key, "ERASE")

        if self.current_text == self.text:
            self.output.redraw()
            save_transitions(self.logger.transitions())
            self.start_next_stage()
            log.debug("KeyLogger: {}".format(self.logger.transitions()))
            self.output.write(self.get_stage_text())
            self.output.write("\n\nKey stats:\n")
            self.output.write(self.aggregator.summary(load_transitions()))
            self.output.goto_writing_position()
