#!/usr/bin/python3
import pygame
import numpy as np
from scipy import signal

pygame.init()

WINDOW_W = 800
WINDOW_H = 600

gameDisplay = pygame.display.set_mode((WINDOW_W,WINDOW_H))
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()

# Settings
color_alive = (0,0,0)
color_dead = (200,200,200)

cell_w = 4
cell_h = 4

n_cell_x = int(WINDOW_W/cell_w)
n_cell_y = int(WINDOW_H/cell_h)

# Variables
grid = np.random.rand(n_cell_y, n_cell_x)
grid[grid < 0.90] = 0
grid[grid != 0] = 1
kernel = np.ones((3, 3))
kernel[1, 1] = 0
update = np.zeros((n_cell_y, n_cell_x))

stop = False
while not stop:
    # Print grid
    gameDisplay.fill(color_dead)
    for i, row in enumerate(grid):
        for j, element in enumerate(row):
            x = int(j*cell_w)
            y = int(i*cell_h)
            if element == 1:
                pygame.draw.rect(gameDisplay, color_alive, (x, y, cell_w, cell_h), 0)

    # Update grid
    update[:] = 0
    conv = signal.convolve2d(grid, kernel, boundary='wrap', mode='same')
    update[(grid == 1) & ((conv == 2)|(conv == 3))] = 1 #lives
    update[(grid == 0) & (conv == 3)] = 1 #reproduces
    grid = np.copy(update)

    # Check for quit commands
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                stop = True

    pygame.display.update()
    clock.tick(15)

pygame.quit()
