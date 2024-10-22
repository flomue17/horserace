# config.py
import pygame
import sys

# Bildschirmgröße definieren
WIDTH, HEIGHT = 1920,1080

# Farben definieren
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

start_x = 15
start_y = 15

goal_x = 1920-75

amount_points = 11

step_size = (goal_x-start_x) / amount_points

amount_teams = 12