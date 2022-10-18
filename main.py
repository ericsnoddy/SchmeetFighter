# std lib
import sys
from os.path import join

# 3rd party
import pygame as pg

# local
from fighter import Fighter


pg.init()
WIDTH = 1000
HEIGHT = 600

WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Schmeet Fighter 2')

# set framerate
clock = pg.time.Clock()
FPS = 60

# load bg
bg_img = pg.image.load(join('assets', 'images', 'background', 'background.jpg')).convert_alpha()

# create two fighters
fighter_1 = Fighter(200, 310)
fighter_2 = Fighter(700, 310)

# FUNCTIONS
def draw_bg():

    scaled_bg = pg.transform.scale(bg_img, (WIDTH, HEIGHT))
    WIN.blit(scaled_bg, (0,0))



# game loop
running = True
while running:

    # tick the framerate clock
    clock.tick(FPS)

    # display bg
    draw_bg()

    # move fighters
    fighter_1.move(WIDTH, HEIGHT)
    # fighter_2.move()

    # draw fighters
    fighter_1.draw(WIN)
    fighter_2.draw(WIN)

    # event handler
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # update display
    pg.display.update()
    

# quit and exit
pg.quit()
sys.exit()