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

# colors
YELLOW = (255, 255, 0)
RED = (255, 0 , 0)
WHITE = (255, 255, 255)

# load bg
bg_img = pg.image.load(join('assets', 'images', 'background', 'background.jpg')).convert_alpha()

# load sprite sheets
warrior_sheet = pg.image.load(join('assets', 'images', 'warrior', 'Sprites', 'warrior.png'))
wizard_sheet = pg.image.load(join('assets', 'images', 'wizard', 'Sprites', 'wizard.png'))

# define fighter variables
WARRIOR_SIZE = 162  # px^2
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# define number of frames per animation
WARRIOR_ANIM_FRAMES = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIM_FRAMES = [8, 8, 1, 8, 8, 3, 7]

# create two fighters
fighter_1 = Fighter(200, 310, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIM_FRAMES)
fighter_2 = Fighter(700, 310, WIZARD_DATA, wizard_sheet, WIZARD_ANIM_FRAMES)

# FUNCTIONS
def draw_bg():

    scaled_bg = pg.transform.scale(bg_img, (WIDTH, HEIGHT))
    WIN.blit(scaled_bg, (0,0))

def draw_health_bar(health, x, y):

    ratio = health / 100
    # white outline
    pg.draw.rect(WIN, WHITE, (x - 2, y - 2, 404, 34))
    # red bg
    pg.draw.rect(WIN, RED, (x, y, 400, 30))
    # health
    pg.draw.rect(WIN, YELLOW, (x, y, 400 * ratio, 30))
    

# game loop
running = True
while running:

    # tick the framerate clock
    clock.tick(FPS)

    # display bg
    draw_bg()

    # display bars
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)

    # move fighters
    fighter_1.move(WIN, WIDTH, HEIGHT, fighter_2)
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