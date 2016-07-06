from levels.levels import Level
import curses

class InvalidMovementError(Exception):
    
    def __init__(self):
        pass

    def __str__(self):
        return 'Attempted to move onto a tile that blocks movement'

def init_colors():
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)

class LitDGame:
    
    def __init__(self, x, y, screen):
        
        self.size_x = x
        self.size_y = y
        self.levels = [Level(x, y)]
        self.current_level = self.levels[0]
        
        start_tile = self.current_level.

        self.screen = screen
        
    def draw_game(self):
        self.current_level.draw_all(self.screen)
    
    # TODO: Move input logic into it's own class.

    def handle_input(self):
        key = self.screen.getch()
        try:
            if key == ord('q'):
                curses.endwin()
                return 'quit'
        except InvalidMovementError:
            pass
        
        self.draw_game()
        
        # Render changes to the screen.
        curses.doupdate()


