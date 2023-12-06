import pygame
from note import *
from patternparser import *

'''

무엇을 할 것인가 ~ 우리 게임의 시급한 문제 ~
약간 팝픈뮤직 느낌?
메뉴 음악 / 로비 음악 / 버튼 입력 효과음이 필요하다 (사실 이게 게임의 맛을 살리는 요소라고 해도 과언이 아니다)
아이캐치
판정 애니메이션


'''





pygame.init()
pygame.mixer.init()

WIDTH = 1280
HEIGHT = 720
FPS = 60

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('rhythm game test')

WHITE = (245, 245, 245)
BLACK = (89, 89, 89)
GRAY = (120, 120, 120)
RED = (255, 0, 0)
GREEN = (94, 228, 148)
BLUE = (0, 0, 255)
SKYBLUE = (113, 179, 250)
YELLOW = (255, 214, 85)
PINK = (242, 130, 173)
LIGHT_PINK = (255, 198, 219)


pink_keybeam = pygame.image.load('img/pink_keybeam.png')
timing_perfect_img = pygame.image.load('img/timing_perfect_1.png')
timing_great_img = pygame.image.load('img/timing_great_1.png')
timing_good_img = pygame.image.load('img/timing_good_1.png')
timing_ok_img = pygame.image.load('img/timing_ok_1.png')
timing_miss_img = pygame.image.load('img/timing_miss_1.png')
timing_break_img = pygame.image.load('img/timing_break_1.png')
startscreen_img = pygame.image.load('img/rhythmetric_main.png')
cover_gradient_bg = pygame.image.load('img/cover_gradient_bg.png')
black_alpha_bg = pygame.image.load('img/black_alpha_bg.png')
white_alpha_bg = pygame.image.load('img/white_alpha_bg.png')
playbutton = pygame.image.load('img/playbutton.png')
forwardbutton = pygame.image.load('img/forwardbutton.png')
backbutton = pygame.image.load('img/backbutton.png')

### Perfect! / Great / Good / OK / Break
keysounds_1 = [pygame.mixer.Sound('keysound/keysound_perfect_1.wav'), pygame.mixer.Sound('keysound/keysound_great_1.wav'), pygame.mixer.Sound('keysound/keysound_good_1.wav'),
               pygame.mixer.Sound('keysound/keysound_ok_1.wav'), pygame.mixer.Sound('keysound/keysound_break_1.wav')]

### 0: 곡 제목 / 1: 아티스트 이름 / 2: 장르명 / 3: 앨범커버 (380x380) / 4: 아이캐치 / 5: 곡 하이라이트 파일 / 6: 곡 전체 파일 / 7: 패턴 위치 문자열
song_info_list = [["주먹 쥐고", "sj", "Children's Song", pygame.image.load('img/jumuck_albumcover.png'), pygame.image.load('img/jumuck_eyecatch.png').convert_alpha(), pygame.mixer.Sound('song/tutorial.wav'),  pygame.mixer.Sound('song/tutorial.wav'), "pattern/jumuck.bms"], 
                  ["Our Rhythmetric", "YTS", "Dance Rock", pygame.image.load('img/our_rhythmetric_albumcover.png'), pygame.image.load('img/our_rhythmetric_eyecatch.png').convert_alpha(), pygame.mixer.Sound('song/our_rhythmetric.wav'), pygame.mixer.Sound('song/our_rhythmetric.wav'), None], 
                  ["Dreamcandy", "PerAl", "Kawaii Chiptune", pygame.image.load('img/dreamcandy_albumcover.png'), pygame.image.load('img/dreamcandy_eyecatch.png').convert_alpha(), pygame.mixer.Sound('song/dreamcandy.wav'), pygame.mixer.Sound('song/dreamcandy.wav'), None]
                  ]
                #["HAPPY FESTA DAY!!", "Team Tomsquare", "Complextro", pygame.image.load('img/dreamcandy_albumcover.png')]
#eyecatch_list = [pygame.image.load('img/alpaca.jpeg')]

#print(song_info_list[0][6].get_length())

smallfont = pygame.font.Font("font/kotra_hope.ttf", 30)
mediumfont = pygame.font.Font("font/kotra_hope.ttf", 45)
bigfont = pygame.font.Font("font/kotra_hope.ttf", 50)
combofont = pygame.font.Font("font/dangam.ttf", 66)


