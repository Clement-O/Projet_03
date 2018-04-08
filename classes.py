# -*- coding: utf8 -*-

import random
import settings

"""
Contain every needed classes for the main function.
"""


class File:
    """" "Read" the maze file and stock every data the script might use later """
    # Maze List #
    MAZE_GRID = []
    MAZE_WALL = []
    MAZE_GROUND = []
    MAZE_POSSIBLE_ITEM = []
    # Maze Starting Position #
    INIT_CHARACTER_COLUMN = 0  # X Axis
    INIT_CHARACTER_LINE = 0  # Y Axis
    INIT_CHARACTER_X = 0
    INIT_CHARACTER_Y = 0
    GUARD_X = 0
    GUARD_Y = 0

    def __init__(self, file):
        self.file = file

    def read(self):
        """ "Read" the maze file and stock every data the script might use later """
        with open(self.file, 'r') as data:
            for line, value in enumerate(data):
                maze_line = []
                for column, letter in enumerate(value):
                    maze_wall_xy = []
                    maze_ground_xy = []
                    maze_possible_item_xy = []
                    x = column * settings.SPRITE_SIZE_W
                    y = line * settings.SPRITE_SIZE_W
                    if letter != '\n':
                        if letter == 'w':
                            maze_wall_xy.append(x)
                            maze_wall_xy.append(y)
                            File.MAZE_WALL.append(maze_wall_xy)
                        else:
                            maze_ground_xy.append(x)
                            maze_ground_xy.append(y)
                            File.MAZE_GROUND.append(maze_ground_xy)
                            if letter == ' ':
                                maze_possible_item_xy.append(x)
                                maze_possible_item_xy.append(y)
                                File.MAZE_POSSIBLE_ITEM.append(maze_possible_item_xy)
                            if letter == 'S':
                                File.INIT_CHARACTER_COLUMN = column
                                File.INIT_CHARACTER_LINE = line
                                File.INIT_CHARACTER_X = x
                                File.INIT_CHARACTER_Y = y
                            if letter == 'E':
                                File.GUARD_X = x
                                File.GUARD_Y = y
                        maze_line.append(letter)
                File.MAZE_GRID.append(maze_line)


class Loot:
    """ Calculate the loot's position. """

    def __init__(self):
        self.item_list = []

    def random_list(self):
        """ Choose a list of X (based on settings) random items from the maze possible item list. """
        self.item_list = random.sample(File.MAZE_POSSIBLE_ITEM, settings.NB_ITEM)


class Character:
    """ Calculate the initial character position and the new one after each event. """

    def __init__(self, loot):
        self.loot = loot
        # Positions #
        self.column = File.INIT_CHARACTER_COLUMN  # X Axis
        self.line = File.INIT_CHARACTER_LINE  # Y Axis
        self.x = File.INIT_CHARACTER_X
        self.y = File.INIT_CHARACTER_Y
        # Used externally #
        self.move_impossible = False
        self.move_direction = ""
        self.inventory = 0

    def move(self, direction):
        """
        Calculate every new position after an event. If the new position is unavailable (wall), let him at his current
        position and send a bool into a variable (used later to display message).
        :param direction: From the keyboard event.
        """
        self.move_impossible = False
        if direction == 'up':
            if self.y > 0:  # Can't go above y0
                if File.MAZE_GRID[self.line - 1][self.column] != 'w':  # Check if the new position has wall
                    self.line -= 1  # If not y-1
                    self.y = self.line * settings.SPRITE_SIZE_H  # New position in pixel
                else:  # If wall
                    self.move_impossible = True
                    self.move_direction = "UP"
        if direction == 'down':
            if self.y < (settings.WINDOW_HEIGHT - settings.SPRITE_SIZE_H):
                if File.MAZE_GRID[self.line + 1][self.column] != 'w':
                    self.line += 1
                    self.y = self.line * settings.SPRITE_SIZE_H
                else:  # If wall
                    self.move_impossible = True
                    self.move_direction = "DOWN"
        if direction == 'right':
            if self.x < (settings.WINDOW_WIDTH - settings.SPRITE_SIZE_W):
                if File.MAZE_GRID[self.line][self.column + 1] != 'w':
                    self.column += 1
                    self.x = self.column * settings.SPRITE_SIZE_W
                else:  # If wall
                    self.move_impossible = True
                    self.move_direction = "RIGHT"
        if direction == 'left':
            if self.x > 0:
                if File.MAZE_GRID[self.line][self.column - 1] != 'w':
                    self.column -= 1
                    self.x = self.column * settings.SPRITE_SIZE_W
                else:  # If wall
                    self.move_impossible = True
                    self.move_direction = "LEFT"

    def item(self):
        """ Look if the character position is on an items. If yes: delete this item and inventory += 1. """
        for i, item in enumerate(self.loot.item_list):
            if self.x == item[0] and self.y == item[1]:
                self.inventory += 1
                del self.loot.item_list[i]


