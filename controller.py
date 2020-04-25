import log
from level_controller import LevelController
from key_logger import KeyLogger
from transition_aggregator import TransitionAggregator
from generators import FrequencyBasedGenerator
from transition_repository import save_transitions, load_transitions
from dictionaries import lazy_load_dict
from focus import (
    focus,
    calculate_main_focus_transitions,
    calculate_secondary_focus,
    calculate_secondary_focus_from_errors,
)

MAX_TRANSITIONS = 50000
zen_mode = False


class Controller:
    def __init__(self, output):
        self.output = output
        self.aggregator = TransitionAggregator()
        self.level_controller = LevelController(
            lazy_load_dict(
                "data", "pl-sci-fi.dict", "data/dictionaries", lambda x: x.lower()
            )
        )
        self.generator = FrequencyBasedGenerator(
            self.level_controller.dictionary_for_current_level()
        )
        self.start_next_stage()

    def format_main_focus(self, main_focus, worst_value, focus_type):
        if focus_type == "COUNT":
            return "Count:    {} - {:2d}".format(main_focus, worst_value)
        if focus_type == "ACCURACY":
            return "Accuracy: {} - {:.1f}%".format(main_focus, worst_value * 100)
        if focus_type == "SPEED":
            return "Speed:    {} - {:.1f} WPM".format(main_focus, worst_value)

    def update_stage(self, transitions, main_focus, focus_string):
        if zen_mode:
            self.output.goto_writing_position(0.1)
            self.output.write(
                "Level {}: {}".format(
                    self.level_controller.current_level,
                    self.level_controller.new_chars(),
                ),
                justify="MIDDLE",
            )
            self.output.write("\n")
            self.output.write(
                main_focus if main_focus is not None else "", justify="MIDDLE"
            )
            self.output.write("\n")
            self.output.write_stage(self.get_stage_text(), justify="MIDDLE")
        else:
            self.output.write(self.get_stage_text())
            if len(transitions) > 0:
                self.output.write(focus_string)
                self.output.write("\n\nKey stats:\n")
                self.output.write(
                    self.aggregator.summary(load_transitions()[-MAX_TRANSITIONS:])
                )

            # TODO this call is now redunant with write_stage method
            self.output.goto_writing_position()

    def start_next_stage(self, transitions=[]):
        def calculate_stage_lenght(seconds, transitions):
            lenght = 0
            min_lenght = 10
            if len(transitions) > 0:
                return max(
                    min_lenght,
                    round(self.aggregator.total_wpm(transitions) * 5 * seconds / 60),
                )
            else:
                return min_lenght

        stage_lenght = calculate_stage_lenght(5, transitions)
        log.debug("Stage lenght will be: {}".format(stage_lenght))
        self.current_text = ""
        self.n = 1
        self.level_controller.advance_to_next_level_if_possible(transitions)
        (
            main_focus,
            worst_value,
            focus_type,
        ) = self.level_controller.main_focus_for_level(transitions)
        secondary_focus = calculate_secondary_focus_from_errors(
            self.aggregator.last_errors(transitions)
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
        short_focus = self.format_main_focus(main_focus, worst_value, focus_type)
        focus_string = "\n\nFocus for stage:\n{}\tSecondary: [{}]".format(
            short_focus, secondary_focus,
        )
        self.update_stage(transitions, short_focus, focus_string)

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
