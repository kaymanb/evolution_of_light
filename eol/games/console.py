import constants.colors as colors
import curses


def init_console(x, y, width, height):
    global STD
    STD = ConsoleManager(x, y, width, height)

def init_info_console(x, y, width, height):
    global INFO
    INFO = InfoManager(x, y, width, height)

class ConsoleManager(object):
    """ A class for managing output to the console. 
    """

    def __init__(self, x, y, width, height):
        """ Creates the console window at the input position with the given
        dimensions.
        """
        self.win = curses.newwin(height, width, y, x)
        self.win.touchwin()
   
    def log(self, msg):
        """ Logs a message to the console.
        """
        self.win.erase()
        self.win.addstr(0, 1, msg)
        self.win.refresh()

class InfoManager(ConsoleManager):
    """ Manager the display of player information to the screen.
    """

    def update(self, player):
        """ Updates the information box with data about the input character.
        """
        self.win.erase()

        self.win.addstr(0, 0, player.name)
        self.win.addstr(1, 0, player.title)
        self.win.addstr(3, 0, "Turns: " + str(player.turns))

        # Display HP
        # TODO: Refactor hp_missing into something easier to understand.
        hp_str = "HP: " + str(player.hp) + "/" + str(player.max_hp)
        color = curses.COLOR_WHITE
        hp_missing = player.max_hp - player.hp
        if hp_missing >= player.max_hp * 0.75: # Order here matters!
            color = curses.color_pair(3)
        elif hp_missing >= player.max_hp * 0.5:
            color = curses.color_pair(1)
        self.win.addstr(5, 0, hp_str, color)
        self.win.addstr(6, 0, "AC: " + str(player.ac))
        self.win.refresh()

