import pygame, threading, queue
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
cover_gradient_bg = pygame.image.load('img/cover_gradient_bg.png')
playbutton = pygame.image.load('img/playbutton.png')
forwardbutton = pygame.image.load('img/forwardbutton.png')
backbutton = pygame.image.load('img/backbutton.png')

### Perfect! / Great / Good / OK / Break
keysounds_1 = [pygame.mixer.Sound('keysound/keysound_perfect_1.wav'), pygame.mixer.Sound('keysound/keysound_great_1.wav'), pygame.mixer.Sound('keysound/keysound_good_1.wav'),
               pygame.mixer.Sound('keysound/keysound_ok_1.wav'), pygame.mixer.Sound('keysound/keysound_break_1.wav')]

### 0: 곡 제목 / 1: 아티스트 이름 / 2: 장르명 / 3: 앨범커버 (380x380) / 4: 아이캐치 / 5: 곡 하이라이트 파일 / 6: 곡 전체 파일 / 7: 패턴 위치 문자열
song_info_list = [["주먹 쥐고", "sj", "Children's Song", pygame.image.load('img/jumuck_albumcover.png'), pygame.image.load('img/jumuck_eyecatch.png'), pygame.mixer.Sound('song/tutorial.wav'),  pygame.mixer.Sound('song/tutorial.wav'), "pattern/jumuck.bms"], 
                  ["Our Rhythmetric", "YTS", "Dance Rock", pygame.image.load('img/our_rhythmetric_albumcover.png'), pygame.image.load('img/our_rhythmetric_eyecatch.png'), pygame.mixer.Sound('song/our_rhythmetric.wav'), pygame.mixer.Sound('song/our_rhythmetric.wav'), None], 
                  ["Dreamcandy", "PerAl", "Kawaii Chiptune", pygame.image.load('img/dreamcandy_albumcover.png'), pygame.image.load('img/dreamcandy_eyecatch.png'), pygame.mixer.Sound('song/dreamcandy.wav'), pygame.mixer.Sound('song/dreamcandy.wav'), None]
                  ]
                #["HAPPY FESTA DAY!!", "Team Tomsquare", "Complextro", pygame.image.load('img/dreamcandy_albumcover.png')]
#eyecatch_list = [pygame.image.load('img/alpaca.jpeg')]

