import pygame
pygame.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Forest Levels')
clock = pygame.time.Clock()
FPS = 60
GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 16
COLUMNS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 22
MAX_LEVELS = 4

screen_scroll = 0
bg_scroll = 0
level = 0
font = pygame.font.SysFont('Futura', 30)
start_game = False
start_intro = False



# colors
BG = (144, 201, 120)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (235, 65, 54)


# load music and sounds
pygame.mixer.music.load('audio/music2.mp3')
pygame.mixer.music.set_volume(0)
#pygame.mixer.music.play(-1, 0.0, 0)

jump_fx = pygame.mixer.Sound('audio/jump.wav')
jump_fx.set_volume(0)

shot_fx = pygame.mixer.Sound('audio/shot.wav')
shot_fx.set_volume(0)

grenade_fx = pygame.mixer.Sound('audio/grenade.wav')
grenade_fx.set_volume(0)

# images
# store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

pine1_img = pygame.image.load('img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()


start_img = pygame.image.load('img/start_btn.png').convert_alpha()
exit_img = pygame.image.load('img/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('img/restart_btn.png').convert_alpha()
title_screen_bg = pygame.image.load('img/background/title-screen-background.jpg').convert_alpha()
victory_img =  pygame.image.load('img/icons/victory.png').convert_alpha()
victory_img = pygame.transform.scale(victory_img, (300, 70))
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()
health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha()
grenade_box_img = pygame.image.load('img/icons/grenade_box.png').convert_alpha()
diamond_img = pygame.image.load('img/icons/diamond.png').convert_alpha()
diamond_img = pygame.transform.scale(diamond_img, (TILE_SIZE, TILE_SIZE))
item_boxes = {
    'Health': health_box_img,
    'Ammo': ammo_box_img,
    'Grenade': grenade_box_img,
    'Diamond': diamond_img
}

def draw_background():
    screen.fill(BG)
    width = sky_img.get_width()
    for i in range(5):
        screen.blit(sky_img, (width * i - bg_scroll * 0.5, 0))
        screen.blit(mountain_img, (width * i - bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, (width * i - bg_scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, (width * i - bg_scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))

def draw_text(text, font, color, x, y):
    # drawing text
    img = font.render(text, 1, color)
    screen.blit(img, (x, y))
    
