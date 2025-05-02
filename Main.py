import pygame
import sys


def loadAssets():
    red = pygame.image.load('Graphics/red circle.png').convert_alpha( )
    blue = pygame.image.load('Graphics/blue circle.png').convert_alpha()
    outline = pygame.image.load('Graphics/circle outline.png').convert_alpha()

    new_size = (100, 100)
    resized_outline = pygame.transform.scale(outline, new_size)
    resized_red_circle = pygame.transform.scale(red, new_size)
    resized_blue_circle = pygame.transform.scale(blue, new_size)

    return resized_red_circle, resized_blue_circle, resized_outline


pygame.init()
height = 800
width = 600
clock = pygame.time.Clock()
display = pygame.display.set_mode((height, width))
pygame.display.set_caption('Rhythm Game')

assetLoader = loadAssets()
red_circle = assetLoader[0]
blue_circle = assetLoader[1]
outline = assetLoader[2]
red_y_pos = 0

red_rect = red_circle.get_rect()
red_rect.topleft = (200, red_y_pos)
outline_rect = outline.get_rect()
outline_rect.topleft = (200,400)

score = 0

background = pygame.Surface((height, width))
background.fill('White')

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                print("Pressed D")
            if event.key == pygame.K_f and red_rect.colliderect(outline_rect):
                print("Pressed F within correct Frame")
                points = max(0,100 - abs(outline_rect.y - red_rect.y))
                score += points
                print("Hit! +" + str(points))
                print(score)

            if event.key == pygame.K_j:
                print("Pressed J")
            if event.key == pygame.K_k:
                print("Pressed K")
    display.blit(background, (0, 0))
    display.blit(blue_circle, (0, 0))
    display.blit(outline, (0,400))
    display.blit(outline, (200, 400))
    display.blit(outline, (400, 400))
    display.blit(outline, (600, 400))
    red_y_pos += 5
    if red_y_pos > 650:
        red_y_pos = 0
    red_rect.y = red_y_pos
    display.blit(red_circle, (200, red_y_pos))
    pygame.display.update()
    clock.tick(60)



