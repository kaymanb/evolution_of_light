                            Light in the Dark

LitD is a roguelike adventure game playable in the shell. It is written in
python and makes extensive use of the curses library to display text to the
screen.

              ( \      \__   __/(  ____ \|\     /|\__   __/
              | (         ) (   | (    \/| )   ( |   ) (   
              | |         | |   | |      | (___) |   | |   
              | |         | |   | | ____ |  ___  |   | |   
              | |         | |   | | \_  )| (   ) |   | |   
              | (____/\___) (___| (___) || )   ( |   | |   
              (_______/\_______/(_______)|/     \|   )_(   
              
                                in the
                  ______   _______  _______  _       
                 (  __  \ (  ___  )(  ____ )| \    /\
                 | (  \  )| (   ) || (    )||  \  / /
                 | |   ) || (___) || (____)||  (_/ / 
                 | |   | ||  ___  ||     __)|   _ (  
                 | |   ) || (   ) || (\ (   |  ( \ \ 
                 | (__/  )| )   ( || ) \ \__|  /  \ \
                 (______/ |/     \||/   \__/|_/    \/

Gameplay:
The game is composed of typical roguelike elements, but also makes use of a
light system by which characters can use to fight creatures and explore the
dungeon. Light is the life blood of a character, and characters will not
survive long without learning to use light to it's fullest potential. 

Development:

- The Map
In the most generality possible the game is composed of a grid of tiles. Tiles
can have various properties, but most importantly they can hold a list of items
as well as a single character, whether that be an NPC or our hero,  a single
feature (ie: a fountain, a boulder, a staircase, a wall, or nothing). Tiles
with a wall feature will compase most of the map, along with empty tiles that
will compose the floor. 

- The Items
Items are objects that can interact with characters. They
have various properties and when placed on a tile, fall into that tiles item
list. ALL items can be applied for some sort of effect. Items all extend the
Item class.

- The Characters
Characters are objects that can interact with their environment. They can move,
they can fight, and they can interact with items. Charcaters all extend the
Character class.  
