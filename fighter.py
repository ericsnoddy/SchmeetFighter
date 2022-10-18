
# 3rd party
import pygame as pg

class Fighter:
    def __init__(self, x, y):

        self.rect = pg.Rect(x, y, 80, 180)
        self.vel_y = 0
        self.jumping = False

    def move(self, screen_width, screen_height):
        SPEED = 10
        GRAVITY = 2
        move_vect = pg.math.Vector2(0,0)

        # get key presses
        key = pg.key.get_pressed()

        # movement
        if key[pg.K_a]:
            move_vect[0] = -SPEED
        if key[pg.K_d]:
            move_vect[0] = SPEED

        # jumping
        if key[pg.K_w] and not self.jumping:
            self.vel_y = -30
            self.jumping = True

        # apply gravity
        self.vel_y += GRAVITY
        move_vect[1] += self.vel_y
        
        # ensure player stays on screen
        if self.rect.left + move_vect[0] < 0:
            move_vect[0] = -self.rect.left
        if self.rect.right + move_vect[0] > screen_width:
            move_vect[0] = screen_width - self.rect.right
        if self.rect.bottom + move_vect[1] > screen_height - 110:
            self.vel_y = 0
            self.jumping = False
            move_vect[1] = screen_height - 110 - self.rect.bottom

        # update position
        self.rect.x += move_vect[0]
        self.rect.y += move_vect[1]

    def draw(self, surf):
        pg.draw.rect(surf, (255, 0, 0), self.rect)