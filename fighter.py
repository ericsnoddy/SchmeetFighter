
# 3rd party
import pygame as pg

class Fighter:
    def __init__(self, x, y):

        self.rect = pg.Rect(x, y, 80, 180)
        self.vel_y = 0
        self.jumping = False
        self.attacking = False
        self.attack_type = 0

    def move(self, surf, screen_width, screen_height, fighter_2):
        SPEED = 10
        GRAVITY = 2
        move_vect = pg.math.Vector2(0,0)

        # get key presses
        key = pg.key.get_pressed()

        # perform movements only if not attacking
        if not self.attacking:
            # movement
            if key[pg.K_a]:
                move_vect[0] = -SPEED
            if key[pg.K_d]:
                move_vect[0] = SPEED

            # jumping
            if key[pg.K_w] and not self.jumping:
                self.vel_y = -30
                self.jumping = True

            # attacking
            if key[pg.K_r] or key[pg.K_t]:
                self.attack(surf, fighter_2)
                # determine attack type
                if key[pg.K_r]:
                    self.attack_type == 1
                if key[pg.K_t]:
                    self.attack_type == 2

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

    def attack(self, surf, target):
        # create rect for attack 2x as wide as character
        attacking_rect = pg.Rect(self.rect.centerx, self.rect.y, 2 * self.rect.width, self.rect.height)
        if attacking_rect.colliderect(target.rect):
            print('Hit')

        pg.draw.rect(surf, (0, 255, 0), attacking_rect)

    def draw(self, surf):
        pg.draw.rect(surf, (255, 0, 0), self.rect)