class Maze:
    """ Create the base maze and additional items to have a complete maze. """

    def __init__(self, character, loot):
        self.character = character
        self.loot = loot

    @staticmethod
    def create():
        """ Create and blit the base maze. """
        for index, position in enumerate(File.MAZE_WALL):
            settings.WINDOW.blit(settings.WALL, (position[0], position[1]))
        for index, position in enumerate(File.MAZE_GROUND):
            settings.WINDOW.blit(settings.GROUND, (position[0], position[1]))

    def additional(self):
        """ Check if character is on items or at the end (or not) and blit the needed sprites. """
        # If Character is at the end with ou without all the items #
        if self.character.x == File.GUARD_X and self.character.y == File.GUARD_Y:
            if self.character.inventory == settings.NB_ITEM:
                settings.WINDOW.blit(settings.CHARACTER, (self.character.x, self.character.y))
            else:
                settings.WINDOW.blit(settings.GUARD, (File.GUARD_X, File.GUARD_Y))
        else:
            settings.WINDOW.blit(settings.CHARACTER, (self.character.x, self.character.y))
            settings.WINDOW.blit(settings.GUARD, (File.GUARD_X, File.GUARD_Y))

        # If Character is on a item #
        for i, item in enumerate(self.loot.item_list):
            if self.character.x == item[0] and self.character.y == item[1]:
                settings.WINDOW.blit(settings.CHARACTER, (self.character.x, self.character.y))
            else:
                settings.WINDOW.blit(settings.ITEM, (item[0], item[1]))


class Cartridge:
    """ Display every text at the bottom of the window. """

    def __init__(self, character):
        self.character = character

    def display(self):
        """ Take parameter in (such as the impossible movement from Character class.) and display it. """
        settings.WINDOW.fill((0, 0, 0), (0, settings.WINDOW_HEIGHT, settings.WINDOW_WIDTH, settings.SPRITE_SIZE_H))
        # ((Color), (X, Y, Width, Height))

        text_str = ""
        text = settings.FONT.render(text_str, 0, (250, 250, 250))

        # If movement is impossible (because wall) :
        if self.character.move_impossible is True:
            text_str = "IMPOSSIBLE MOVE " + self.character.move_direction + " !"
            text = settings.FONT.render(text_str, 0, (250, 250, 250))

        # Check if character has all the item. Win or Lose.
        if self.character.x == File.GUARD_X and self.character.y == File.GUARD_Y:
            if self.character.inventory == settings.NB_ITEM:
                text_str = "YOU KNOCK THE GUARD AND GAIN FREEDOM !"
                text = settings.FONT.render(text_str, 0, (250, 250, 250))
            if self.character.inventory != settings.NB_ITEM:
                inventory = settings.NB_ITEM - self.character.inventory
                if inventory == 1:
                    text_str = "GAME OVER ! YOU MISSED : " + str(inventory) + " ITEM !"
                    text = settings.FONT.render(text_str, 0, (250, 250, 250))
                else:
                    text_str = "GAME OVER ! YOU MISSED : " + str(inventory) + " ITEMS !"
                    text = settings.FONT.render(text_str, 0, (250, 250, 250))

        # Else if movement is possible and character isn't at the end, print inventory state
        elif self.character.move_impossible is False:
            text_str = "YOU HAVE " + str(self.character.inventory) + " ITEMS OUT OF " + str(settings.NB_ITEM) + " !"
            text = settings.FONT.render(text_str, 0, (250, 250, 250))

        # Center the text on the cartridge #
        text_width = text.get_width()
        text_height = text.get_height()
        text_left = settings.WINDOW_WIDTH / 2 - text_width / 2
        text_top = settings.WINDOW_HEIGHT + (settings.CARTRIDGE_H / 2 - text_height / 2)
        settings.WINDOW.blit(text, (text_left, text_top))
