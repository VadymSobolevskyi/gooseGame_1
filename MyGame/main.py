import random
import os

import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800 #800
WIDTH = 1200 #1200

FONT = pygame.font.SysFont('Verdana', 20)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0 , 0)
COLOR_BLUE = (0, 0, 255)
COLOR_RED = (255, 0, 0)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

player_size = (20, 20)
player = pygame.image.load('player.png').convert_alpha() # pygame.Surface(player_size)
# player.fill(COLOR_BLACK)
player_rect = pygame.Rect(40, (0.5*HEIGHT-150), *player_size)
player_move_down = [0, 5]
player_move_right = [5, 0]
player_move_up = [0, -5]
player_move_left = [-5, 0]

def create_cloud():
    cloud_size = (30, 30)
    cloud = pygame.image.load('cloud.png').convert_alpha() # pygame.Surface(cloud_size)
    # cloud.fill(COLOR_BLUE)
    cloud_rect = pygame.Rect(WIDTH, random.randint(0, (HEIGHT-cloud.get_height())), *cloud_size)
    cloud_move = [random.randint(-8, -4), 0]
    return [cloud, cloud_rect, cloud_move]

def create_bonus():
    bonus_size = (40, 40)
    bonus = pygame.image.load('bonus.png').convert_alpha() # pygame.Surface(bonus_size)
    # bonus.fill(COLOR_RED)
    bonus_rect = pygame.Rect(random.randint(0, WIDTH), 0, *bonus_size)
    bonus_rect = pygame.Rect(random.randint(0+15, (WIDTH-bonus.get_width())), -(bonus.get_height()), *bonus_size)
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]

CREATE_cloud = pygame.USEREVENT + 1
CREATE_BONUS = CREATE_cloud + 1
pygame.time.set_timer(CREATE_cloud, 2800)
pygame.time.set_timer(CREATE_BONUS, 3000)
CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

enemies = []
bonuses = []

score = 0
image_index = 0

playing = True
while playing:
    FPS.tick(120)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_cloud:
            enemies.append(create_cloud())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            for cloud in enemies:
                cloud[0] = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0

    # main_display.fill(COLOR_BLACK)
    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)
    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)
    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)
    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    for cloud in enemies:
        cloud[1] = cloud[1].move(cloud[2])
        main_display.blit(cloud[0], cloud[1])

        if player_rect.colliderect(cloud[1]):
            playing = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-50, 20))
    main_display.blit(player, player_rect)
    pygame.display.flip()       

    for cloud in enemies:
        if cloud[1].left < (0-int(cloud[0].get_width())):
            enemies.pop(enemies.index(cloud))

    for bonus in bonuses:
        if bonus[1].bottom > HEIGHT:
            bonuses.pop(bonuses.index(bonus))    
