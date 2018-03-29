# -*- coding: utf8 -*-

import pygame

"""
Contain every single constants needed to the program. Change one of them and it will impact the whole maze game !
"""

pygame.init()

#  SETTINGS  #
# Change those values to fit your sprite, maze and random item spawn #
SPRITE_SIZE_W = 32  # X
SPRITE_SIZE_H = 32  # Y
SPRITE_NUM = 15
NB_ITEM = 3

# WINDOW #
WINDOW_WIDTH = SPRITE_SIZE_W * SPRITE_NUM
WINDOW_HEIGHT = SPRITE_SIZE_H * SPRITE_NUM
CARTRIDGE_W = WINDOW_WIDTH
CARTRIDGE_H = SPRITE_SIZE_H

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT + CARTRIDGE_H))
pygame.display.set_caption("MacGyver Maze")
ICON = pygame.image.load("sprites/character.png").convert_alpha()
ICON = pygame.transform.scale(ICON, (SPRITE_SIZE_W, SPRITE_SIZE_H))
pygame.display.set_icon(ICON)

# SPRITES #
WALL = pygame.image.load("sprites/wall.png").convert()
WALL = pygame.transform.scale(WALL, (SPRITE_SIZE_W, SPRITE_SIZE_H))

GROUND = pygame.image.load("sprites/ground.png").convert()
GROUND = pygame.transform.scale(GROUND, (SPRITE_SIZE_W, SPRITE_SIZE_H))

GUARD = pygame.image.load("sprites/guard.png").convert_alpha()
GUARD = pygame.transform.scale(GUARD, (SPRITE_SIZE_W, SPRITE_SIZE_H))

CHARACTER = pygame.image.load("sprites/character.png").convert_alpha()
CHARACTER = pygame.transform.scale(CHARACTER, (SPRITE_SIZE_W, SPRITE_SIZE_H))

ITEM = pygame.image.load("sprites/item.png").convert_alpha()
ITEM = pygame.transform.scale(ITEM, (SPRITE_SIZE_W, SPRITE_SIZE_H))

# TEXT #
FONT = pygame.font.SysFont("monospace", SPRITE_SIZE_H // 2)
