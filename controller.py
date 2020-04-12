class Controller:
    n = 0

    def __init__(self, text, output):
        self.text = text
        self.output = output

    def sendKey(self, key):
        if key.char == self.text[self.n]:
            self.output.on_correct_key(key)
            self.n = self.n + 1
            if self.n == len(self.text):
                self.output.on_stage_complete()
        else:
            self.output.on_wrong_key(key)
