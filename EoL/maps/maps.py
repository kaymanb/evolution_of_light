from features.features import Wall, EmptyFeature
import curses


class LevelMap:

    def __init__(self, x, y):
        """ Create an x by y level map, completely filled with walls. 

        Tiles can be accessed using the .get_tile(x, y) method. 
        """
        self.map = [[ Tile(Wall()) for i in range(x)] for j in range(y)]
        self.rooms = []
   
    def get_tile(self, x, y):
        """ Returns the tile located at position (x, y) in the map
        """
        return self.map[x][y]

    def draw_map(self, screen):
        """ Draws the map to the input screen.
        """
        for x in range(len(self.map)):
            for y in range(len(self.map[0])):
                tile = self.get_tile(0, 0)
                screen.addstr(y, x, tile.feature.sprite)

        # Add these changes to the screen, but wait for doupdate() to render.
        screen.noutrefresh()

class Tile:

#TODO: Add other variables to tile.
    
    def __init__(self, feature = EmptyFeature()):
        """ Creates a tile at position (x, y). By default this tile will be a
        wall.
        """
        self.feature = feature

