from games.game import EoLGame
from levels.level import Level
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
    constants.colors.init_colors()


    # Turn off blinking cursor.
    curses.curs_set(0)
    main_game = EoLGame(GAME_WIDTH, GAME_HEIGHT, screen)
    console.init_console(0, GAME_HEIGHT + 1, GAME_WIDTH, CONSOLE_HEIGHT)

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



# Run main. curses.wrapper() initializes noecho, cbreak and keypad(1)
if __name__ == '__main__':
    
    parse_arguments()
    
    curses.wrapper(main)
