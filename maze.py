# -*- coding: utf8 -*-

import pygame
import classes

"""
Contain the main function.
"""


def main():
    """ Init everything, look for event and quit at the end. """

    file = classes.File('maze')
    file.read()

    loot = classes.Loot()
    loot.random_list()

    character = classes.Character(loot)

    maze = classes.Maze(character, loot)

    cartridge = classes.Cartridge(character)

    pygame.key.set_repeat(150, 200)

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
            maze.additional()
            # Check if inventory item += 1
            character.item()
            # Display text
            cartridge.display()

            pygame.display.flip()

            # If character is at the end, pause program and quit.
            if character.x == file.GUARD_X and character.y == file.GUARD_Y:
                pygame.time.wait(2000)
                loop = 0


if __name__ == "__main__":
    main()
