from maps.tiles import Tile
import chars.npc
import maps.fov
import maps.map
import constants.globals
import random
import curses

class Level:
    """ Generic Level class that contains a map and a list of npcs.
    """

    def __init__(self, x, y):
        self.level_map = maps.map.RandomRoomsMap(x, y, 7)
        self.objects = []
        self.fov = maps.fov.ShadowCast(self.level_map.tiles, 7)
        self.npcs = []
        self.generate_npcs()

    def draw_all(self, screen, player):
        """ Render everything in this level to the input screen.
        """

        # TODO: Maybe creating sight maps shouldn't happen when drawing to the
        # screen?

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
        """ Generate npcs for this level. Can be overriden by sub classes to
        generate the appropiate npcs.
        """

        npc_start_tile = self.level_map.get_empty_tile()

        npc = chars.npc.NPC(npc_start_tile, 'M', curses.color_pair(2))
        self.npcs.append(npc)

        
