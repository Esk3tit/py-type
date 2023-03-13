import curses
from curses import wrapper
import time
import string
import random


# from transformers import pipeline

def start_screen(stdscr):
    # Clear screen
    stdscr.erase()

    stdscr.addstr("PYTHON TYPING APP\n")
    stdscr.addstr("Press any key to start")
    stdscr.refresh()

    # Wait for next input (user needs to press any key)
    stdscr.getkey()


def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        stdscr.addstr(0, i, char, curses.color_pair(1) if char == correct_char else curses.color_pair(2))


def load_text():
    # generator = pipeline("text-generation", model="EleutherAI/gpt-neo-125M")
    # context = "Generate text using words with as many of the following letters as possible: e"
    # output = generator(context, max_length=50, do_sample=True, temperature=0.9)
    # print(output)
    # return output
    return ''.join(random.choices(' ' + 'e', k=20))


def wpm_test(stdscr):
    # load_text()
    target_text = load_text()
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
            break
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)

    while True:
        wpm_test(stdscr)

        stdscr.addstr(2, 0, "Great Work! Press any key to continue...")
        key = stdscr.getkey()

        if ord(key) == 27:
            break


wrapper(main)
