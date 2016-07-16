from features.features import Feature, Wall, EmptyFeature
import random
import curses


class LevelMap:
    

    def __init__(self, x, y):
        """ Create an x by y level map, completely filled with walls. 

        Tiles can be accessed using the .get_tile(x, y) method. 
        """
        self.size_x = x
        self.size_y = y
        self.tiles = [[ Tile(j, i, Wall()) for i in range(y)] for j in range(x)]

    def get_tile(self, x, y):
        """ Returns the tile located at position (x, y) in the map
        """
        return self.tiles[x][y]

    def draw_map(self, screen):
        """ Draws the map to the input screen.
        """
        for x in range(len(self.tiles)):
            for y in range(len(self.tiles[0])):
                tile = self.tiles[x][y]
                screen.addstr(y, x, tile.get_top_glyph())

        # Add these changes to the screen, but wait for doupdate() to render.
        screen.noutrefresh()

class RoomsMap(LevelMap):

    MAX_ROOM_WIDTH = 15
    MAX_ROOM_HEIGHT = 10

    def __init__(self, x, y):
        """ Create a map with rooms.
        """
        super().__init__(x, y)
        self.rooms = []

    def add_room(self, room):
        """ Add the input room to the map.
        """
        self.rooms.append(room)
        for (x, y) in room.list_floorspace():
            self.tiles[x][y] = Tile(x, y)

class RandomRoomsMap(RoomsMap):

    def __init__(self, x, y, num_rooms):
        """ Creates a map with a given amount of randomly generated rooms.
        """
        super().__init__(x, y)
        self.generate_rooms(num_rooms)
                    
    def generate_rooms(self, num_rooms):
        """ Populate the map with a given number of randomly generated rooms.
        """
        for _ in range(num_rooms):
            new_room = None
            valid_room = False
            
            while not valid_room:
                new_room = self.create_random_room()
                result = self.check_intersections(new_room)
                valid_room = result
        
            self.add_room(new_room)

    def create_random_room(self):
        """ Create and return a random sized room at a random location.
        """
        width = random.randint(3, self.MAX_ROOM_WIDTH)
        height = random.randint(3, self.MAX_ROOM_HEIGHT)

        # We want the room we create to have walls all the way around it, hence
        # the added 1's in these four statements.
        farthest_x = self.size_x - width - 1
        farthest_y = self.size_y - height - 1
        x = random.randint(1, farthest_x)
        y = random.randint(1, farthest_y)
        return Room(x, y, width, height)
       
    def check_intersections(self, new_room):
        """ Return whether a given room intersects with any existing rooms in
        the map.
        """
        for room in self.rooms:
            if new_room.intersects(room):
                return False
        return True
            
class Tile:

#TODO: Add other variables to tile.
    
    def __init__(self, x, y, feature = EmptyFeature()):
        """ Create a tile at position (x, y). By default this tile will be a
        wall.
        """
        self.x = x
        self.y = y
        self.feature = feature
        self.char = None

    def blocks_movement(self):
        """ Return whether this tile blocks movement
        """
        return self.feature.blocks_movement
    
    def get_top_glyph(self):
        """ Returns the glyph that should appear when this tile is drawn to the
        screen.
        """
        if(self.char is not None):
            return self.char.glyph
        return self.feature.sprite

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

class Room(Rectangle):
    """ A room.
    """
    
    floor_feature = EmptyFeature()

    def list_floorspace(self):
        """Return a list of all coordinate pairs that are in this room.
        """

        x_coords = [self.x1 + i for i in range(self.x2 - self.x1)]
        y_coords = [self.y1 + j for j in range(self.y2 - self.y1)]

        return [(x, y) for x in x_coords for y in y_coords]

