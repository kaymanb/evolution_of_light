import curses

###                     ###
# Definitions for colors. # 
###                     ###
def init_colors():
    curses.init_pair(1, curses.COLOR_YELLOW, 0)
    curses.init_pair(2, curses.COLOR_GREEN, 0)
