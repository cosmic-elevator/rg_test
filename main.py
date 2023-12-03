import pygame

'''


테스트용 게임
------------------
필요한 것들 목록
- 음악 플레이 버튼
- 테스트용 음악 (주먹 쥐고)
- 음악 러닝타임 표시 기능
- 기본 노트 낙하 레인
- 박자마다 떨어지는 노트
- 마디마다 떨어지는 마디선
- 그 외...

지금 왜 어지러운지는 모르겠는데 아무튼 어지러워 죽을 것 같아요
살려줘어어어어ㅓㅓㅓㅓㅓㅓㅓ



'''





pygame.init()
pygame.mixer.init()


class Note(pygame.sprite.Sprite):
    def __init__(self, linenum, exact_hit_time):
        super(Note, self).__init__()
        self.linenum = linenum
        self.exact_hit_time = exact_hit_time
        self.image = pygame.image.load('purple_note.png')
        self.rect = self.image.get_rect()
        self.rect.x = 440
        self.rect.y = 0

    def drop(self):
        self.rect.y += 10
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))
        if self.rect.y >= 570:
            self.kill()
    


WIDTH = 1280
HEIGHT = 720
FPS = 60
SPEED = 10  # 1프레임당 내려오는 노트의 픽셀
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('rhythm game test')

smallfont = pygame.font.Font(None, 40)
mediumfont = pygame.font.Font(None, 50)
bigfont = pygame.font.Font(None, 80)

playbutton = pygame.image.load('playbutton.png')
pink_keybeam = pygame.image.load('pink_keybeam.png')
judgeline = pygame.Rect(WIDTH/2-100, HEIGHT/2, 200, 10)
pygame.mixer.music.load('test.wav')
MusicChannel = pygame.mixer.Channel(1)

clock = pygame.time.Clock()
music_start_time = 0
music_playtime = 0

notequeue = [Note(1, 1), Note(1, 2), Note(1, 3), Note(1, 4), Note(1, 5), Note(1, 6), Note(1, 7), Note(1, 8)]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 255)


def music_play():
    if not pygame.mixer.get_busy():
        MusicChannel.play(pygame.mixer.Sound('test.wav'))


def timing(note):
    key_press_time = pygame.time.get_ticks()
    if abs(key_press_time - note.exact_hit_time) >= 0 and abs(key_press_time - note.exact_hit_time) <= 400:
       SCREEN.blit(mediumfont.render("Perfect", True, YELLOW), (540, 400))

is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            music_play()
            music_start_time = pygame.time.get_ticks()

    SCREEN.fill(BLACK)
    pygame.draw.rect(SCREEN, GREEN, [WIDTH/2-200, HEIGHT/2+140, 400, 10])   # 540, 500, 200, 10

    for note in notequeue:
        if music_playtime/1000 >= note.exact_hit_time - (500 / (FPS * SPEED)):
            note.drop()

        
    if pygame.key.get_pressed()[pygame.K_d]:
        SCREEN.blit(pink_keybeam, (440, 0))
        timing(notequeue[0])
        #SCREEN.blit(mediumfont.render("Perfect", True, YELLOW), (560, 400))

    if music_start_time > 0 and music_playtime <= 8000:
        music_playtime = pygame.time.get_ticks() - music_start_time
    SCREEN.blit(bigfont.render(str(music_playtime/1000), True, WHITE), (20, 20))
        

    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()