is_running = True
gamemode = 0
songlist_cursor = 0
song_selected_time = 0
pos = (0, 0)
#speed = 10  # 1프레임당 내려오는 노트의 픽셀

songlist_boxes = []
for i in range(len(song_info_list)):
    songlist_boxes.append(pygame.Rect(640, (120*i+110), 560, 100))
backbutton_rect = pygame.Rect(130, 565, 75, 50)
forwardbutton_rect = pygame.Rect(435, 565, 75, 50)

judgeline = pygame.Rect(WIDTH/2-100, HEIGHT/2, 200, 10)
MusicChannel = pygame.mixer.Channel(1)
SoundFXChannel = pygame.mixer.Channel(2)

clock = pygame.time.Clock()
music_start_time = 0
music_playtime = 0
is_tutorial = False
global combo, max_combo, rate, key_press_time, miss_check_time, play_score, cur_pattern
combo = 0
max_combo = 0
rate = ""
key_press_time = 0
miss_check_time = 0
play_score = 0
cur_pattern = None
# Perfect! / Great / Good / OK / Break / Miss
timing_count = [0, 0, 0, 0, 0, 0]


notequeue_1 = [Note(1, 1), Note(1, 2), Note(1, 3), Note(1, 4), Note(1, 5), Note(1, 6), Note(1, 7), Note(1, 8)]
notequeue_2 = [Note(2, 1), Note(2, 2)]
notequeue_3 = [Note(3, 3), Note(3, 4)]
notequeue_4 = [Note(4, 5), Note(4, 6)]


## 곡 프리뷰를 반복 재생하는 함수
def preview_play(cursor):
    MusicChannel.play(song_info_list[cursor][5])

## 커서에 해당하는 음악을 재생하는 함수
def music_play(cursor):
    MusicChannel.play(song_info_list[cursor][6])


## 커서에 해당하는 음악의 패턴을 불러오는 함수
def pattern_load(cursor):
    global cur_pattern
    cur_pattern = Pattern(song_info_list[cursor][7])
    #cur_pattern.noteq_1 = [Note(1, 1), Note(1, 2), Note(1, 3), Note(1, 4), Note(1, 5), Note(1, 6), Note(1, 7), Note(1, 8)]
    #cur_pattern.noteq_2 = [Note(2, 1.5), Note(2, 2.5)]
    #cur_pattern.noteq_3 = [Note(3, 3.5), Note(3, 4.5)]
    #cur_pattern.noteq_4 = [Note(4, 5), Note(4, 6)]

## 노트 큐에서 노트를 제거하는 함수
def remove_note(note):
    if note.linenum == 1:
        #notequeue_1.remove(note)
        cur_pattern.noteq_1.remove(note)
    elif note.linenum == 2:
        #notequeue_2.remove(note)
        cur_pattern.noteq_2.remove(note)
    elif note.linenum == 3:
        #notequeue_3.remove(note)
        cur_pattern.noteq_3.remove(note)
    elif note.linenum == 4:
        #notequeue_4.remove(note)
        cur_pattern.noteq_4.remove(note)


## 그냥 순수하게 노트 큐에 있는 노트를 떨어뜨리는 역할을 하는 함수.
def drop_notes():
    #for note in notequeue_1:
    for note in cur_pattern.noteq_1:
        if music_playtime/1000 >= note.exact_hit_time - (500 / (FPS * speed)):
            note.drop()
            SCREEN.blit(note.image, (note.rect.x, note.rect.y))
    #for note in notequeue_2:
    for note in cur_pattern.noteq_2:
        if music_playtime/1000 >= note.exact_hit_time - (500 / (FPS * speed)):
            note.drop()
            SCREEN.blit(note.image, (note.rect.x, note.rect.y))
    #for note in notequeue_3:
    for note in cur_pattern.noteq_3:
        if music_playtime/1000 >= note.exact_hit_time - (500 / (FPS * speed)):
            note.drop()
            SCREEN.blit(note.image, (note.rect.x, note.rect.y))
    #for note in notequeue_4:
    for note in cur_pattern.noteq_4:
        if music_playtime/1000 >= note.exact_hit_time - (500 / (FPS * speed)):
            note.drop()
            SCREEN.blit(note.image, (note.rect.x, note.rect.y))
    

