# -*- coding: utf8 -*-

import random
import settings

"""
Contain every needed classes for the main function.
"""


class Maze:
    """
    Create the base maze and additional items to have a complete maze.
    """

    def __init__(self, file):
        self.file = file

        self.guard_x = 0
        self.guard_y = 0

    def create(self):
        """
        Create and blit the base maze.
        :return:
        """
        with open(self.file, 'r') as data:
            line_number = 0  # Y Axis
            for line in data:
                column_number = 0  # X Axis
                for letter in line:
                    x = column_number * settings.SPRITE_SIZE_W  # X in pixel
                    y = line_number * settings.SPRITE_SIZE_H  # Y in pixel
                    if letter != '\n':
                        if letter == 'w':
                            settings.WINDOW.blit(settings.WALL, (x, y))
                        elif letter == 'E':
                            self.guard_x = column_number * settings.SPRITE_SIZE_W
                            self.guard_y = line_number * settings.SPRITE_SIZE_H
                            settings.WINDOW.blit(settings.GROUND, (self.guard_x, self.guard_y))
                        else:
                            settings.WINDOW.blit(settings.GROUND, (x, y))
                    column_number += 1
                line_number += 1

    def additional(self, loot, character):
        """
        Check if character is on items or at the end (or not) and blit the needed sprites (items / character / guard).
        :param loot: List of items to blit.
        :param character: Character and guard position.
        :return:
        """
        loot = loot
        character = character

        if character.x == self.guard_x and character.y == self.guard_y:
            if character.inventory == settings.NB_ITEM:
                settings.WINDOW.blit(settings.CHARACTER, (character.x, character.y))
            else:
                settings.WINDOW.blit(settings.GUARD, (self.guard_x, self.guard_y))
        else:
            settings.WINDOW.blit(settings.CHARACTER, (character.x, character.y))
            settings.WINDOW.blit(settings.GUARD, (self.guard_x, self.guard_y))

        i = 0
        while i < len(loot.random_list):
            item_column = loot.random_list[i][0]
            item_line = loot.random_list[i][1]
            x = item_column * settings.SPRITE_SIZE_W
            y = item_line * settings.SPRITE_SIZE_H
            if character.column == item_column and character.line == item_line:
                settings.WINDOW.blit(settings.CHARACTER, (character.x, character.y))
                i += 1
            else:
                settings.WINDOW.blit(settings.ITEM, (x, y))
                i += 1


class Loot:
    """
    Calculate the position of the loot.
    """

    def __init__(self, file):
        self.file = file
        self.possible_list = []
        self.random_list = []

    def available_list(self):
        """
        Calculate the possible position list for items.
        :return:
        """
        with open(self.file) as data:
            line_number = 0  # Y Axis
            for line in data:
                column_number = 0  # X Axis
                for letter in line:
                    random_cl = []
                    if letter == ' ':
                        random_cl.append(column_number)
                        random_cl.append(line_number)
                        self.possible_list.append(random_cl)
                    column_number += 1
                line_number += 1

    def random_item_list(self):
        """
        Choose a number of random items (based on settings) from the get_random() property.
        :return:
        """
        item = 0
        while item < settings.NB_ITEM:
            self.random_list.append(self.get_random)
            item += 1

    @property
    def get_random(self):
        """
        Pick a random position for one item from the possible list and delete it (to avoid picking it twice).
        :return:
        """
        number = random.randint(0, len(self.possible_list) - 1)
        item_cl = self.possible_list[number]
        del self.possible_list[number]
        return item_cl


