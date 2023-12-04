import pygame
pygame.init()

WIDTH = 1280
HEIGHT = 720
FPS = 60
SPEED = 10  # 1프레임당 내려오는 노트의 픽셀

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


pink_keybeam = pygame.image.load('img/pink_keybeam.png')
timing_perfect_img = pygame.image.load('img/timing_perfect_1.png')
timing_great_img = pygame.image.load('img/timing_great_1.png')
timing_good_img = pygame.image.load('img/timing_good_1.png')
timing_ok_img = pygame.image.load('img/timing_ok_1.png')
timing_miss_img = pygame.image.load('img/timing_miss_1.png')
timing_break_img = pygame.image.load('img/timing_break_1.png')
startscreen_img = pygame.image.load('img/alpaca.jpeg')

### 곡 제목 / 아티스트 이름 / 장르명
song_info_list = [["주먹 쥐고", "sj", "Children's Song"], ["Our Rhythmetric", "YTS", "Glide Dance"]]
eyecatch_list = [pygame.image.load('img/alpaca.jpeg')]
