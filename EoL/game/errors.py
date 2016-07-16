
class InvalidMovementError(Exception):
    """ Exception for attempting to move to invalid tile.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
