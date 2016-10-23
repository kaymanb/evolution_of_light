from features.glyphs import Glyph
import games.errors as errors
import games.console as console
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
        self.inventory =[]
        
        # Declare character attributes.
        self.name = "Aht Sihmbol"
        self.title = "the Lost"
        self.max_hp = 10
        self.hp = 10
        self.ac = 0

        self.tile.explored = True
        self.sight_map = None # Maybe set to empty object instead of None?      

    def move(self, new_tile):
        """ Move this character to a new tile.
        """
        
        if new_tile.char is not None:
            console.STD.log("Someone is already standing there.")
            return
            #raise InvalidMovementError("That tile looks a bit small for two.")

        if (new_tile.feature.blocks_movement):
            raise errors.InvalidMovementError("Tile Blocks Movement")
        
        self.tile.char = None
        new_tile.char = self
        self.tile = new_tile

        self.tile.explored = True
    
    def can_see(self, tile):
        """ Returns whether this character can see the input tile.
        """
        return self.sight_map[tile.x][tile.y] > 0

class Player(Character):
    """ The games hero, a player.
    """

    def __init__(self, tile, icon, color=curses.COLOR_WHITE):
        """ Create a player.
        """
        super().__init__(tile, icon, color)
        self.turns = 0
