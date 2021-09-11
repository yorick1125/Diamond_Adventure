import pygame
import button
import globals
import csv
import ScreenFade
import World
from globals import *

font = pygame.font.SysFont('Futura', 30)
world = World.World()
player = {}

start_game = False
start_intro = False
level = 0
bg_scroll = 0

# create sprite groups
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

# create buttons
start_button = button.Button(globals.SCREEN_WIDTH // 2 - 130, globals.SCREEN_HEIGHT // 2 - 150, globals.start_img, 1)
exit_button = button.Button(globals.SCREEN_WIDTH // 2 - 110, globals.SCREEN_HEIGHT // 2 + 50, globals.exit_img, 1)
restart_button = button.Button(globals.SCREEN_WIDTH // 2 - 114, globals.SCREEN_HEIGHT // 2 - 80, globals.restart_img, 2)

# create screen fades
intro_fade = ScreenFade.ScreenFade(1, BLACK, 20)
death_fade = ScreenFade.ScreenFade(2, PINK, 14)
victory_fade = ScreenFade.ScreenFade(2, BLUE, 14)

class Game():
    def __init__(self):
        self.quit = False
        self.gameover = False
        self.win = False



    def start(self):
        # tile map
        # create empty tile list
        world_data = []
        for row in range(ROWS):
            r = [-1] * COLUMNS
            world_data.append(r)
        # load in level data and create world
        with open(f'levels/level{globals.level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)
        world = World.World()
        player, health_bar = self.world.process_data(world_data)


    def start_menu(self):
        # draw menu
        screen.blit(title_screen_bg, (0, 0))
        if exit_button.draw(screen):
            quit = True
        if start_button.draw(screen):
            start_game = True
            start_intro = True
            return True
        else:
            return False



    def game_loop(self, player, world):
        clock.tick(FPS)

        if not self.win:
            draw_background()
            world.draw()
            # show ammo
            draw_text(f'Health: {player.health}', font, RED, 10, 15)
            self.health_bar.draw(player.health)
            draw_text(f'Grenades: {player.grenades_count}', font, RED, 10, 65)
            for i in range(player.grenades_count):
                screen.blit(grenade_img, (140 + (i * 10), 70))
            draw_text(f'Diamonds: {player.diamonds}', font, RED, 10, 115)
            for i in range(player.diamonds):
                screen.blit(pygame.transform.scale(diamond_img, (round(TILE_SIZE/2), round(TILE_SIZE/2))), (140 + (i * 20), 112))

            # update and draw groups
            bullet_group.update()
            bullet_group.draw(screen)

            grenade_group.update()
            grenade_group.draw(screen)

            explosion_group.update()
            explosion_group.draw(screen)

            item_box_group.update()
            item_box_group.draw(screen)

            water_group.update()
            water_group.draw(screen)

            decoration_group.update()
            decoration_group.draw(screen)

            exit_group.update()
            exit_group.draw(screen)


            # show intro 
            if self.start_intro:
                if self.intro_fade.fade():
                    start_intro = False
                    self.intro_fade.fade_counter = 0


            player.update()
            screen_scroll, level_complete = player.move()
            bg_scroll -= screen_scroll
            player.draw()
            player.check_alive()
            

            # check if player has completed the level
            if level_complete:
                start_intro = True
                level += 1
                bg_scroll = 0
                world_data = self.reset_level()
                if level <= MAX_LEVELS:
                    try:
                        # reload the world on the same level and recreate player
                        with open(f'levels/level{level}_data.csv', newline='') as csvfile:
                            reader = csv.reader(csvfile, delimiter=',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                        world = World.World()
                        player, health_bar = world.process_data(world_data)
                        player.moving_left = False
                        player.moving_right = False
                    except:
                        win = True


            if not player.alive:
                screen_scroll = 0
                self.enemy_group.empty()
                if self.death_fade.fade():
                    if self.restart_button.draw(screen):
                        self.death_fade.fade_counter = 0
                        start_intro = True
                        bg_scroll = 0
                        level = 0
                        world_data = self.reset_level()
                        # reload the world on the same level and recreate player
                        with open(f'levels/level{level}_data.csv', newline='') as csvfile:
                            reader = csv.reader(csvfile, delimiter=',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                        world = World.World()
                        player, health_bar = world.process_data(world_data)
                        player.moving_left = False
                        player.moving_right = False


            for enemy in self.enemy_group:
                enemy.ai()
                enemy.update()
                enemy.draw()


            if not player.alive:
                all_enemies_dead = True
                for enemy in self.enemy_group:
                    if enemy.alive:
                        all_enemies_dead = False
                        break
                if all_enemies_dead or len(enemy_group) == 0:
                    gameover = True
        else:
            if victory_fade.fade():
                victory_fade.fade_counter = 0
            screen.blit(victory_img, (SCREEN_WIDTH/2 - 150, SCREEN_HEIGHT/2 - 300))
            if exit_button.draw(screen):
                quit = True
            if restart_button.draw(screen):
                start_game = False
                win = False
                bg_scroll = 0
                level = 0
                world_data = self.reset_level()
                # reload the world on the same level and recreate player
                with open(f'levels/level{level}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World.World()
                player, health_bar = world.process_data(world_data)
                player.moving_left = False
                player.moving_right = False




            
        # Event Handling
        for event in pygame.event.get():
            # quit game
            if event.type == pygame.QUIT:
                quit = True
            # PLAYER ----------------------------
            # keyboard presses
            if player.alive:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quit = True
                    if event.key == pygame.K_a:
                        player.moving_left = True
                        player.flipped = True
                        player.update_action(2) # Run
                    if event.key == pygame.K_d:
                        player.moving_right = True
                        player.flipped = False
                        player.update_action(2) # Run
                    if event.key == pygame.K_w and player.alive:
                        player.jump = True
                        jump_fx.play()
                        player.jump_count += 1
                    if event.key == pygame.K_s and not player.in_air:
                        if player.moving_left or player.moving_right:
                            player.sliding = True
                            player.update_action(6) # Slide
                        else:
                            player.update_action(3) # Crouch
                    if event.key == pygame.K_SPACE and player.alive:
                        player.shooting = True
                    if event.key == pygame.K_q:
                        player.grenade = True
                    if event.key == pygame.K_SPACE:
                        player.update_action(1) # Attack
                        player.attacking = True

                # keyboard button released
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        player.moving_left = False
                        player.update_action(0) # Idle  
                    if event.key == pygame.K_d:
                        player.moving_right = False
                        player.update_action(0) # Idle
                    if event.key == pygame.K_s:
                        if player.sliding:
                            player.update_action(2)
                            player.sliding = False
                        else:
                            player.update_action(0)
                    if event.key == pygame.K_q:
                        player.grenade = False
                        player.grenade_thrown = False
                    if event.key == pygame.K_SPACE:
                        if player.moving_right or player.moving_left:
                            player.update_action(2) # running
                        else:
                            player.update_action(0) # Idle

                        player.attacking = False
        pygame.display.update()

    def reset_level(self):
        # delete groups
        enemy_group.empty()
        bullet_group.empty()
        grenade_group.empty()
        explosion_group.empty()
        item_box_group.empty()
        decoration_group.empty()
        water_group.empty()
        exit_group.empty()

        # create empty tile list
        data = []
        for row in range(ROWS):
            r = [-1] * COLUMNS
            data.append(r)

        return data