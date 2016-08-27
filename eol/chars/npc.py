from chars.char import Character
import games.errors as errors
import random
import curses

class NPC(Character):
    """ A generic NPC class. Contains several basic methods for how they should
    interact with the player.
    """

    def wander(self, level_map):
        """ NPC will wander around aimlessly. Each turn grabs a random tile
        around it and moves there. NPC will randomly attack it the player is
        standing next to it.
        """
        move_horz = random.randint(0, 1)
    
        #TODO: Refactor to be more efficent that getting until != 0
        distance = 0
        while distance == 0:
            distance = random.randint(-1, 1)
        
        if move_horz:
            new_tile = level_map.get_tile(self.tile.x + distance, self.tile.y)
        else:
            new_tile = level_map.get_tile(self.tile.x, self.tile.y + distance)

        try:
            self.move(new_tile)
        except errors.InvalidMovementError:
            self.wander(level_map)

