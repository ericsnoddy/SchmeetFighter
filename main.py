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
pg.display.set_caption('Schmeet Fighter')

# set framerate
clock = pg.time.Clock()
FPS = 60

# define color constants
YELLOW = (255, 255, 0)
RED = (255, 0 , 0)
WHITE = (255, 255, 255)

# load bg
bg_img = pg.image.load(join('assets', 'images', 'background', 'background.jpg')).convert_alpha()

# load sprite sheets
warrior_sheet = pg.image.load(join('assets', 'images', 'warrior', 'Sprites', 'warrior.png')).convert_alpha()
wizard_sheet = pg.image.load(join('assets', 'images', 'wizard', 'Sprites', 'wizard.png')).convert_alpha()

# load victory image
victory_img = pg.image.load(join('assets', 'images', 'icons', 'victory.png')).convert_alpha()

# define game variables
intro_count = 3
last_count_update = round_over_time = pg.time.get_ticks()
round_over = False
ROUND_OVER_COOLDOWN = 2500
score = [0, 0]  # [player 1 score, player 2 score]

# define fighter constants
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

# load sounds
pgm = pg.mixer.music
pgs = pg.mixer.Sound
pgm.load(join('assets', 'audio', 'music.mp3'))
pgm.set_volume(0.5)
pgm.play(-1, 0.0, 5000)
sword_fx = pgs(join('assets', 'audio', 'sword.wav'))
sword_fx.set_volume(0.5)
staff_fx = pgs(join('assets', 'audio', 'magic.wav'))
staff_fx.set_volume(0.75)

# create two fighters
fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIM_FRAMES, sword_fx)
fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIM_FRAMES, staff_fx)

# load fonts
count_font = pg.font.Font(join('assets', 'fonts', 'turok.ttf'), 150)
victory_font = pg.font.Font(join('assets', 'fonts', 'turok.ttf'), 130)
score_font = pg.font.Font(join('assets', 'fonts', 'turok.ttf'), 30)

# FUNCTIONS
def draw_bg():

    scaled_bg = pg.transform.scale(bg_img, (WIDTH, HEIGHT))
    WIN.blit(scaled_bg, (0,0))

def draw_text(text, font, color, x, y):

    img = font.render(text, True, color)
    WIN.blit(img, (x, y))

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

    # display scores
    draw_text('Player 1 KOs: ' + str(score[0]), score_font, RED, 20, 60)
    draw_text('Player 2 KOs: ' + str(score[1]), score_font, RED, 580, 60)

    # move fighters after intro countdown
    if intro_count <= 0:
        fighter_1.move(WIN, WIDTH, HEIGHT, fighter_2, round_over)
        fighter_2.move(WIN, WIDTH, HEIGHT, fighter_1, round_over)
    else:
        # display countdown
        draw_text(str(intro_count), count_font, RED, (WIDTH - 58) / 2, (HEIGHT - 168) / 4)
        # update countdown
        now = pg.time.get_ticks()
        if now - last_count_update >= 1000:
            intro_count -= 1
            last_count_update = now
            
    # update fighters
    fighter_1.update()
    fighter_2.update()

    # draw fighters
    fighter_1.draw(WIN)
    fighter_2.draw(WIN)

    # check for defeat
    if not round_over:
        now = pg.time.get_ticks()
        if not fighter_1.alive:
            score[1] += 1
            round_over = True
            round_over_time = now
        if not fighter_2.alive:
            score[0] += 1
            round_over = True
            round_over_time = now
    else:
        # display victory image
        if (fighter_1.alive and not fighter_2.alive) or (fighter_2.alive and not fighter_1.alive):
            draw_text('VICTORY!', victory_font, RED, (WIDTH - 462) / 2, (HEIGHT - 146) / 4)
        elif not fighter_1.alive and not fighter_2.alive:
            draw_text('DOUBLE KO!', victory_font, RED, (WIDTH - 585) / 2, (HEIGHT - 146) / 4)

        now = pg.time.get_ticks()
        if now - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            last_count_update = now            
            fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIM_FRAMES, sword_fx)
            fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIM_FRAMES, staff_fx)


    # event handler
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # update display
    pg.display.update()
    

# quit and exit
pg.quit()
sys.exit()