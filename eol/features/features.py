from features.glyphs import Glyph
import curses
#TODO: Clean this module up, inheritance doesn't make sence

class Feature(Glyph):
    """ A feature is the defining characteristic of a tile. This is the parent
    class that all features will inherit from. 
    """

    def __init__(self, blocks_light, blocks_movement, icon,
                 color=curses.COLOR_WHITE):
        """ A generic feature that can either block light and/or movement.
        """
        super().__init__(icon, color)
        self.blocks_light = blocks_light
        self.blocks_movement = blocks_movement

class Wall(Feature):
    """ A Wall feature that blocks both light and movement"""

    sprite = '#'
    blocks_light = True
    blocks_movement = True
    
    def __init__(self):
        super().__init__(self.blocks_light, self.blocks_movement, self.sprite)
    
class EmptyFeature(Feature):
    """ An empty feature that omits both light and movement"""

    sprite = '.'
    blocks_light = False
    blocks_movement = False

    def __init__(self):
        super().__init__(self.blocks_light, self.blocks_movement, self.sprite)
