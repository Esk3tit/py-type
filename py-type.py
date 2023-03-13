import curses
from curses import wrapper


def start_screen(stdscr):
    # Clear screen
    stdscr.clear()

    stdscr.addstr("PYTHON TYPING APP\n")
    stdscr.addstr("Press any key to start")
    stdscr.refresh()

    # Wait for next input (user needs to press any key)
    key = stdscr.getkey()
    print(key)

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)


wrapper(main)
