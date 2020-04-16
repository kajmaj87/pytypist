from controller import Controller
from key import Key
import curses
import log


class Console_ui:

    should_redraw = False

    def write_correct_char(self, key):
        self.stdscr.addch(key.char)

    def write_wrong_char(self, key):
        self.stdscr.addch(key.char, curses.A_STANDOUT)

    def redraw(self):
        self.stdscr.clear()

    def goto_writing_position(self):
        self.stdscr.move(1, 0)

    def get_next_key(self):
        return self.stdscr.getkey()

    def write(self, text):
        self.stdscr.addstr(text + "\n")

    def inner_loop(self, stdscr):
        self.stdscr = stdscr

        self.controller = Controller(self)
        c = ""
        while c != "`":  # main loops waits for Ctrl+C
            c = self.get_next_key()
            if ord(c) == ord(curses.erasechar()):
                self.controller.sendKey(Key(special="ERASE"))
                y, x = stdscr.getyx()
                stdscr.delch(y, x - 1)
            elif ord(c) not in [ord("\n"), curses.KEY_ENTER]:
                self.controller.sendKey(Key(c))

    def loop(self):
        curses.wrapper(self.inner_loop)
