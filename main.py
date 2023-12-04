import pygame
from settings import *

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

프로토타입 개발 완료! 이제 이걸 잘 조합해서 겜 하나 만들면 됩니다....

오늘 해야 할 것들
무엇을 할 것인가 ~ 우리 게임의 시급한 문제 ~
약간 팝픈뮤직 느낌?
메뉴 음악 / 로비 음악
아이캐치
판정 애니메이션
메인 화면 만들기 

>> 디자인은 나중에, 기능 구현을 먼저!! <<
필요한 기능


'''





pygame.init()
pygame.mixer.init()

smallfont = pygame.font.Font("font/kotra_hope.ttf", 30)
mediumfont = pygame.font.Font("font/kotra_hope.ttf", 45)
bigfont = pygame.font.Font("font/kotra_hope.ttf", 50)

class Note(pygame.sprite.Sprite):
    def __init__(self, linenum, exact_hit_time):
        super(Note, self).__init__()
        self.linenum = linenum
        self.exact_hit_time = exact_hit_time
        self.image = pygame.image.load('img/purple_note.png')
        self.rect = self.image.get_rect()
        self.rect.x = 440 + (linenum - 1) * 100
        self.rect.y = 0

    def drop(self):
        self.rect.y += SPEED
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))
        
    

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('rhythm game test')

is_running = True
gamemode = 0
songlist_cursor = 0

judgeline = pygame.Rect(WIDTH/2-100, HEIGHT/2, 200, 10)
pygame.mixer.music.load('test.wav')
MusicChannel = pygame.mixer.Channel(1)

clock = pygame.time.Clock()
music_start_time = 0
music_playtime = 0
global combo
combo = 0
global rate
rate = ""
global key_press_time
key_press_time = 0
global miss_check_time
miss_check_time = 0
global play_score
play_score = 0
# Perfect! / Great / Good / OK / Break / Miss
timing_count = [0, 0, 0, 0, 0, 0]


notequeue_1 = [Note(1, 1), Note(1, 2), Note(1, 3), Note(1, 4), Note(1, 5), Note(1, 6), Note(1, 7), Note(1, 8)]
notequeue_2 = [Note(2, 1), Note(2, 2)]
notequeue_3 = [Note(3, 3), Note(3, 4)]
notequeue_4 = [Note(4, 5), Note(4, 6)]



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
    global rate
    global combo
    global key_press_time
    key_press_time = pygame.time.get_ticks()
    diff_time = key_press_time - note.exact_hit_time * 1000 - music_start_time
    print(diff_time)
    
    if abs(diff_time) <= 30:
        print('Perfect!')
        rate = "Perfect!"
        remove_note(note)
        combo += 1
    elif abs(diff_time) <= 70:
        print('Great')
        rate = "Great"
        remove_note(note)
        combo += 1
    elif abs(diff_time) <= 100:
        print('Good')
        rate = "Good"
        remove_note(note)
        combo += 1
    elif abs(diff_time) <= 300:
        print('OK')
        rate = "OK"
        remove_note(note)
        combo = 0
    elif abs(diff_time) <= 800:
        print('Break')
        rate = "Break"
        remove_note(note)
        combo = 0
       

def miss_check(note):
    global combo
    global rate
    global miss_check_time
    if note.rect.y >= 570:
        print('Miss')
        combo = 0
        rate = "Miss"
        miss_check_time = pygame.time.get_ticks()
        remove_note(note)
        

def show_timing(rate):
    if pygame.time.get_ticks() - key_press_time < 250 or pygame.time.get_ticks() - miss_check_time < 250:      # 0.25초 동안 판정 보여주기 
        if rate == "Perfect!":
            SCREEN.blit(timing_perfect_img, (490, 400))
        elif rate == "Great":
            SCREEN.blit(timing_great_img, (490, 400))
        elif rate == "Good":
            SCREEN.blit(timing_good_img, (490, 400))
        elif rate == "OK":
            SCREEN.blit(timing_ok_img, (490, 400))
        elif rate == "Break":
            SCREEN.blit(timing_break_img, (490, 400))
        elif rate == "Miss":
            SCREEN.blit(timing_miss_img, (490, 400))


def show_combo():
    global combo


while is_running:
    if gamemode == 0:       ## 시작 화면
        SCREEN.blit(startscreen_img, (0, 0))
        SCREEN.blit(mediumfont.render("튜토리얼을 진행하려면 T,\n바로 플레이하려면 Space를 눌러주세요.", True, WHITE), (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    gamemode = 2    # T를 누르면 튜토리얼 플레이 화면으로 전환
                elif event.key == pygame.K_SPACE:
                    gamemode = 1
                
    if gamemode == 1:       ## 곡 선택 화면
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
        SCREEN.fill(GREEN)
        pygame.draw.rect(SCREEN, YELLOW, (0, 0, 1280, 70))
        SCREEN.blit(mediumfont.render("SONG SELECT", True, BLACK), (50, 15))
        pygame.draw.rect(SCREEN, WHITE, [130, 110, 380, 380])
        SCREEN.blit(mediumfont.render(song_info_list[songlist_cursor][0], True, BLACK), (150, 350))
        SCREEN.blit(smallfont.render(song_info_list[songlist_cursor][1], True, BLACK), (150, 400))
        SCREEN.blit(smallfont.render(song_info_list[songlist_cursor][2], True, BLACK), (150, 440))
        
        

    if gamemode == 2:       ## 플레이 화면
        SCREEN.fill(BLACK)
        pygame.draw.rect(SCREEN, YELLOW, [WIDTH/2-200, HEIGHT/2+140, 400, 10])   # 540, 500, 200, 10

        drop_notes()

        if pygame.key.get_pressed()[pygame.K_d]:
            SCREEN.blit(pink_keybeam, (440, 0))
        if pygame.key.get_pressed()[pygame.K_f]:
            SCREEN.blit(pink_keybeam, (540, 0))
        if pygame.key.get_pressed()[pygame.K_j]:
            SCREEN.blit(pink_keybeam, (640, 0))
        if pygame.key.get_pressed()[pygame.K_k]:
            SCREEN.blit(pink_keybeam, (740, 0))

            #SCREEN.blit(mediumfont.render(rate, True, YELLOW), (560, 400))

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

        show_timing(rate)
            
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
                
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False


    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()