from controller import Controller
from key import Key
import curses
import log


class Console_ui:

    should_redraw = False

    def write_char(self, key):
        self.stdscr.addch(key.char)

    def redraw(self):
        log.debug("Will redraw screen")
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
        log.debug("Redraw: {}".format(self.should_redraw))
        while c != "`":  # main loops waits for Ctrl+C
            c = self.get_next_key()
            if ord(c) == ord(curses.erasechar()):
                self.controller.sendKey(Key(special="ERASE"))
                y, x = stdscr.getyx()
                stdscr.delch(y, x - 1)
            else:
                self.controller.sendKey(Key(c))

    def loop(self):
        curses.wrapper(self.inner_loop)
