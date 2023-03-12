import curses
from curses import wrapper

def main(stdscr):
    # Clear screen
    stdscr.clear()

    stdscr.addstr("Hello World!")
    stdscr.refresh()

    # Wait for next input (user needs to press any key)
    stdscr.getkey()

wrapper(main)