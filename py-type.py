import curses
from curses import wrapper
import time
import string
import random
import os
import userdata
import pickle

USER_DATA_FILE = 'user.dat'


def start_screen(stdscr):
    # Clear screen
    stdscr.erase()

    stdscr.addstr("PYTHON TYPING APP\n")
    stdscr.addstr("Press any key to start")
    stdscr.refresh()

    # Wait for next input (user needs to press any key)
    stdscr.getkey()


def display_text(stdscr, target, current, wpm=0):
    # Add special unicode symbol representations for spaces and new lines
    for char in target:
        target_char = char
        if char == ' ':
            target_char = '\u2423'

        stdscr.addstr(target_char)

    stdscr.addstr(f"\nWPM: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(3)
        if char == correct_char and correct_char == ' ':
            color = curses.color_pair(4)
        elif char == correct_char:
            color = curses.color_pair(1)
        else:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)


def get_keys_to_practice(stdscr):
    keys_set = set()
    allowed_keys = []

    while True:
        stdscr.erase()
        stdscr.addstr("Enter the letters you want in the typing prompt (no delimiters, ex. 'abCde./,')\n")
        stdscr.addstr("Enter ESC to stop entering keys")
        stdscr.addstr(3, 0, f"Current keys: {' '.join([key for key in allowed_keys])}")
        stdscr.refresh()
        key = stdscr.getkey()

        if ord(key) == 27:
            break
        elif key in keys_set or key not in string.printable:
            continue
        else:
            keys_set.add(key)
            allowed_keys.append(key)

    return allowed_keys


def load_user(stdscr):
    user = None
    if os.path.exists(USER_DATA_FILE):
        stdscr.erase()
        stdscr.addstr("Existing user data found! Loading...", curses.color_pair(5))
        stdscr.refresh()
        with open(USER_DATA_FILE, 'rb') as f:
            user = pickle.load(f)
    else:
        stdscr.erase()
        stdscr.addstr("No existing user data found! Creating new user...", curses.color_pair(5))
        stdscr.refresh()
        user = userdata.UserData()
        with open(USER_DATA_FILE, 'wb') as f:
            pickle.dump(user, f)

    return user


def load_text(allowed_keys, length=50):
    return ''.join(random.choices(allowed_keys, k=length))


def wpm_test(stdscr):
    # load_text()
    allowed_keys = get_keys_to_practice(stdscr)
    target_text = load_text(allowed_keys)
    current_text = []
    wpm = 0
    start_time = time.time()

    # Stops get key from blocking so WPM decreases if we don't type
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.erase()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        # Stops get key from throwing exception now that we no longer block the call
        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            stdscr.nodelay(False)
            exit(0)
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    start_screen(stdscr)

    while True:
        wpm_test(stdscr)

        stdscr.addstr(2, 0, "Great Work! Press any key to continue...")
        key = stdscr.getkey()

        if ord(key) == 27:
            break


wrapper(main)
