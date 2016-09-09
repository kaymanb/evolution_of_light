from maps.tiles import Tile
from chars.char import Character
from games.errors import InvalidMovementError
import features.feature as feat
import games.console as console
import features.stairs
import curses

MOVEMENT_KEYS  = frozenset([curses.KEY_UP, curses.KEY_DOWN,
                            curses.KEY_LEFT, curses.KEY_RIGHT])
QUIT = ord('q')
CLIMB_DOWN = ord('<')
CLIMB_UP = ord('>')
INSPECT = ord(';')

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
            elif key == INSPECT:
                console.STD.log("You see " + self.player.tile.inspect() + ".")

            elif key == CLIMB_DOWN:
                if isinstance(self.player.tile.feature, features.stairs.StairwayDown):
                    console.STD.log("You climb down the staircase...")
                    self.handle_staircase(self.player.tile.feature)
           
            elif key == CLIMB_UP:
                console.STD.log("You climb up the staircase...")
                if isinstance(self.player.tile.feature, features.stairs.StairwayUp):
                    self.handle_staircase(self.player.tile.feature)
        
            elif key == QUIT:
                msg = "Are you sure you want to quit? Press 'y' to confirm."
                console.STD.log(msg)
                confirm = self.game.screen.getch()
                if confirm == ord('y'):
                    curses.endwin()
                    return 'quit'
                else:
                    console.STD.log("You reluctantly keep playing.")
        except InvalidMovementError:
            curses.beep()
            pass
    
    def handle_movement(self, key):
        """ Returns a new tile for the player to move to, based on which key
            was pressed.
        """
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
        """ Helper function for moving a player up or down a staircase. Creates
        the new levels stack and then moves the player accordingly.
        """

        (levels, index) = staircase.climb(self.game.levels, self.level,
                                                            self.player)
        self.game.levels = levels
        self.game.current_level = levels[index]
