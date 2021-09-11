import pygame
import main
from globals import SCREEN_WIDTH, bullet_img
from Game import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        # move bullet
            
        self.rect.x += (self.direction * self.speed)

        # check bounds
        # offscreen
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.kill()

        # check for collision with level
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        # player collisions
        if pygame.sprite.spritecollide(player, bullet_group, False) and player.alive:
            player.health -= 5
            self.kill()

        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False) and enemy.alive:
                enemy.health -= 40
                self.kill()