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

    def goto_writing_position(self, position=0):
        y, x = self.stdscr.getmaxyx()
        self.stdscr.move(max(1, round(y * position)), 0)

    def get_next_key(self):
        return self.stdscr.getkey()

    def calculate_x_position(self, justify, text):
        maxy, maxx = self.stdscr.getmaxyx()
        if justify == "LEFT":
            return 0
        if justify == "MIDDLE":
            return round(maxx / 2 - len(text) / 2)

    def write(self, text, justify="LEFT"):
        if justify == "LEFT":
            self.stdscr.addstr(text + "\n")
        if justify == "MIDDLE":
            y, x = self.stdscr.getyx()
            newx = self.calculate_x_position(justify, text)
            self.stdscr.addstr(y, newx, text)

    def write_stage(self, text, justify="LEFT"):
        y, x = self.stdscr.getyx()
        self.write(text, justify)
        newx = self.calculate_x_position(justify, text)
        self.stdscr.move(y + 1, newx)

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
