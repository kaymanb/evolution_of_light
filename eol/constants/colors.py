import games.errors as errors
import curses

###                     ###
# Definitions for colors. # 
###                     ###
def init_colors():
   
    # TODO: Refactor this with a better message.
    # TODO: Add global constants for common colors instead of curses.color_pair
    if not curses.has_colors():
        raise errors.ColorsNotSupportedError("ERR") 

    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
