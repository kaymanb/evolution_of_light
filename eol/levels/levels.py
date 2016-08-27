from maps.fov import ShadowCast
from features.features import EmptyFeature
from chars.npc import NPC
from maps.tiles import Tile
import constants.globals
import maps.maps as maps
import random
import curses

class Level:

    def __init__(self, x, y):
        self.level_map = maps.RandomRoomsMap(x, y, 7)
        self.objects = []
        self.fov = ShadowCast(self.level_map.tiles, 7)
        self.npcs = []
        self.generate_npcs()

    def draw_all(self, screen, player):
        """ Render everything in this level to the input screen.
        """
 
        # Give player unbroken vision in wizard mode.
        if constants.globals.WIZARD_MODE:
            height = self.level_map.size_y
            width = self.level_map.size_x
            player.sight_map = [[1 for y in range(height)] for x in range(width)]
        else:
            player.sight_map = self.fov.calculate_fov(player.tile.x, player.tile.y)

        # Generate sight maps for all npcs.
        for npc in self.npcs:
            npc.sight_map = self.fov.calculate_fov(npc.tile.x, npc.tile.y)
        self.level_map.draw_map(screen, player)

    def generate_npcs(self):
        
        npc_start_tile = self.level_map.get_a_tile()

        npc = NPC(npc_start_tile, 'M', curses.color_pair(2))
        self.npcs.append(npc)

        
