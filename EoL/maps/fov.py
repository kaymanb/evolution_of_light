from maps.tiles import Tile
from features.features import Feature

class ShadowCast:

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
                        star_slope = new_start
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
        
