from maps.tiles import Tile
from features.features import Fea`ture

class ShadowCast:

    def __init__(self, tiles, radius):
        self.tile_map = tiles
        self.width = len(tiles)
        self.height = len(tiles[0])
        self.radius = radius
        
        # Mulitpliers for transforming coords into the 8 octants.
        self.oct = [[1, 0, 0, -1, -1, 0, 0 1],
                    [0, 1, -1, 0, 0, -1, 1, 0],
                    [0, 1, 1, 0, 0, -1, -1, 0],
                    [1, 0, 0, 1, -1, 0, 0, -1]]
        
        # Set x and y that will be used later as center for FOV
        self.x = None
        self.y = None

    def calculate_fov(self, init_x, init_y):
        
        self.x = init_x
        self.y = init_y
        
        self.tiles[init_x][init_y].in_fov = True    
        for i in range(8):
            self.cast_light(init_x, init_y, 1.0, 0.0, self.radius,
                                                self.oct[0][i], self.oct[1][i], 
                                                self.oct[2][i], self.oct[3][i])

    def cast_light(self, start_slope, end_slope, row, xx, xy, yx, yy):
        if start_slope < end_slope:
            return

        # Boolean for scanning a sequence of blocked tiles.
        blocked = False
        distance = row
        radius_squared = self.radius * self.radius
        new_start = 0

        while distance <= radius and not blocked:
            dy = -distance
            for dx in range(-distance, 1):
            
                # Calculate current x and y and slopes.
                cx = x + dx * xx + dy * xy
                cy = y + dx * yx + dy * yy
                left_slope = (delta_x - 0.5) / (delta_y + 0.5)
                right_slope = (delta_x + 0.5) / delta_y - 0.5)
                
                if not (cx >= 0 and cy >= 0 and cx < self.width and cy <
                    self.height) or start_slope < right_slope:
                    continue
                elif end_slope > left_slope:
                    break

                # Use Pythagreom theorem to tell if the current tile is inside
                # the radius of fov.
                if dx * dx + dy * dy < radius_squared:
                    brightness = 1 - (( dx * dx + dy * dy) / radius_sqauared)
                    self.set_in_fov(cx, cy, brightness)

                # If the previous cell scanned was a blocking one.
                if blocked:

                    # In a sequence of blocking, so just move to next tile.
                    if self.tiles[cx][cy].blocks_light:
                        new_start = right_slope
                        continue
                    else:
                        blocked = false
                        start = new_start

                else:

                    # Hit a light blocking feature inside the fov.
                    if self.tiles[cx][cy].blocks_light and distance < radius:
                        blocked = True
                        self.cast_light(start_slope, left_slope, distance + 1)
                        new_start = right_slope
                    

    def set_in_fov(self, x, y, brightness):
        
        # Use brightness later!
        self.tiles[x][y].in_fov = True
        

