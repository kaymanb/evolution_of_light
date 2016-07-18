import maps.maps as maps
import curses

class Level:

    def __init__(self, x, y):
        self.level_map = maps.RandomRoomsMap(x, y, 7)
        self.objects = []

    def draw_all(self, screen):
        """ Render everything in this level to the input screen.
        """
        self.level_map.draw_map(screen)


