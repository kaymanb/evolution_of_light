from maps.tiles import Tile
import features.feature as feat
import features.stairs
import maps.fov
import random
import curses
import math


class LevelMap:
    """ Generic Map that the game is played on. Contains methods for accessing
    tiles and drawing the map to a screen.
    """

    def __init__(self, x, y):
        """ Create an x by y level map, completely filled with walls. 

        Tiles can be accessed using the .get_tile(x, y) method. 
        """
        self.size_x = x
        self.size_y = y
        self.tiles = [[ Tile(j, i, feat.Wall()) for i in range(y)] for j in range(x)]

    def get_tile(self, x, y):
        """ Returns the tile located at position (x, y) in the map
        """
        return self.tiles[x][y]

    def get_empty_tile(self):
        """ Returns an empty tile in the map.
        """
        for row in self.tiles:
            for tile in row:
                if isinstance(feat.EmptyFeature, tile.feature) and tile.char == None:
                    return tile

    def draw_map(self, screen, char):
        """ Draws the map to the input screen, as though it is from the
        perspective of the input char.
        """
        for row in self.tiles:
            for tile in row:
                tile.brightness = char.sight_map[tile.x][tile.y]

                # Mark tiles that have been seen as explored.
                if tile.brightness > 0:
                    tile.explored = True

                tile.draw_tile(screen)
 
class RoomsMap(LevelMap):
    """ A Map filled with rooms. Contains methods for creating rooms along with
    tunnels to connect them.
    """

    MAX_ROOM_WIDTH = 15
    MAX_ROOM_HEIGHT = 10
    MIN_ROOM_WIDTH = 3
    MIN_ROOM_HEIGHT = 3

    def __init__(self, x, y):
        """ Create a map with rooms.
        """
        super().__init__(x, y)
        self.rooms = []
    
    def get_empty_tile(self):
        """ Get an empty tile inside of a random room
        """
        room_index = random.randint(0, len(self.rooms) - 1)
        (x, y) = self.rooms[room_index].list_floorspace()[0]
        return self.tiles[x][y]

    def add_room(self, room):
        """ Add the input room to the map.
        """
        self.rooms.append(room)
        for (x, y) in room.list_floorspace():
            self.tiles[x][y] = Tile(x, y)

    
    def connect_rooms(self, room_a, room_b):
        """ Connects room_a to room_b VIA a tunnel.
        """
        center_a = room_a.get_center()
        center_b = room_b.get_center()
        
        self.create_diagonal_tunnel(center_a[0], center_a[1],
                                    center_b[0], center_b[1])

        # Connect with horizontal/vertical tunnels
        #self.create_horz_tunnel(center_a[0], center_b[0], center_a[1])
        #self.create_vert_tunnel(center_a[1], center_b[1], center_b[0])
    
    def create_diagonal_tunnel(self, x1, y1, x2, y2):
        """ Create a diagonal tunnel from the (x1, y1) tile in the map
        the the (x2, y2) tile.
        """
                
        dif_x = x2 - x1
        dif_y = y2 - y1
        if dif_x == 0:
            return self.create_vert_tunnel(y1, y2, x1)
        if dif_y == 0:
            return self.create_horz_tunnel(x1, x2, y1)

        step_h = dif_x / abs(dif_y)
        step_v = dif_y / abs(dif_x)
        
        step_h = math.floor(step_h) if step_h < 0 else math.ceil(step_h)
        step_v = math.floor(step_v) if step_v < 0 else math.ceil(step_v)
        
        step_dir_h = -1 if step_h < 0 else 1
        step_dir_v = -1 if step_v < 0 else 1

        for x in range(x1 + step_dir_h, x1 + step_h + step_dir_h, step_dir_h):
            self.tiles[x][y1].feature = feat.EmptyFeature()

        for y in range(y1 + step_dir_v, y1 + step_v + step_dir_v, step_dir_v):
            self.tiles[x1 + step_h][y].feature = feat.EmptyFeature()

        return self.create_diagonal_tunnel(x1 + step_h, y1 + step_v, x2, y2)
    
    def create_horz_tunnel(self, x1, x2, y):
        """ Create a horizontal tunnel from the (x1, y) tile to (x2, y).
        """
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].feature = feat.EmptyFeature()

    def create_vert_tunnel(self, y1, y2, x):
        """ Create  vertical tunnel from the (x, y1) tile to (x, y2).
        """
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].feature = feat.EmptyFeature()

class RandomRoomsMap(RoomsMap):
    """ A map with randomly generated rooms. Constructor takes in the number of
    rooms to generate as input.
    """

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
            
            # Connect this room the last room that was added.
            self.connect_rooms(new_room, self.rooms[len(self.rooms) - 2])

        # Add a staircase to the last room that was generated.
        room = self.rooms[len(self.rooms) - 1]
        (x, y) = room.get_center()
        tile = self.tiles[x][y]
        tile.feature = features.stairs.StairwayDown()

    def create_random_room(self):
        """ Create and return a random sized room at a random location.
        """
        width = random.randint(self.MIN_ROOM_WIDTH, self.MAX_ROOM_WIDTH)
        height = random.randint(self.MIN_ROOM_HEIGHT, self.MAX_ROOM_HEIGHT)

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
    
class Room(maps.tiles.Rectangle):
    """ A room.
    """
    
    floor_feature = feat.EmptyFeature()

    def list_floorspace(self):
        """Return a list of all coordinate pairs that are in this room.
        """

        x_coords = [self.x1 + i for i in range(self.x2 - self.x1)]
        y_coords = [self.y1 + j for j in range(self.y2 - self.y1)]

        return [(x, y) for x in x_coords for y in y_coords]

