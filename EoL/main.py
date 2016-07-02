import game.game as game
import curses

def main(screen):
    """ This is the games main loop.

    - screen: game screen accepted from curses.wrapper(main)
    """
    game.init_colors()
    
    # Turn off blinking cursor.
    curses.curs_set(0)
    
    main_game = game.LitDGame(80, 20, screen)
    main_game.draw_game()
    curses.doupdate()

    while(True):
        state = main_game.handle_input()
        if state == 'quit':
            break
        

# Run main. curses.wrapper() initializes noecho, cbreak and keypad(1)
if __name__ == '__main__':
    curses.wrapper(main)
