import pygame
import Velocity
import random
import os
import main
from Game import *
import Bullet
import Grenade
class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, type, flipped, grenades_count):
        super().__init__()
        # variables
        self.alive = True
        self.type = type
        self.x = x
        self.y = y
        self.velocity = Velocity(0, 0)
        self.direction = 0
        self.speed = speed
        self.jump = False
        self.double_jump = False
        self.jump_count = 0
        self.in_air = True
        self.flipped = flipped
        self.health = 100
        self.max_health = self.health
        self.sliding = False
        self.attacking = False
        self.diamonds = 0
        self.moving_right = False
        self.moving_left = False

        # ai specific variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0

        # Bullets
        self.shooting = False
        self.shoot_cooldown = 0
        self.ammo = 20
        self.start_ammo = self.ammo

        # grenades
        self.grenade = False
        self.grenade_thrown = False
        self.grenades_count = grenades_count


        # animation variables
        self.animation_list = []
        self.animate_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks() # now


        # animation images
        if self.type == 'player':
            animations = ['Idle', 'Attack', 'Run', 'Crouch', 'Jump', 'Fall', 'Slide', 'Hurt', 'Death', 'Double_Jump']
        else:
            animations = ['Idle', 'Run', 'Jump', 'Death']

        for anim_type in animations:
            # reset temporary list of images
            temp_list = []
            # get number of files in the folder
            num_of_frames = len(os.listdir(f'img/{self.type}/{anim_type}'))
            # loop through each image/frame for the animations
            for i in range(num_of_frames):
                image = pygame.image.load(f'img/{self.type}/{anim_type}/{i}.png').convert_alpha()
                image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
                temp_list.append(image)
            self.animation_list.append(temp_list)


        # settings
        self.img = self.animation_list[self.action][self.animate_index]
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)
        self.width = self.img.get_width()
        self.height = self.img.get_height()


    def update(self):
        self.update_animation()
        if self.attacking:
            enemies_attacked = pygame.sprite.spritecollide(player, enemy_group, False)
            if len(enemies_attacked) > 0:
                if enemies_attacked[0].alive:
                    self.attack(enemies_attacked[0])
        self.check_alive()

        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1


    def move(self):
        screen_scroll = 0

        # update action
        if self.alive:
            if self.grenade and not self.grenade_thrown and self.grenades_count > 0:
                self.throw_grenade()
                self.grenade_thrown = True
                self.grenades_count -= 1
            if self.in_air and self.type == 'player':
                if self.action != 9:
                    self.update_action(4) # 4: jumping
            
            # elif moving_right or moving_left:
            #     self.update_action(2) # 2: running
            # else:
            #     self.update_action(0) # 0: idle


        # reset movement variables
        dx = 0
        dy = 0

        # assign movement variables if moving left or right
        if self.moving_left:
            dx = -self.speed
            self.flipped = True
            self.direction = -1
        if self.moving_right:
            dx = self.speed
            self.flipped = False
            self.direction = 1

        # jump
        if self.jump and not self.in_air:
            self.velocity.y = -11
            self.jump = False
            self.in_air = True

        self.double_jump = self.jump and self.in_air and self.jump_count <= 2
        if self.double_jump:
            self.double_jump = False
            self.update_action(9)
            self.velocity.y = -11
            self.jump = False

        # falling
        if self.velocity.y >= 0 and self.in_air and self.type == 'player':
            self.update_action(5) # Fall

        # apply gravity
        self.velocity.y += main.GRAVITY
        if self.velocity.y > 10:
            self.velocity.y
        dy += self.velocity.y

        # check for collision
        # x collision with objects
        for tile in main.world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                # if the ai has hit a wall then make it turn around
                if self.type == 'enemy':
                    self.direction *= -1
                    self.move_counter = 0

        # y collision
        for tile in main.world.obstacle_list:
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if below the ground, i.e jumping
                if self.velocity.y < 0:
                    self.velocity.y = 0
                    dy = tile[1].bottom - self.rect.top
                # check if above the ground, i.e falling
                elif self.velocity.y >= 0:
                    self.velocity.y = 0
                    self.in_air = False
                    self.double_jump = False
                    self.jump_count = 0
                    # # if falling keep the correct animation going
                    if self.type == 'player':
                        if self.action == 5:
                            if self.moving_left or self.moving_right:
                                self.update_action(2) # running
                            else:
                                self.update_action(0) # idle

                    dy = tile[1].top - self.rect.bottom

        # check for collision with water or fallen off map 
        if pygame.sprite.spritecollide(self, main.water_group, False) or self.rect.y > main.SCREEN_HEIGHT:
            self.health = 0


        # check for collision with exit
        level_complete = False
        if pygame.sprite.spritecollide(self, main.exit_group, False):
            level_complete = True

        # check if going off the edges of the screen
        if self.type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > main.SCREEN_WIDTH:
                dx = 0


        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        # update scroll based on player position
        if self.type == 'player':
            if (self.rect.right > main.SCREEN_WIDTH - main.SCROLL_THRESH and main.bg_scroll < (main.world.level_length * main.TILE_SIZE) - main.SCREEN_WIDTH) or (self.rect.left < main.SCROLL_THRESH and main.bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        # update image depending on current frame
        self.img = self.animation_list[self.action][self.animate_index]

        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.animate_index += 1
            # if animation has run out then reset back to the start
            if self.animate_index >= len(self.animation_list[self.action]):
                # if animating death, make it stay on the last frame
                if ((self.action == 3 and self.type != 'player') or self.action == 8):
                    self.animate_index = len(self.animation_list[self.action]) - 1
                else:
                    self.animate_index = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.animate_index = 0
            self.update_time = pygame.time.get_ticks()


    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0 :
            self.shoot_cooldown = 5
            bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            main.bullet_group.add(bullet)
            self.ammo -= 0
            main.shot_fx.play()


    def throw_grenade(self):
        if not self.flipped:
            grenade = Grenade(player.rect.centerx + (player.rect.size[0] * 0.5), player.rect.centery, 1)
        else:
            grenade = Grenade(player.rect.centerx - (player.rect.size[0] * 0.5), player.rect.centery, -1)
        grenade_group.add(grenade)

    def ai(self):
        if self.alive and player.alive:
            if random.randint(1, 200) == 1 and not self.idling:
                self.update_action(0)  # 0: idle
                self.idling = True
                self.idling_counter = 50

            # check if the ai is near the player
            if self.vision.colliderect(player.rect):
                # stop running and shoot the player 
                self.update_action(0) # 0: Idle
                self.shoot()
            # if ai doesnt see player
            else:
                if not self.idling:
                    if self.direction == 1:
                        self.moving_right = True
                    else:
                        self.moving_right = False
                    self.moving_left = not self.moving_right
                    self.move()
                    self.update_action(1)
                    self.move_counter += 1

                    # update ai vision as the enemy moves
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

        # scroll
        self.rect.x += main.screen_scroll

    def attack(self, target):
        hit_range_rect = pygame.Rect(self.rect.left - 10, self. rect.top - 10, self.rect.width + 10, self.rect.height + 10)
        if hit_range_rect.colliderect(target.rect):
            target.update_action(3)
            target.health -= 3
            target.direction = random.randint(-1, 1)

    def draw(self):
        if self.flipped:
            pygame.draw.rect(main.screen, main.BLACK, self.rect)
            main.screen.blit(pygame.transform.flip(self.img, True, False), self.rect)
        else:
            pygame.draw.rect(main.screen, main.BLACK, self.rect)
            main.screen.blit(self.img, self.rect)

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            if self.type == 'player':
                self.update_action(8)   
            else:
                self.update_action(3)   
            return False
        else:
            return True