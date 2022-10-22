
# 3rd party
import pygame as pg

class Fighter:
    def __init__(self, player_x, x, y, flip, player_data, sprite_sheet, frame_number_list, sound_fx):

        self.player_x = player_x
        self.sound_fx = sound_fx
        self.size = player_data[0]  # px^2
        self.scale = player_data[1]  # image scaling
        self.offset = player_data[2]  # px offset        
        self.anim_list = self.load_images(sprite_sheet, frame_number_list)
        self.action = 0  # 0: idle, 1: run, 2: jump, 3: attack1, 4: attack2, 5: hit, 6: death
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()
        self.image = self.anim_list[self.action][self.frame_index]
        self.rect = pg.Rect(x, y, 80, 180)

        self.vel_y = 0
        self.flip = flip
        self.running = False
        self.jumping = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.hit = False
        self.damage = 10
        self.health = 100
        self.alive = True

    def load_images(self, sprite_sheet, frame_number_list):

        anim_list = []

        for y, frames in enumerate(frame_number_list):

            temp_img_list = []

            # extract from sprite sheet
            for x in range(frames):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img = pg.transform.scale(temp_img, (self.size * self.scale, self.size * self.scale))
                temp_img_list.append(temp_img)

            anim_list.append(temp_img_list)
        
        return anim_list

    def move(self, surf, screen_width, screen_height, target, round_over):

        SPEED = 10
        GRAVITY = 2

        # reset variables
        move_vect = pg.math.Vector2(0,0)
        self.running = False
        self.attack_type = 0

        # get key presses
        key = pg.key.get_pressed()

        # perform movements only if not attacking
        if not self.attacking and self.alive and not round_over:

            # check player 1 controls
            if self.player_x == 1:
                # movement
                if key[pg.K_a]:
                    move_vect[0] = -SPEED
                    self.running = True
                if key[pg.K_d]:
                    move_vect[0] = SPEED
                    self.running = True

                # jumping
                if key[pg.K_w] and not self.jumping:
                    self.vel_y = -30
                    self.jumping = True

                # attacking
                if key[pg.K_r] or key[pg.K_t]:
                    self.attack(surf, target)
                    # determine attack type
                    if key[pg.K_r]:
                        self.attack_type = 1
                        self.damage = 10
                    if key[pg.K_t]:
                        self.attack_type = 2
                        self.damage = 15

            # check player 2 controls
            if self.player_x == 2:
                # movement
                if key[pg.K_LEFT]:
                    move_vect[0] = -SPEED
                    self.running = True
                if key[pg.K_RIGHT]:
                    move_vect[0] = SPEED
                    self.running = True

                # jumping
                if key[pg.K_UP] and not self.jumping:
                    self.vel_y = -30
                    self.jumping = True

                # attacking
                if key[pg.K_PAGEUP] or key[pg.K_PAGEDOWN]:
                    self.attack(surf, target)
                    # determine attack type
                    if key[pg.K_PAGEUP]:
                        self.attack_type = 1
                    if key[pg.K_PAGEDOWN]:
                        self.attack_type = 2

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

        # apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # update position
        self.rect.x += move_vect[0]
        self.rect.y += move_vect[1]

    def update(self):

        # check action to determine animation
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)  # death
        elif self.hit:
            self.update_action(5)  # hit
        elif self.attacking:
            if self.attack_type == 1:
                self.update_action(3)  # attack 1
            elif self.attack_type == 2:
                self.update_action(4)  # attack 2
        elif self.jumping:
            self.update_action(2)  # jump
        elif self.running:
            self.update_action(1)  # run
        else: 
            self.update_action(0)  # idle

        COOLDOWN = 75
        now = pg.time.get_ticks()

        if now - self.update_time > COOLDOWN:
            self.image = self.anim_list[self.action][self.frame_index]
            self.frame_index += 1
            self.update_time = now

        # ensure index is within range (animation has finished)
        if self.frame_index >= len(self.anim_list[self.action]):

            # halt animation if dead
            if not self.alive:
                self.frame_index = len(self.anim_list[self.action]) - 1
            else:
                self.frame_index = 0
                # check if attack executed
                if self.action == 3:
                    self.attacking = False
                    self.attack_cooldown = 20
                if self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 30
                # check if damage was taken
                if self.action == 5:
                    self.hit = False
                    # if player in middle of attack, halt attack; successful parry
                    self.attacking = False
                    self.attack_cooldown = 25

    def attack(self, surf, target):

        # only if attack is allowed
        if self.attack_cooldown == 0:
            self.attacking = True
            self.sound_fx.play()            

            # create rect for attack 2x as wide as character, accounting for facing direction
            attacking_rect = pg.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= self.damage
                target.hit = True


    def update_action(self, new_action):

        # check if new action is different than previous
        if new_action != self.action:
            self.action = new_action

            # update animation settings
            self.frame_index = 0
            self.update_time = pg.time.get_ticks()

    def draw(self, surf):

        img = pg.transform.flip(self.image, self.flip, False)
        surf.blit(img, (self.rect.x - (self.offset[0] * self.scale), self.rect.y - (self.offset[1] * self.scale)))