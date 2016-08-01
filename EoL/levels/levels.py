from maps.fov import ShadowCast
import maps.maps as maps
import curses

class Level:

    def __init__(self, x, y):
        self.level_map = maps.RandomRoomsMap(x, y, 7)
        self.objects = []
        self.fov = ShadowCast(self.level_map.tiles, 10)

    def draw_all(self, screen, player):
        """ Render everything in this level to the input screen.
        """
        light_map = self.fov.calculate_fov(player.tile.x, player.tile.y)
        self.level_map.draw_map(screen, light_map)


