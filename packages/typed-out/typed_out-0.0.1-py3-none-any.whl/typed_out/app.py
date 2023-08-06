import curses
import os
import random
import time
from curses import wrapper
print(os.getcwd())

words = []
with open('common_word') as f:
    for line in f.readlines():
        words.append(line.lower().strip('\n'))

words = random.choices(words, k=20)


def main(stdscr):
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_RED)

    output = []
    current_word_str = ' '.join(words)
    start_time = time.time()
    while True:
        stdscr.clear()
        current_input_str = ''.join(output)

        if current_word_str != current_input_str:
            stdscr.addstr(0, 0, current_word_str, curses.A_DIM)
            if current_word_str.startswith(current_input_str):
                stdscr.addstr(0, 0, current_input_str, curses.A_BOLD)
            else:
                stdscr.addstr(0, 0, current_input_str, curses.color_pair(1))

            c = stdscr.getch()

            if c == curses.KEY_BACKSPACE:
                if output:
                    output.pop()
            else:
                if ord('A') <= c <= ord('z') or c == ord(' '):
                    output.append(chr(c))
        else:
            break

        stdscr.refresh()
    end_time = time.time()
    stdscr.addstr(0, 0, f"DONE, WPM: {(20/(end_time-start_time))*60}, total spend time {end_time-start_time}")
    stdscr.getch()


wrapper(main)