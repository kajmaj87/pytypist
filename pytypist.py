#!/home/kajman/projects/pytypist/.pytypist/bin/python
import curses
text = "This is some test text\n"
n = 0

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()

stdscr.addstr(text)
while 1:
    c = stdscr.getch()
    if c == ord(text[n]):
        stdscr.addch(c)
        n = n + 1
    elif c == ord('q'):
        break  # Exit the while()
    elif c == curses.KEY_HOME:
        x = y = 0

curses.nocbreak()
curses.echo()