## 키를 누른 시간과 노트 시간의 차이인 오차 시간을 측정한 뒤, 판정을 결정하는 함수
def timing(note):
    global rate
    global combo
    global key_press_time
    key_press_time = pygame.time.get_ticks()
    diff_time = key_press_time - note.exact_hit_time * 1000 - music_start_time
    print(diff_time)
    
    if abs(diff_time) <= 20:
        print('Perfect!')
        rate = "Perfect!"
        remove_note(note)
        combo += 1
        SoundFXChannel.play(keysounds_1[0])
    elif abs(diff_time) <= 60:
        print('Great')
        rate = "Great"
        remove_note(note)
        combo += 1
        SoundFXChannel.play(keysounds_1[1])
    elif abs(diff_time) <= 110:
        print('Good')
        rate = "Good"
        remove_note(note)
        combo += 1
        SoundFXChannel.play(keysounds_1[2])
    elif abs(diff_time) <= 210:
        print('OK')
        rate = "OK"
        remove_note(note)
        combo = 0
        SoundFXChannel.play(keysounds_1[3])
    elif abs(diff_time) <= 800:
        print('Break')
        rate = "Break"
        remove_note(note)
        combo = 0
        SoundFXChannel.play(keysounds_1[4])

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
        

## 판정 이미지를 출력하는 함수 
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


## 콤보 폰트를 출력하는 함수 
def show_combo():
    global combo
    if pygame.time.get_ticks() - key_press_time < 250:
        combo_text = combofont.render(str(combo), True, WHITE)
        SCREEN.blit(combo_text, combo_text.get_rect(center=(WIDTH/2, 200)))


## 사용자의 최대 콤보를 체크하는 함수 
def check_max_combo():
    global combo
    global max_combo
    if combo > max_combo:
        max_combo = combo


