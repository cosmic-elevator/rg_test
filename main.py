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
        self.rect.x = 440 + (linenum - 1) * 100  #
        self.rect.y = 0

    def drop(self):
        self.rect.y += SPEED
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))
        
    


WIDTH = 1280
HEIGHT = 720
FPS = 60
SPEED = 10  # 1프레임당 내려오는 노트의 픽셀
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('rhythm game test')

smallfont = pygame.font.Font(None, 40)
mediumfont = pygame.font.Font(None, 50)
bigfont = pygame.font.Font(None, 80)

pink_keybeam = pygame.image.load('pink_keybeam.png')
judgeline = pygame.Rect(WIDTH/2-100, HEIGHT/2, 200, 10)
pygame.mixer.music.load('test.wav')
MusicChannel = pygame.mixer.Channel(1)

clock = pygame.time.Clock()
music_start_time = 0
music_playtime = 0
combo = 0

notequeue_1 = [Note(1, 1), Note(1, 2), Note(1, 3), Note(1, 4), Note(1, 5), Note(1, 6), Note(1, 7), Note(1, 8)]
notequeue_2 = [Note(2, 1), Note(2, 2)]
notequeue_3 = [Note(3, 3), Note(3, 4)]
notequeue_4 = [Note(4, 5), Note(4, 6)]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 255)


def music_play():
    if not pygame.mixer.get_busy():
        MusicChannel.play(pygame.mixer.Sound('test.wav'))


def remove_note(note):
    if note.linenum == 1:
        notequeue_1.remove(note)
    elif note.linenum == 2:
        notequeue_2.remove(note)
    elif note.linenum == 3:
        notequeue_3.remove(note)
    elif note.linenum == 4:
        notequeue_4.remove(note)


def drop_notes():
    for note in notequeue_1:
        if music_playtime/1000 >= note.exact_hit_time - (500 / (FPS * SPEED)):
            note.drop()
    for note in notequeue_2:
        if music_playtime/1000 >= note.exact_hit_time - (500 / (FPS * SPEED)):
            note.drop()
    for note in notequeue_3:
        if music_playtime/1000 >= note.exact_hit_time - (500 / (FPS * SPEED)):
            note.drop()
    for note in notequeue_4:
        if music_playtime/1000 >= note.exact_hit_time - (500 / (FPS * SPEED)):
            note.drop()


def timing(note):
    key_press_time = pygame.time.get_ticks()
    diff_time = key_press_time - note.exact_hit_time*1000 - music_start_time
    #print(diff_time)
    
    if abs(diff_time) <= 30:
        print('Perfect!')
        rate = "perfect"
        remove_note(note)
        combo += 1
        SCREEN.blit(mediumfont.render("Perfect!", True, YELLOW), (540, 400))
    elif abs(diff_time) <= 70:
        print('Great')
        rate = "great"
        remove_note(note)
        combo += 1
        SCREEN.blit(mediumfont.render("Great", True, YELLOW), (540, 400))
    elif abs(diff_time) <= 100:
        print('Good')
        rate = "good"
        remove_note(note)
        combo += 1
        SCREEN.blit(mediumfont.render("Good", True, YELLOW), (540, 400))
    elif abs(diff_time) <= 300:
        print('OK')
        rate = "ok"
        remove_note(note)
        combo = 0
        SCREEN.blit(mediumfont.render("OK", True, YELLOW), (540, 400))
    elif abs(diff_time) <= 800:
        print('Break')
        rate = "break"
        remove_note(note)
        combo = 0
        SCREEN.blit(mediumfont.render("Break", True, YELLOW), (540, 400))
       

def miss_check(note):
    if note.rect.y >= 570:
        print('Miss')
        combo = 0
        SCREEN.blit(mediumfont.render("Miss", True, YELLOW), (540, 400))
        remove_note(note)
        

is_running = True
while is_running:
    SCREEN.fill(BLACK)
    pygame.draw.rect(SCREEN, GREEN, [WIDTH/2-200, HEIGHT/2+140, 400, 10])   # 540, 500, 200, 10

    drop_notes()

    if pygame.key.get_pressed()[pygame.K_d]:
        SCREEN.blit(pink_keybeam, (440, 0))
    if pygame.key.get_pressed()[pygame.K_f]:
        SCREEN.blit(pink_keybeam, (540, 0))
    if pygame.key.get_pressed()[pygame.K_j]:
        SCREEN.blit(pink_keybeam, (640, 0))
    if pygame.key.get_pressed()[pygame.K_k]:
        SCREEN.blit(pink_keybeam, (740, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                music_play()
                music_start_time = pygame.time.get_ticks()
                
            if event.key == pygame.K_d:
                if music_start_time > 0:
                    try:
                        timing(notequeue_1[0])
                    except IndexError:
                        continue
            if event.key == pygame.K_f:
                if music_start_time > 0:
                    try:
                        timing(notequeue_2[0])
                    except IndexError:
                        continue
            if event.key == pygame.K_j:
                if music_start_time > 0:
                    try:
                        timing(notequeue_3[0])
                    except IndexError:
                        continue
            if event.key == pygame.K_k:
                if music_start_time > 0:
                    try:
                        timing(notequeue_4[0])
                    except IndexError:
                        continue
    
    if music_start_time > 0 and music_playtime <= 8000:
        music_playtime = pygame.time.get_ticks() - music_start_time
        if notequeue_1:                   
            miss_check(notequeue_1[0])
        if notequeue_2:                   
            miss_check(notequeue_2[0])
        if notequeue_3:                   
            miss_check(notequeue_3[0])
        if notequeue_4:                   
            miss_check(notequeue_4[0])
        
        

    SCREEN.blit(bigfont.render(str(music_playtime/1000), True, WHITE), (20, 20))
        

    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()