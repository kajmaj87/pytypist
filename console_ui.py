from controller import Controller
import key
import curses

class Console_ui:
  
  stage_complete = False

  def __init__(self):
    self.stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()

    text = "test\n"
    self.controller = Controller(text, self) 
    self.stdscr.addstr(text)
    
  def on_correct_key(self, key):
    self.stdscr.addch(key.char)

  def on_wrong_key(self, key):
    self.stdscr.addch(key.char)
    curses.flash() 

  def on_stage_complete(self):
    self.stage_complete = True

  def get_next_key(self):
    return self.stdscr.getkey()

  def loop(self):
    while not self.stage_complete:
      c = self.get_next_key()
      self.controller.sendKey(Key(c))
    curses.nocbreak()
    curses.echo()
