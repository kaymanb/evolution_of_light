from features.feature import Feature
from maps.tiles import Tile

class ShadowCast:
    """ An implementation of ShadowCasting FOV. 
    
    Contains methods to construct a light_map of values in [0, 1] representing
    the brightness of the corresponging (x, y) tile in the map, based on the
    position on the inital input tile. The initial light_map is given all
    values of 0 representing comlete darkness.

    Shadow Casting works as follows. The area in a given radius around the
    inital tile is divided into 8 octants, as if you were slicing it like a
    pizza. 
                                    \  |  /
                                     \ | /
                                   ___\|/___
                                      /|\
                                     / | \
                                    /  |  \
    
    To calculate brightness values, starting at the inital tile, each
    octant is scanned line by line, begining with the smallest line right next
    to the inital tile. As the line is scanned, empty tiles are lit up with a
    brightness according to how close they are to the initials tile. If a tile
    that blocks light is reached, the scan makes a recursive call to scan the
    next line, but stopping when the scan reaches the slop of the previously
    blocked tile. The original scan then skips over any more blocking tiles
    until it reaches one that isn't blocked. At this point it continues
    scanning but records the slope that it startup up at. When it reaches the
    end of the row another recursive call is made, this time starting at the
    slope that was recorded at the end of the section of blocked tiles.

    This process is repeated for each of the 8 octants, creating a total FOV of
    a given radius.

                                 \->    ->|
                                  \->   ->|
                                   \->  ->|
                                    \->#->|
                                     \--->|
                                      \-->|
                                       \->|

    As a result of this algorithm, each tile that is lit up is only ever
    scanned once, and moreover, tiles that should remain dark are never scanned
    at all. By recording the slope of where the scan hits a blocked tile, the
    algorithm "casts a shadow" behind it, maintaining the slope of the shadow
    relative to the initial tile. 
    """

    def __init__(self, tiles, radius):
        self.tile_map = tiles
        self.width = len(tiles)
        self.height = len(tiles[0])
        self.radius = radius
        
        # Mulitpliers for transforming coords into the 8 octants.
        self.oct = [[1, 0, 0, -1, -1, 0, 0, 1],
                    [0, 1, -1, 0, 0, -1, 1, 0],
                    [0, 1, 1, 0, 0, -1, -1, 0],
                    [1, 0, 0, 1, -1, 0, 0, -1]]
        
        # Set x and y that will be used later as center for FOV
        self.x = None
        self.y = None
        self.light_map = None

    def calculate_fov(self, init_x, init_y):
        """Returns a map of real numbers in [0, 1], which represent the amount
        of light that a tile should have, 0 being black, 1 being completely
        lit. These are calculated based on the distance from the inital tile,
        whos brightness value will always be 1.
        """

        self.x = init_x
        self.y = init_y
        self.light_map = [[0 for i in range(self.height)] for j in range(self.width)]

        for i in range(8):
            self.cast_light(1.0, 0.0, 1, self.oct[0][i], self.oct[1][i], 
                                            self.oct[2][i], self.oct[3][i])
        
        # Always set the inital tile to be lit.
        self.light_map[init_x][init_y] = 1
        return self.light_map

    def cast_light(self, start_slope, end_slope, row, xx, xy, yx, yy):
        """ Sets the values of the light_map to the appropiate brightness,
        scanning from the start_slope to the end_slope in a given row. Values
        xx, xy, yx, yy are multipliers that transform the delta values and scan
        direction to match the a certain octant. 
        """
        if start_slope < end_slope:
            return
        # Boolean for scanning a sequence of blocked tiles.
        blocked = False
        distance = row
        radius_squared = self.radius * self.radius
        new_start = 0
        
        while distance <= self.radius and not blocked:
            dy = -distance
            for dx in range(-distance, 1):
                
                # Calculate current x and y and slopes.
                cx = self.x + dx * xx + dy * xy
                cy = self.y + dx * yx + dy * yy
                left_slope = (dx - 0.5) / (dy + 0.5)
                right_slope = (dx + 0.5) / (dy - 0.5)
                
                # If the current tile is not within the map, or the slope at
                # the current tile is outside where the start slope should be,
                # move on to the next tile.
                if not (cx >= 0 and cy >= 0 and cx < self.width and cy <
                    self.height) or start_slope < right_slope:
                    continue
                elif end_slope > left_slope:
                    break

                # Use Pythagreom theorem to tell if the current tile is inside
                # the radius of fov.
                if dx * dx + dy * dy < radius_squared:
                    brightness = 1 - (( dx * dx + dy * dy) / radius_squared)
                    self.light_map[cx][cy] = brightness

                # If the previous cell scanned was a blocking one.
                if blocked:

                    # In a sequence of blocking, so just move to next tile.
                    if self.tile_map[cx][cy].feature.blocks_light:
                        new_start = right_slope
                        continue
                    else:
                        blocked = False
                        start_slope = new_start
                else:

                    # Hit a light blocking feature inside the fov.
                    if (self.tile_map[cx][cy].feature.blocks_light 
                                                    and distance < self.radius):
                        blocked = True
                        self.cast_light(start_slope, left_slope, distance + 1, 
                                                                    xx, xy, yx, yy)
                        new_start = right_slope
            
            # Proceed to the next row.            
            distance += 1
        
