# std lib
import sys
from os.path import join

# 3rd party
import pygame as pg

# local

pg.init()
WIDTH = 1000
HEIGHT = 600

WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Schmeet Fighter 2')

# load bg
bg_img = pg.image.load(join('assets', 'images', 'background', 'background.jpg')).convert_alpha()

# FUNCTIONS
def draw_bg():

    scaled_bg = pg.transform.scale(bg_img, (WIDTH, HEIGHT))
    WIN.blit(scaled_bg, (0,0))



# game loop
running = True
while running:

    # display bg
    draw_bg()

    # event handler
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # update display
    pg.display.update()

# quit and exit
pg.quit()
sys.exit()