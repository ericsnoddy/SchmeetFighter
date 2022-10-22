
# 3rd party
import pygame as pg

class Fighter:
    def __init__(self, x, y, player_data, sprite_sheet, frame_number_list):

        self.size = player_data[0]  # px^2
        self.flip = False
        self.anim_list = self.load_images(sprite_sheet, frame_number_list)
        self.action = 0  # 0: idle, 1: run, 2: jump, 3: attack1, 4: attack2, 5: hit, 6: death
        self.rect = pg.Rect(x, y, 80, 180)
        self.vel_y = 0
        self.jumping = False
        self.attacking = False
        self.attack_type = 0
        self.health = 100

    def load_images(self, sprite_sheet, frame_number_list):

        anim_list = []

        for y, frames in enumerate(frame_number_list):

            # temp img list
            temp_img_list = []

            # extract from sprite sheet
            for x in range(frames):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(temp_img)

            anim_list.append(temp_img_list)
        
        return anim_list

    def move(self, surf, screen_width, screen_height, target):

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
                self.attack(surf, target)
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

        # ensure players face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else: self.flip = True

        # update position
        self.rect.x += move_vect[0]
        self.rect.y += move_vect[1]

    def attack(self, surf, target):

        self.attacking = True

        # create rect for attack 2x as wide as character, accounting for facing direction
        attacking_rect = pg.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
        if attacking_rect.colliderect(target.rect):
            target.health -= 10

        pg.draw.rect(surf, (0, 255, 0), attacking_rect)

    def draw(self, surf):
        pg.draw.rect(surf, (255, 0, 0), self.rect)