from maps.maps import Tile
from levels.levels import Level
from chars.chars import Character
from game.errors import InvalidMovementError
import curses

MOVEMENT_KEYS  = frozenset([curses.KEY_UP, curses.KEY_DOWN,
                            curses.KEY_LEFT, curses.KEY_RIGHT])
QUIT_KEY = ord('q')

class InputHandler:
    """ Class for handling user input. Tells the player and the screen what
    action to take based on which key is pressed.
    """

    def __init__(self, screen, level, player):
        self.game_screen = screen
        self.game_level = level
        self.game_player = player
            
    def handle_input(self, key):
        """ Make changes and trigger events based on input key.
        """
        try:
            if key in MOVEMENT_KEYS:
                old_tile = self.game_player.tile
                new_tile = self.handle_movement(key)
                self.game_player.move(new_tile)
                return 'player_moved'
            elif key == QUIT_KEY:
                curses.endwin()
                return 'quit'
        except InvalidMovementError:
            pass
    
    def handle_movement(self, key):
        tile_map = self.game_level.level_map
        tile = self.game_player.tile
        x = None
        y = None
        if key == curses.KEY_UP:
            x = tile.x
            y = tile.y - 1
        elif key == curses.KEY_DOWN:
            x = tile.x
            y = tile.y + 1
        elif key == curses.KEY_LEFT:
            x = tile.x - 1
            y = tile.y
        elif key == curses.KEY_RIGHT:
            x = tile.x + 1
            y = tile.y 
        return tile_map.get_tile(x, y)
