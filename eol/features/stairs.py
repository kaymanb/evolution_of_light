from features.feature import Feature
import levels.level as lvls
import features.stairs

class Stairway(Feature):
    """ A stairway.
    """

    blocks_light = False
    blocks_movement = False
    
    def climb_down(self, levels, current_level, player):
        """ Moves the player up or down the staircase.

        If going down, moves the player down the level stack. If there is
        no level to go to,  generates a new level and pushes it to the 
        top of the levels stack. If going up, moves the player up to the
        the stack.
        """
        
        index = levels.index(current_level)
        new_level = None 

        # If the player is moving down, but is already on the last level,
        # generate a new one.
        if index == len(levels) - 1:
            player_coords = (player.tile.x, player.tile.y) 
            good_level = False
            
            while not good_level:
                new_level = lvls.Level(current_level.level_map.size_x,
                               current_level.level_map.size_y)
                rooms = new_level.level_map.rooms
                for room in rooms:
                    if player_coords in room.list_floorspace():
                        good_level = True
            start_tile = new_level.level_map.get_tile(player.tile.x,
                                                        player.tile.y)
            
            # Place a stairway back up where the player comes down.
            start_tile.feature = features.stairs.StairwayUp()
            levels.append(new_level)

        # If there already exists another level below the player, just move
        # down to that one.
        else:
            new_level = levels[index + 1]

        tile = new_level.level_map.get_tile(player.tile.x, player.tile.y)
        player.move(tile)
        return (levels, levels.index(new_level))

    def climb_up(self, levels, current_level, player):
        """ Moves the player up.

        Leaves the previous level in it's current state. 
        """
        index = levels.index(current_level)
        
        # If the player is on the top level, don't allow any further climbing.
        if index == 0:
            return (levels, index)
        
        new_level = levels[index - 1]
        tile =new_level.level_map.get_tile(player.tile.x, player.tile.y)
        player.move(tile)
        return (levels, index -1)
        
class StairwayDown(Stairway):
    """ A stairway going down.
    """

    icon = '<'

    def __init__(self):
        super().__init__(self.blocks_light, self.blocks_movement, self.icon)

    def climb(self, levels, current_level, player):
        return self.climb_down(levels, current_level, player)

class StairwayUp(Stairway):
    """ A stairway going up.
    """

    icon = '>'

    def __init__(self):
        super().__init__(self.blocks_light, self.blocks_movement, self.icon)

    def climb(self, levels, current_level, player):
        return self.climb_up(levels, current_level, player)
