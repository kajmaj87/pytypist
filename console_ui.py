from controller import Controller
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
    self.stdscr.addch(key)

  def on_wrong_key(self, key):
    curses.flash() 

  def on_stage_complete(self):
    self.stage_complete = True

  def get_next_char(self):
    return self.stdscr.getch()

  def loop(self):
    while not self.stage_complete:
      c = self.get_next_char()
      self.controller.sendKey(chr(c))
    curses.nocbreak()
    curses.echo()
