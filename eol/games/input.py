from maps.tiles import Tile
from levels.level import Level
from chars.char import Character
from games.errors import InvalidMovementError
import features.feature as feat
import features.stairs
import curses

MOVEMENT_KEYS  = frozenset([curses.KEY_UP, curses.KEY_DOWN,
                            curses.KEY_LEFT, curses.KEY_RIGHT])
QUIT = ord('q')
CLIMB_DOWN = ord('<')
CLIMB_UP = ord('>')

class InputHandler:
    """ Class for handling user input. Tells the player and the screen what
    action to take based on which key is pressed.
    """

    def __init__(self, game):
        self.game = game
        self.level = game.current_level
        self.player = game.player
            
    def handle_input(self, key):
        """ Make changes and trigger events based on input key.
        """
        try:
            if key in MOVEMENT_KEYS:
                old_tile = self.player.tile
                new_tile = self.handle_movement(key)
                self.player.move(new_tile)
                return 'player_moved'
            
            elif key == CLIMB_DOWN:
                if isinstance(self.player.tile.feature, features.stairs.StairwayDown):
                    self.handle_staircase(self.player.tile.feature)
           
            elif key == CLIMB_UP:
                if isinstance(self.player.tile.feature, features.stairs.StairwayUp):
                    self.handle_staircase(self.player.tile.feature)
        
            elif key == QUIT:
                curses.endwin()
                return 'quit'
        except InvalidMovementError:
            pass
    
    def handle_movement(self, key):
        tile_map = self.level.level_map
        tile = self.player.tile
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

    def handle_staircase(self, staircase):
        (levels, index) = staircase.climb(self.game.levels, self.level,
                                                            self.player)
        self.game.levels = levels
        self.game.current_level = levels[index]
