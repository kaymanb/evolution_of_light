

class Feature:
    """ A feature is the defining characteristic of a tile. This is the parent
    class that all features will inherit from. 
    """

    def __init__(self, blocks_light, blocks_movement, sprite):
        """ A generic feature that can either block light and/or movement.
        """
        self.blocks_light = blocks_light
        self.blocks_movement = blocks_movement
        self.sprite = sprite

class Wall(Feature):
    """ A Wall feature that blocks both light and movement"""

    sprite = '#'
    blocks_light = True
    blocks_movement = True
    
    def __init__(self):
        super().__init__(self.blocks_light, self.blocks_movement, self.sprite)
    
class EmptyFeature(Feature):
    """ An empty feature that emits both light and movement"""

    sprite = '.'
    blocks_light = False
    blocks_movement = False

    def __init__(self):
        super().__init__(self.blocks_light, self.blocks_movement, self.sprite)
