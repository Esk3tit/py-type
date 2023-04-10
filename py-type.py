import curses
from curses import wrapper
import time
import string
import random
import os
import userdata
import pickle

USER_DATA_FILE = 'user.dat'
PROMPT_LENGTH = {
    "1": 50,
    "2": 100,
    "3": 300
}

SPECIAL_CHARS = {
    ord(' '): '\u2423',
    ord('\n'): '\u21b5',
    ord('\r'): '\u21b5'
}


def start_screen(stdscr):
    # Clear screen
    stdscr.erase()

    stdscr.addstr("PYTHON TYPING APP\n")
    stdscr.addstr("Press any key to start")
    stdscr.refresh()

    # Wait for next input (user needs to press any key)
    stdscr.getkey()


def display_text(stdscr, target, current, mistakes, wpm=0):
    # Add special unicode symbol representations for spaces and new lines
    for char in target:
        target_char = char
        if ord(char) in SPECIAL_CHARS:
            target_char = SPECIAL_CHARS[ord(char)]

        stdscr.addstr(target_char)

    stdscr.addstr(f"\nWPM: {wpm}")

    for i, char in enumerate(current):
        char_to_scr = char
        correct_char = target[i]
        color = curses.color_pair(3)
        if char == correct_char and correct_char == ' ':
            color = curses.color_pair(4)
        elif char == correct_char and mistakes[i]:
            color = curses.color_pair(6)
        elif char == correct_char:
            color = curses.color_pair(1)
        else:
            color = curses.color_pair(2)
            char_to_scr = correct_char

        stdscr.addstr(0, i, char_to_scr, color)


def display_stats(stdscr, user):
    info_color = curses.color_pair(5)
    stdscr.addstr("\nSTATS\n", info_color)
    stdscr.addstr(f"Max Words Per Minute (WPM): {user.max_wpm}\n", info_color)
    stdscr.addstr(f"Average Words Per Minute (WPM): {user.avg_wpm()}\n", info_color)
    stdscr.addstr(f"Average Accuracy: {user.avg_accuracy()}\n", info_color)


def get_keys_to_practice(stdscr):
    keys_set = set()
    allowed_keys = []

    while True:
        stdscr.erase()
        stdscr.addstr("Enter the letters you want in the typing prompt (no delimiters, ex. 'abCde./,')\n")
        stdscr.addstr("Enter ESC to stop entering keys\n")
        stdscr.addstr(f"Current keys: {' '.join([key if ord(key) not in SPECIAL_CHARS else SPECIAL_CHARS[ord(key)] for key in allowed_keys])}")
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


def get_length(stdscr):
    while True:
        stdscr.erase()
        stdscr.addstr("Select the length of the text prompt by entering the number in parentheses\n")
        for key, length in PROMPT_LENGTH.items():
            stdscr.addstr(f"({key}) {length} characters\n")
        stdscr.refresh()
        # Maybe custom amount in future but switching back to normal term breaks docker terminal...

        key = stdscr.getkey()

        if key in PROMPT_LENGTH:
            break

    return PROMPT_LENGTH[key]


def load_user(stdscr):
    user = userdata.UserData()
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

    return user


def save_user(stdscr, user):
    stdscr.erase()
    stdscr.addstr("Saving user data to disk...", curses.color_pair(5))
    stdscr.refresh()
    with open(USER_DATA_FILE, 'wb') as f:
        pickle.dump(user, f)


def load_text(allowed_keys, length=50):
    return ''.join(random.choices(allowed_keys, k=length))


def calculate_accuracy(mistakes, prompt_length):
    return int(((prompt_length - sum(mistakes)) / prompt_length) * 100)


def wpm_test(stdscr, user):
    allowed_keys = get_keys_to_practice(stdscr)

    if not allowed_keys:
        exit(0)

    prompt_length = get_length(stdscr)
    target_text = load_text(allowed_keys, prompt_length)
    current_text = []
    mistakes = [False] * prompt_length
    cursor_idx = 0
    wpm = 0
    start_time = time.time()

    # Stops get key from blocking so WPM decreases if we don't type
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.erase()
        display_text(stdscr, target_text, current_text, mistakes, wpm)
        stdscr.refresh()

        if len("".join(current_text)) == len(target_text):
            stdscr.nodelay(False)

            # Update user stats after test finishes
            user.wpm_sum += wpm
            user.max_wpm = max(user.max_wpm, wpm)
            user.num_trials += 1
            user.accuracy_sum += calculate_accuracy(mistakes, prompt_length)

            break

        # Stops get key from throwing exception now that we no longer block the call
        try:
            key = stdscr.getkey()
        except:
            continue

        try:
            if ord(key) == 27:
                stdscr.nodelay(False)
                exit(0)
        except:
            pass

        if key in ("KEY_BACKSPACE", "\b", "\x7f", 263):
            if len(current_text) > 0:
                current_text.pop()
                cursor_idx -= 1
        elif len(current_text) < len(target_text):
            if key != target_text[cursor_idx]:
                mistakes[cursor_idx] = True
            current_text.append(key)
            cursor_idx += 1


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    start_screen(stdscr)

    # Save and read only once per session, not once per game/wpm test
    # so it is in main instead of wpm_test
    user = load_user(stdscr)

    while True:
        wpm_test(stdscr, user)
        display_stats(stdscr, user)

        stdscr.addstr(6, 0, "Great Work! Press any key to continue... (ESC to exit)")
        key = stdscr.getkey()

        if ord(key) == 27:
            break

    save_user(stdscr, user)


wrapper(main)
