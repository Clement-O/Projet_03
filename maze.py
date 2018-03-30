# -*- coding: utf8 -*-

import pygame
import classes

"""
Contain the main function.
"""


def main():
    """
    Init everything, look for event and quit at the end.
    :return:
    """
    maze = classes.Maze('maze')

    loot = classes.Loot('maze')
    loot.available_list()
    loot.random_item_list()

    character = classes.Character('maze', loot)
    character.position()

    cartridge = classes.Cartridge(maze, loot, character)

    loop = 1
    while loop:
        for event in pygame.event.get():
            # Look for close event
            if event.type == pygame.QUIT:
                loop = 0
            # Look for keyboard event
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    character.move('up')
                if event.key == pygame.K_DOWN:
                    character.move('down')
                if event.key == pygame.K_RIGHT:
                    character.move('right')
                if event.key == pygame.K_LEFT:
                    character.move('left')

            # Create the base maze
            maze.create()
            # Add item, character and guard to the maze
            maze.additional(loot, character)
            # Check if inventory item += 1
            character.item()
            # Display text
            cartridge.display()

            pygame.display.flip()

            # If character is at the end, pause program and quit.
            if character.x == maze.guard_x and character.y == maze.guard_y:
                pygame.time.wait(2000)
                loop = 0


if __name__ == "__main__":
    main()