class Character:
    """
    Calculate the initial character position and the new one after each event.
    """

    def __init__(self, file, loot):
        self.file = file
        self.loot = loot

        self.column = 0  # X Axis
        self.line = 0  # Y Axis
        self.x = 0
        self.y = 0
        self.grid = []
        self.impossible = 0
        self.direction = 0

        self.inventory = 0

    def position(self):
        """
        Initial character position in coordinates and pixel.
        :return:
        """
        with open(self.file) as data:
            grid_line = []  # grid [Y Axis]
            line_number = 0  # Y Axis
            for line in data:
                grid_column = []  # grid [X Axis]
                column_number = 0  # X Axis
                for letter in line:
                    if letter != '\n':
                        if letter == 'S':
                            self.column = column_number
                            self.line = line_number
                            self.x = column_number * settings.SPRITE_SIZE_W
                            self.y = line_number * settings.SPRITE_SIZE_H
                    grid_column.append(letter)
                    column_number += 1
                grid_line.append(grid_column)
                line_number += 1
            self.grid = grid_line

    def move(self, direction):
        """
        Calculate every new position after an event. If the new position is unavailable (wall), let him at his current
        position and send a bool into a variable (used later to display message).
        :param direction: From the keyboard event.
        :return:
        """
        self.impossible = 0
        if direction == 'up':
            if self.y > 0:  # Can't go above y0
                if self.grid[self.line - 1][self.column] != 'w':  # Check if the new position has wall
                    self.line -= 1  # If not y-1
                    self.y = self.line * settings.SPRITE_SIZE_H  # New position in pixel
                else:  # If wall
                    self.impossible = 1
                    self.direction = "UP"
        if direction == 'down':
            if self.y < (settings.WINDOW_HEIGHT - settings.SPRITE_SIZE_H):
                if self.grid[self.line + 1][self.column] != 'w':
                    self.line += 1
                    self.y = self.line * settings.SPRITE_SIZE_H
                else:  # If wall
                    self.impossible = 1
                    self.direction = "DOWN"
        if direction == 'right':
            if self.x < (settings.WINDOW_WIDTH - settings.SPRITE_SIZE_W):
                if self.grid[self.line][self.column + 1] != 'w':
                    self.column += 1
                    self.x = self.column * settings.SPRITE_SIZE_W
                else:  # If wall
                    self.impossible = 1
                    self.direction = "RIGHT"
        if direction == 'left':
            if self.x > 0:
                if self.grid[self.line][self.column - 1] != 'w':
                    self.column -= 1
                    self.x = self.column * settings.SPRITE_SIZE_W
                else:  # If wall
                    self.impossible = 1
                    self.direction = "LEFT"

    def item(self):
        """
        Look if the character position is on an items. If yes: delete this item and inventory += 1.
        :return:
        """
        i = 0
        while i < len(self.loot.random_list):
            item_column = self.loot.random_list[i][0]
            item_line = self.loot.random_list[i][1]
            if self.column == item_column and self.line == item_line:
                self.inventory += 1
                del self.loot.random_list[i]
            else:
                i += 1


class Cartridge:
    """
    Display every text at the bottom of the window.
    """

    def __init__(self, maze, loot, character):
        self.maze = maze
        self.loot = loot
        self.character = character

    def display(self):
        """
        Take parameter in (such as the impossible movement from Character class.) and display it.
        :return:
        """
        settings.WINDOW.fill((0, 0, 0), (0, settings.WINDOW_HEIGHT, settings.WINDOW_WIDTH, settings.SPRITE_SIZE_H))
        # ((Color), (X, Y, Width, Height))

        # If movement is impossible (because wall) :
        if self.character.impossible:
            text_str = "IMPOSSIBLE MOVE " + self.character.direction + " !"
            text = settings.FONT.render(text_str, 0, (250, 250, 250))
            text_width = text.get_width()
            text_height = text.get_height()
            text_left = settings.WINDOW_WIDTH / 2 - text_width / 2
            text_top = settings.WINDOW_HEIGHT + (settings.CARTRIDGE_H / 2 - text_height / 2)
            settings.WINDOW.blit(text, (text_left, text_top))

        # Check if character has all the item. Win or Lose.
        if self.character.x == self.maze.guard_x and self.character.y == self.maze.guard_y:
            if self.character.inventory == settings.NB_ITEM:
                text = settings.FONT.render("YOU WON !", 0, (250, 250, 250))
                text_width = text.get_width()
                text_height = text.get_height()
                text_left = settings.WINDOW_WIDTH / 2 - text_width / 2
                text_top = settings.WINDOW_HEIGHT + (settings.CARTRIDGE_H / 2 - text_height / 2)
                settings.WINDOW.blit(text, (text_left, text_top))
            if self.character.inventory != settings.NB_ITEM:
                text = settings.FONT.render("YOU LOST !", 0, (250, 250, 250))
                text_width = text.get_width()
                text_height = text.get_height()
                text_left = settings.WINDOW_WIDTH / 2 - text_width / 2
                text_top = settings.WINDOW_HEIGHT + (settings.CARTRIDGE_H / 2 - text_height / 2)
                settings.WINDOW.blit(text, (text_left, text_top))

        # Else if movement is possible and character isn't at the end, print inventory state
        elif self.character.impossible == 0:
            text_str = "YOU HAVE " + str(self.character.inventory) + " ITEMS OUT OF " + str(settings.NB_ITEM) + " !"
            text = settings.FONT.render(text_str, 0, (250, 250, 250))
            text_width = text.get_width()
            text_height = text.get_height()
            text_left = settings.WINDOW_WIDTH / 2 - text_width / 2
            text_top = settings.WINDOW_HEIGHT + (settings.CARTRIDGE_H / 2 - text_height / 2)
            settings.WINDOW.blit(text, (text_left, text_top))
