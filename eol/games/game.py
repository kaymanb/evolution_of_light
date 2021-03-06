from games.input import InputHandler
from chars.char import Player
from levels.level import Level
from features.stairs import StairwayDown
import maps.map as maps
import games.console as console
import features.feature as feat
import curses

class EoLGame:
    """ Evolution of Light game.

        Methods in this class construct and control the flow of the game.
        """
    
    def __init__(self, x, y, screen):
        """ Create an instance of the game with an x by y map.    
        """
    
        # A stack of levels in the current dungeon.
        self.levels = [Level(x, y)]
        self.current_level = self.levels[0]
         
        
        start_room = self.current_level.level_map.rooms[0]
        (start_x, start_y) = start_room.list_floorspace()[0]
        start_tile = self.current_level.level_map.get_tile(start_x, start_y) 
        self.player = Player(start_tile, '@', curses.color_pair(1))
        self.screen = screen

    def draw_game(self):
        """ Draw the game to the screen.
        """
        self.current_level.draw_all(self.screen, self.player)
    
    def do_turn(self):
        """ Run the game for one turn.
        """
        state = self.handle_input()
        self.run_npcs()

        console.INFO.update(self.player)

        # Draw the game. Must be done after everything else.
        self.draw_game()
        return state

    def run_npcs(self):
        """ Tell each npc on the current level to perform one turn worth of
        action.
        """
        for npc in self.current_level.npcs:
            npc.follow_player(self.current_level.level_map, self.player)

    def handle_input(self):
        """ Handle user input, allowing the player to perform an action.
        """
        key = self.screen.getch()
        
        # TODO: Maybe don't reinstaniate this every turn.
        new = InputHandler(self)
        state = new.handle_input(key)
        return state
