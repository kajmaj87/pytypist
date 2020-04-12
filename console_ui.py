from controller import Controller
from key import Key
import curses

class Console_ui:
  
  stage_complete = False

  def write_char(self, key):
    self.stdscr.addch(key.char)

  def on_stage_complete(self):
    self.stage_complete = True

  def get_next_key(self):
    return self.stdscr.getkey()

  def inner_loop(self, stdscr):
    self.stdscr = stdscr

    text = "test\n"
    self.controller = Controller(text, self) 
    self.stdscr.addstr(text)
    while not self.stage_complete:
      c = self.get_next_key()
      if ord(c) == ord(curses.erasechar()): 
          self.controller.sendKey(Key(special='ERASE'))
          y, x = stdscr.getyx()
          stdscr.delch(y, x - 1)
      else:
          self.controller.sendKey(Key(c))

  def loop(self):
      curses.wrapper(self.inner_loop)
