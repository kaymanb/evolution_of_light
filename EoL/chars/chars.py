from maps.maps import Tile
from game.errors import InvalidMovementError
import curses

class Character:
    """ Generic character class that defines an inventory, movement, basic
    combat and other essentials.
    """

    def __init__(self, tile, glyph, color=curses.COLOR_WHITE):
        """ Create a character with the input glyph and color. 
        """
        
        self.tile = tile
        self.glyph = glyph
        self.color = color
        self.inventory = []
        

    def move(self, new_tile):
        """ Move this character to a new tile.
        """
        if (new_tile.blocks_movement()):
            raise InvalidMovementError("Tile Blocks Movement")
        
        self.tile.char = None
        new_tile.char = self
        self.tile = new_tile
    
            
    
