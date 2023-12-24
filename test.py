import pygame

pygame.init()


WIDTH = 1280
HEIGHT = 720
FPS = 60

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Rhythmetric')
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN])

clock = pygame.time.Clock()


pink_keybeam = pygame.image.load('img/pink_keybeam.png').convert_alpha()


is_running = True

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        
    SCREEN.fill((0, 0, 0))
    if pygame.key.get_pressed()[pygame.K_d]:
        SCREEN.blit(pink_keybeam, (440, 0))
    if pygame.key.get_pressed()[pygame.K_f]:
        SCREEN.blit(pink_keybeam, (540, 0))
    if pygame.key.get_pressed()[pygame.K_j]:
        SCREEN.blit(pink_keybeam, (640, 0))
    if pygame.key.get_pressed()[pygame.K_k]:
        SCREEN.blit(pink_keybeam, (740, 0))


    pygame.display.update() 
    clock.tick(FPS)


pygame.quit()