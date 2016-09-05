###    ###
# Errors #
###    ###

class ColorsNotSupportedError(Exception):
    """ Error raised when starting the game in a terminal without support for
    colors.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidMovementError(Exception):
    """ Exception for attempting to move to invalid tile.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
