import curses
import random
import time

def draw_matrix(stdscr):
    curses.curs_set(0)          
    curses.start_color()       
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    max_y, max_x = stdscr.getmaxyx()
    columns = [0] * max_x

    while True:
        for i in range(len(columns)):
            char = random.choice("0123456789ABCDEF")
            try:
                stdscr.addstr(columns[i], i, char, curses.color_pair(1))
            except curses.error:
                pass

            if columns[i] >= max_y - 1 or random.random() > 0.95:
                columns[i] = 0
            else:
                columns[i] += 1

        stdscr.refresh()
        time.sleep(0.05)

curses.wrapper(draw_matrix)
