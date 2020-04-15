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
        self.should_redraw = True

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
            while not self.should_redraw and c != "`":
                c = self.get_next_key()
                if ord(c) == ord(curses.erasechar()):
                    self.controller.sendKey(Key(special="ERASE"))
                    y, x = stdscr.getyx()
                    stdscr.delch(y, x - 1)
                else:
                    self.controller.sendKey(Key(c))

            self.stdscr.getkey()
            log.debug("Redrawing screen (key: {})".format(c))
            self.stdscr.clear()
            self.write(self.controller.start_next_stage())
            self.should_redraw = False

    def loop(self):
        curses.wrapper(self.inner_loop)
