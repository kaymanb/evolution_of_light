from features.glyphs import Glyph

class MeleeWeapon(Glyph):
    """ Generic wrapper class for a melee weapon.
    """

    def __init__(self, icon, color, dmg):
        super().__init__(icon, color)
        self.dmg = dmg


