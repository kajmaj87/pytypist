from stage_stats import StageStats
from key_logger import KeyLogger
from transition_aggregator import TransitionAggregator
from dictonary_generator import DictonaryGenerator

class Controller:
    n = 1
    current_text = ""

    def __init__(self, output):
        text = "This is a very long text. It contains a lot of bla bla bla bla and other nonmeaningful words."
        text = "test"
        self.text = DictonaryGenerator({'nice': 5, 'hi': 1, 'test': 2, 'hello': 1}).generateText(60)
        self.output = output
        self.stats = StageStats(text)
        self.logger = KeyLogger()
        self.aggregator = TransitionAggregator()
        self.output.write(self.text)

    def sendKey(self, key):
        if key.char:
            self.current_text += key.char 
            self.output.write_char(key)
            if self.current_text == self.text[:self.n]:
                self.stats.registerKey(key, 'CORRECT')
                self.logger.log_key(key, 'CORRECT')
                self.n += 1
            else:
                self.stats.registerKey(key, 'ERROR')
                self.logger.log_key(key, 'ERROR')
        elif key.special == 'ERASE':
            self.current_text = self.current_text[:-1]
            self.stats.registerKey(key, 'ERASE')
            self.logger.log_key(key, 'ERASE')


        if self.current_text == self.text:
            self.output.close()
            self.stats.registerStageEnd()
            self.output.write("\nStage complete.\n")
            self.output.write(self.stats.summary())
            self.output.write("\nKey stats:\n")
#            self.output.write(self.logger.summary())
            self.output.write(self.aggregator.summary(self.logger.transitions()))


