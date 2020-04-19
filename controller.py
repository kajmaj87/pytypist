import log
from level_controller import LevelController
from key_logger import KeyLogger
from transition_aggregator import TransitionAggregator
from generators import FrequencyBasedGenerator
from files import create_dict, save_transitions, load_transitions
from focus import (
    focus,
    calculate_main_focus,
    calculate_main_focus_transitions,
    calculate_secondary_focus,
)

MAX_TRANSITIONS = 5000


class Controller:
    def __init__(self, output):
        self.output = output
        self.aggregator = TransitionAggregator()
        self.level_controller = LevelController(
            create_dict("data/dictionaries", lambda x: x.lower())
        )
        self.generator = FrequencyBasedGenerator(
            self.level_controller.dictionary_for_current_level()
        )
        self.start_next_stage()

    def start_next_stage(self, transitions=[]):
        def calculate_stage_lenght(seconds, transitions):
            lenght = 0
            min_lenght = 10
            if len(transitions) > 0:
                return max(
                    min_lenght,
                    round(self.aggregator.wpm(transitions) * 5 * seconds / 60),
                )
            else:
                return min_lenght

        stage_lenght = calculate_stage_lenght(5, transitions)
        log.debug("Stage lenght will be: {}".format(stage_lenght))
        self.current_text = ""
        self.n = 1
        main_focus = calculate_main_focus_transitions(transitions)
        self.level_controller.advance_to_next_level_if_possible(
            self.aggregator.key_stats(transitions)
        )
        secondary_focus = calculate_secondary_focus(
            self.aggregator.key_stats(transitions, lambda x: x.state == "CORRECT"), 10
        )
        self.generator = FrequencyBasedGenerator(
            focus(
                self.level_controller.dictionary_for_current_level(),
                main_focus,
                secondary_focus,
            )
        )
        self.text = self.generator.generateText(stage_lenght)
        self.logger = KeyLogger()
        self.output.write(self.get_stage_text())
        if len(transitions) > 0:
            self.output.write(
                "\n\nFocus for stage:\nMain: [{}]\tSecondary: [{}]".format(
                    main_focus, secondary_focus
                )
            )
            self.output.write("\n\nKey stats:\n")
            self.output.write(
                self.aggregator.summary(load_transitions()[-MAX_TRANSITIONS:])
            )
        self.output.goto_writing_position()

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
            self.start_next_stage(load_transitions()[-MAX_TRANSITIONS:])
