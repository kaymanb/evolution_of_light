from maps.fov import ShadowCast
from features.features import EmptyFeature
from chars.npc import NPC
from maps.tiles import Tile
import maps.maps as maps
import random
import curses

class Level:

    def __init__(self, x, y):
        self.level_map = maps.RandomRoomsMap(x, y, 7)
        self.objects = []
        self.fov = ShadowCast(self.level_map.tiles, 5)
        self.npcs = []
        self.generate_npcs()

    def draw_all(self, screen, player):
        """ Render everything in this level to the input screen.
        """
        light_map = self.fov.calculate_fov(player.tile.x, player.tile.y)
        self.level_map.draw_map(screen, light_map)

    def generate_npcs(self):
        
        npc_start_tile = self.level_map.get_a_tile()

        npc = NPC(npc_start_tile, 'M', curses.color_pair(2))
        self.npcs.append(npc)


