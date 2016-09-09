from games.game import EoLGame
from levels.level import Level
from games.errors import ColorsNotSupportedError
import constants.colors
import games.console as console
import constants.globals
import curses
import argparse

GAME_WIDTH = 80
GAME_HEIGHT = 20
CONSOLE_HEIGHT = 5

def main(screen):
    """ This is the games main loop.

    - screen: game screen accepted from curses.wrapper(main)
    """
    try:
        constants.colors.init_colors()
    except ColorsNotSupportedError:
        msg = "ERROR: To play EoL please open it in a terminal with color support."
        prompt = "Press any key to quit."
        display_message(msg, prompt)
        return

    msg = "Welcome to Evolution of Light!"
    prompt = "Press any key to begin."
    display_message(msg, prompt)

    # Turn off blinking cursor.
    curses.curs_set(0)

    main_game = EoLGame(GAME_WIDTH, GAME_HEIGHT, screen)
    console.init_console(0, GAME_HEIGHT + 1, GAME_WIDTH, CONSOLE_HEIGHT)
    console.STD.win.overlay(screen)

    main_game.draw_game() 
    console.STD.log("Welcome to EoL!")
    
    while(True):
        state = main_game.do_turn()
        curses.doupdate()
        if state == 'quit':
            break

def parse_arguments():
    """ Parse command line arguments and prepare constants.gloabals
    appropriately.
    """
    parser = argparse.ArgumentParser(description="Play Evolution of Light.")
    
    # Add argument for wizard mode.
    parser.add_argument("-w", "--wizard_mode",
                        action="store_true",
                        help="Start the game in Wizard Mode.")
    args = parser.parse_args()

    constants.globals.WIZARD_MODE = args.wizard_mode

def display_message(msg, prompt):
    win = curses.newwin(GAME_HEIGHT + CONSOLE_HEIGHT, GAME_WIDTH)

    msg_start_x = (GAME_WIDTH - len(msg)) // 2
    msg_start_y = (GAME_HEIGHT + CONSOLE_HEIGHT) // 2
    prompt_start_x = (GAME_WIDTH - len(prompt)) // 2

    win.addstr(msg_start_y, msg_start_x, msg)
    win.addstr(msg_start_y + 1, prompt_start_x, prompt)
    win.getch()
    win.erase()

# Run main. curses.wrapper() initializes noecho, cbreak and keypad(1)
if __name__ == '__main__':
    
    parse_arguments()
    
    curses.wrapper(main)
