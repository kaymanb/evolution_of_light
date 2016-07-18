from maps.maps import Tile
from features.glyphs import Glyph
from game.errors import InvalidMovementError
import curses

class Character(Glyph):
    """ Generic character class that defines an inventory, movement, basic
    combat and other essentials.
    """

    def __init__(self, tile, icon, color=curses.COLOR_WHITE):
        """ Create a character with the input glyph and color. 
        """
        super().__init__(icon, color) 
        self.tile = tile
        tile.char = self
        self.inventory = []
        

    def move(self, new_tile):
        """ Move this character to a new tile.
        """
        if (new_tile.blocks_movement()):
            raise InvalidMovementError("Tile Blocks Movement")
        
        self.tile.char = None
        new_tile.char = self
        self.tile = new_tile
    
            
    