while is_running:
    if gamemode == 0:       ## 시작 화면
        SCREEN.blit(startscreen_img, (0, 0))
        start_text = mediumfont.render("튜토리얼을 진행하려면 T,\n바로 플레이하려면 Space를 눌러주세요.", True, WHITE)
        SCREEN.blit(start_text, start_text.get_rect(center=(WIDTH/2, 600)))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    gamemode = 3    # T를 누르면 튜토리얼 플레이 화면으로 전환
                    is_tutorial = True
                    song_selected_time = pygame.time.get_ticks()
                elif event.key == pygame.K_SPACE:
                    gamemode = 1
                
    if gamemode == 1:       ## 곡 선택 화면
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i in range(len(songlist_boxes)):
                    if songlist_boxes[i].collidepoint(pos):
                        songlist_cursor = i
                        
                if backbutton_rect.collidepoint(pos):
                    songlist_cursor = (songlist_cursor - 1) % len(song_info_list)

                if forwardbutton_rect.collidepoint(pos):
                    songlist_cursor = (songlist_cursor + 1) % len(song_info_list)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gamemode = 0

                if event.key == pygame.K_UP:
                    songlist_cursor = (songlist_cursor - 1) % len(song_info_list)

                if event.key == pygame.K_DOWN:
                    songlist_cursor = (songlist_cursor + 1) % len(song_info_list)

        #SCREEN.fill(BLACK)
        SCREEN.blit(song_info_list[songlist_cursor][4], (0, 0))
        SCREEN.blit(black_alpha_bg, (0, 0))
        pygame.draw.rect(SCREEN, YELLOW, (0, 0, 1280, 70))
        SCREEN.blit(mediumfont.render("SONG SELECT", True, BLACK), (50, 15))
        #pygame.draw.rect(SCREEN, RED, [130, 110, 380, 380])
        #pygame.draw.rect(SCREEN, GRAY, (80, 70, 480, 720))
        SCREEN.blit(white_alpha_bg, (80, 70))
        SCREEN.blit(song_info_list[songlist_cursor][3], (130, 110))
        SCREEN.blit(cover_gradient_bg, (130, 110))
        SCREEN.blit(mediumfont.render(song_info_list[songlist_cursor][0], True, WHITE), (150, 350))
        SCREEN.blit(smallfont.render(song_info_list[songlist_cursor][1], True, WHITE), (150, 400))
        SCREEN.blit(smallfont.render(song_info_list[songlist_cursor][2], True, WHITE), (150, 440))
        SCREEN.blit(playbutton, (260, 530))
        SCREEN.blit(backbutton, (130, 565))
        SCREEN.blit(forwardbutton, (435, 565))

        for i in range(len(song_info_list)):
            if songlist_cursor == i:
                pygame.draw.rect(SCREEN, YELLOW, [640, (120*i+110), 560, 100])
                SCREEN.blit(smallfont.render(song_info_list[i][0], True, BLACK), (660, 120*i+125))
                SCREEN.blit(smallfont.render(song_info_list[i][1], True, BLACK), (660, 120*i+155))
                if not MusicChannel.get_busy() or MusicChannel.get_sound() != song_info_list[songlist_cursor][5]:
                    preview_play(songlist_cursor)
            else:
                pygame.draw.rect(SCREEN, BLACK, [640, (120*i+110), 560, 100])
                SCREEN.blit(smallfont.render(song_info_list[i][0], True, WHITE), (660, 120*i+125))
                SCREEN.blit(smallfont.render(song_info_list[i][1], True, WHITE), (660, 120*i+155))
        
    
    if gamemode == 2:       ## 아이캐치
        if pygame.time.get_ticks() - song_selected_time >= 1500:
            gamemode = 3    
        else:
            SCREEN.blit(song_info_list[songlist_cursor][4], (0, 0))

    if gamemode == 3:       ## 플레이 화면
        SCREEN.blit(song_info_list[songlist_cursor][4], (0, 0))
        SCREEN.blit(black_alpha_bg, (0, 0))
        pygame.draw.rect(SCREEN, YELLOW, [WIDTH/2-200, HEIGHT/2+140, 400, 10])   # 540, 500, 200, 10
        # 나중에 bga / 아이캐치 / 기어 추가 


        if pygame.key.get_pressed()[pygame.K_d]:
            SCREEN.blit(pink_keybeam, (440, 0))
        if pygame.key.get_pressed()[pygame.K_f]:
            SCREEN.blit(pink_keybeam, (540, 0))
        if pygame.key.get_pressed()[pygame.K_j]:
            SCREEN.blit(pink_keybeam, (640, 0))
        if pygame.key.get_pressed()[pygame.K_k]:
            SCREEN.blit(pink_keybeam, (740, 0))

        if not music_start_time:
            beforeplay_text = mediumfont.render("Space를 눌러 시작하세요!", True, WHITE)
            SCREEN.blit(beforeplay_text, beforeplay_text.get_rect(center=(WIDTH/2, HEIGHT/2)))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gamemode = 1

                if event.key == pygame.K_SPACE:
                    if not pygame.mixer.get_busy():
                        if not cur_pattern:
                            pattern_load(songlist_cursor)
                            music_play(songlist_cursor)
                            music_start_time = pygame.time.get_ticks()
                            
                if event.key == pygame.K_d:
                    if music_start_time > 0:
                        try:
                            timing(cur_pattern.noteq_1[0])
                        except IndexError:
                            continue
                if event.key == pygame.K_f:
                    if music_start_time > 0:
                        try:
                            timing(cur_pattern.noteq_2[0])
                        except IndexError:
                            continue
                if event.key == pygame.K_j:
                    if music_start_time > 0:
                        try:
                            timing(cur_pattern.noteq_3[0])
                        except IndexError:
                            continue
                if event.key == pygame.K_k:
                    if music_start_time > 0:
                        try:
                            timing(cur_pattern.noteq_4[0])
                        except IndexError:
                            continue


        if music_start_time > 0 and music_playtime <= song_info_list[songlist_cursor][6].get_length() * 1000:
            drop_notes()
            show_timing(rate)
            show_combo()
            check_max_combo()

            music_playtime = pygame.time.get_ticks() - music_start_time
            if cur_pattern.noteq_1:                   
                miss_check(cur_pattern.noteq_1[0])
            if cur_pattern.noteq_2:                   
                miss_check(cur_pattern.noteq_2[0])
            if cur_pattern.noteq_3:                   
                miss_check(cur_pattern.noteq_3[0])
            if cur_pattern.noteq_4:                   
                miss_check(cur_pattern.noteq_4[0])
                
                

        SCREEN.blit(bigfont.render(str(music_playtime/1000), True, WHITE), (20, 20))
        SCREEN.blit(bigfont.render("SCORE: " + str(play_score), True, WHITE), (50, 580))
        SCREEN.blit(bigfont.render("MAX COMBO: " + str(max_combo), True, WHITE), (50, 630))

    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()