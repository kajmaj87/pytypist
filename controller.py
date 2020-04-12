class Controller:
    n = 0
    current_text = ""

    def __init__(self, text, output):
        self.text = text
        self.output = output

    def sendKey(self, key):
        if key.char:
            self.current_text += key.char 
            self.output.write_char(key)
        elif key.special == 'ERASE':
            self.current_text = self.current_text[:-1]
        if self.current_text == self.text:
            self.output.on_stage_complete()

    def getCurrentText(self):
        return self.current_text
