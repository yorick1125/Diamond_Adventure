import pygame
from Game import *
import Soldier
import HealthBar
import ItemBox
import Water
import Decoration
class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        self.level_length = len(data[0])
        # iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif tile == 9 or tile == 10:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif 11 <= tile <= 14:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 15:
                        if x < 1:
                            x = 1
                        player = Soldier(x * TILE_SIZE, y * TILE_SIZE, 2, 8, 'player', False, 5)
                        health_bar = HealthBar(130, 13, player.health, player.max_health)
                    elif tile == 16:
                        enemy = Soldier(x * TILE_SIZE, y * TILE_SIZE, 1.65, 4, 'enemy', True, 0)
                        enemy_group.add(enemy)
                    elif tile == 17: # ammo box
                        ammo_box = ItemBox('Ammo', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(ammo_box)
                    elif tile == 18:
                        health_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(health_box)
                    elif tile == 19: 
                        grenade_box = ItemBox('Grenade', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(grenade_box)
                    elif tile == 20:
                        exit = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)
                    elif tile == 21:
                        diamond = ItemBox('Diamond', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(diamond)
        return player, health_bar
    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])