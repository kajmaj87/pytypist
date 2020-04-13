import time
from collections import namedtuple

class KeyLogger:

    Transition = namedtuple('Transition', ['start','end','state','time'])
    first_key = True
    keys = []

    def extract_to(self, key):
        return key.special if key.special is not ''  else key.char

    def time_ms(self):
        return time.time_ns()/1000000
        
    def log_key(self, key, state):
        if self.first_key:
            self.keys.append(self.Transition('START', self.extract_to(key), state, 0))
            self.first_key = False
        else: 
            self.keys.append(self.Transition(self.keys[-1].end, \
                                        self.extract_to(key), \
                                        state, \
                                        self.time_ms() - self.last_time))
        self.last_time = self.time_ms()

    def summary(self):
        return '\n'.join(["{}".format(k) for k in self.keys])

