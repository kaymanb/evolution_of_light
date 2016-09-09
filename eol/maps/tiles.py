from features.glyphs import Glyph
import features.feature as feat
import curses

class Tile:
    """ Tile object that sits inside a map.

    Holds a single feature and a single character. 
    """
#TODO: Add other variables to tile.
    
    def __init__(self, x, y, feature = feat.EmptyFeature()):
        """ Create a tile at position (x, y). By default this tile will be a
        wall.
        """
        self.x = x
        self.y = y
        self.feature = feature
        self.char = None
        self.explored = False
        self.brightness = 0

    def inspect(self):
        """ Returns a string describing the tile.
        """
        return self.feature.inspect()

    def draw_tile(self, screen):
        """ Draws the tile to the screen.
        """
        glyph = self.get_top_glyph()
        screen.addstr(self.y, self.x, glyph.icon, glyph.color)

    def get_top_glyph(self):
        """ Returns the glyph that should appear when this tile is drawn to the
        screen.

        Note that this can be a feature, a character, or even just a plain
        glyph object.
        """
        if self.brightness > 0:
            if self.char is not None:
                return self.char
            return self.feature
        else:
            if self.explored:
                if isinstance(self.feature, feat.Explorable):
                    return self.feature
            return Glyph(" ", curses.color_pair(0))



class Rectangle:
    """ A Rectangluar Prism """

    def __init__(self, x, y, width, height):
        """ Create a rectangle with top left corner at (x, y) and with width and
        height w and h respectivly.

        (x1, y1) --- (x2, y1)
           |            |
           |            |
        (x1, y2) --- (x2, y2)
        """
        self.x1 = x
        self.y1 = y

        self.x2 = x + width
        self.y2 = y + height

    def get_center(self):
        """ Return the approximate (rounded down) coordinates of the tile in
        the center of the rectangle.
        """
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return (center_x, center_y)

    def intersects(self, other):
        """ Returns whetehr another rectangle intersects with this one. This
        method considers rectangles that are just "touching" (ie. have an edge
        that exactly overlaps) as intersecting.
        """
    
        # The equals in the following inequalities is the condition for
        # "touching" rectangles. 
        #
        # Also, notice that each inequality takes care of a case where the
        # other rectangle in North/East/South/West of this one.
        bool_x = self.x1 <= other.x2 and other.x1 <= self.x2
        bool_y = self.y1 <= other.y2 and other.y1 <= self.y2
        return bool_x and bool_y

