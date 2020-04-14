from controller import Controller
from key import Key
import curses


class Console_ui:

    stage_complete = False

    def write_char(self, key):
        self.stdscr.addch(key.char)

    def close(self):
        self.stage_complete = True

    def get_next_key(self):
        return self.stdscr.getkey()

    def write(self, text):
        self.stdscr.addstr(text + "\n")

    def inner_loop(self, stdscr):
        self.stdscr = stdscr

        self.controller = Controller(self)
        while not self.stage_complete:
            c = self.get_next_key()
            if ord(c) == ord(curses.erasechar()):
                self.controller.sendKey(Key(special="ERASE"))
                y, x = stdscr.getyx()
                stdscr.delch(y, x - 1)
            else:
                self.controller.sendKey(Key(c))
        self.stdscr.getkey()

    def loop(self):
        curses.wrapper(self.inner_loop)
