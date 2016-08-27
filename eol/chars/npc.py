from chars.chars import Character
from game.errors import InvalidMovementError
import random
import curses

class NPC(Character):

    def wander(self, level_map):
        move_horz = random.randint(0, 1)
    
        #TODO: Refactor this with speed
        distance = 0
        while distance == 0:
            distance = random.randint(-1, 1)
        
        if move_horz:
            new_tile = level_map.get_tile(self.tile.x + distance, self.tile.y)
        else:
            new_tile = level_map.get_tile(self.tile.x, self.tile.y + distance)

        try:
            self.move(new_tile)
        except InvalidMovementError:
            self.wander(level_map)

