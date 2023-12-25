import pygame
from note import *
from patternparser import *
#from PIL import Image, ImageFilter, ImageEnhance


pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()
pygame.mixer.init()

WIDTH = 1280
HEIGHT = 720
#FPS = 60

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Rhythmetric')
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN])

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


pink_keybeam = pygame.image.load('img/pink_keybeam.png').convert_alpha()

startscreen_img = pygame.image.load('img/rhythmetric_main.png').convert()
cover_gradient_bg = pygame.image.load('img/cover_gradient_bg.png').convert_alpha()
black_alpha_bg = pygame.image.load('img/black_alpha_bg.png').convert_alpha()
white_alpha_bg = pygame.image.load('img/white_alpha_bg.png').convert_alpha()
playbutton = pygame.image.load('img/playbutton.png').convert_alpha()
forwardbutton = pygame.image.load('img/forwardbutton.png').convert_alpha()
backbutton = pygame.image.load('img/backbutton.png').convert_alpha()
tutorial_img = pygame.image.load('img/tutorial_img.png').convert_alpha()
ap_img = pygame.image.load('img/allperfect.png').convert_alpha()
fc_img = pygame.image.load('img/fullcombo.png').convert_alpha()
song_select_fx = pygame.mixer.Sound('fx/song_select_fx.wav')    # 효과음이 구림 ...

grade_img_list = []

timing_img_list = [pygame.image.load('img/timing_perfect_1.png').convert_alpha(), pygame.image.load('img/timing_great_1.png').convert_alpha(), pygame.image.load('img/timing_good_1.png').convert_alpha(),
                   pygame.image.load('img/timing_ok_1.png').convert_alpha(), pygame.image.load('img/timing_break_1.png').convert_alpha(), pygame.image.load('img/timing_miss_1.png').convert_alpha()]

### Perfect! / Great / Good / OK / Break
keysounds_1 = [pygame.mixer.Sound('fx/keysound_perfect_1.wav'), pygame.mixer.Sound('fx/keysound_great_1.wav'), pygame.mixer.Sound('fx/keysound_good_1.wav'),
               pygame.mixer.Sound('fx/keysound_ok_1.wav'), pygame.mixer.Sound('fx/keysound_break_1.wav')]

### 0: 곡 제목 / 1: 아티스트 이름 / 2: 장르명 / 3: 앨범커버 (380x380) / 4: 아이캐치 / 5: 곡 하이라이트 파일 / 6: 곡 전체 파일 / 7: 패턴 위치 문자열
song_info_list = [["주먹 쥐고", "sj", "Children's Song", pygame.image.load('img/jumuck_albumcover.png').convert(), pygame.image.load('img/jumuck_eyecatch.png').convert_alpha(), pygame.mixer.Sound('song/tutorial.wav'),  pygame.mixer.Sound('song/tutorial.wav'), "pattern/jumuck.bms"], 
                  ["Our Rhythmetric", "YTS", "Dance Rock", pygame.image.load('img/our_rhythmetric_albumcover.png').convert(), pygame.image.load('img/our_rhythmetric_eyecatch.png').convert_alpha(), pygame.mixer.Sound('song/our_rhythmetric_old.wav'), pygame.mixer.Sound('song/our_rhythmetric.wav'), None], 
                  ["Dreamcandy", "PerAl", "Kawaii Chiptune", pygame.image.load('img/dreamcandy_albumcover.png').convert(), pygame.image.load('img/dreamcandy_eyecatch.png').convert_alpha(), pygame.mixer.Sound('song/dreamcandy_old.wav'), pygame.mixer.Sound('song/dreamcandy.wav'), None]
                  ]
                #["HAPPY FESTA DAY!!", "Team Tomsquare", "Complextro", pygame.image.load('img/dreamcandy_albumcover.png')]
#eyecatch_list = [pygame.image.load('img/alpaca.jpeg')]

#print(song_info_list[0][6].get_length())

smallfont = pygame.font.Font("font/kotra_hope.ttf", 30)
mediumfont = pygame.font.Font("font/kotra_hope.ttf", 45)
bigfont = pygame.font.Font("font/kotra_hope.ttf", 50)
combofont = pygame.font.Font("font/dangam.ttf", 66)
resultscorefont = pygame.font.Font("font/dangam.ttf", 80)
resulttimingfont = pygame.font.Font("font/kotra_hope.ttf", 60)


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
playbutton_rect = pygame.Rect(260, 530, 120, 120)

#judgeline = pygame.Rect(WIDTH/2-200, HEIGHT/2+140, 400, 10) # 540, 500, 200, 10 / 전ㅔ는 WIDTH/2-100, HEIGHT/2, 200, 10
BgMusicChannel = pygame.mixer.Channel(1)
SoundFXChannel = pygame.mixer.Channel(2)
PlayingMusicChannel = pygame.mixer.Channel(3)

clock = pygame.time.Clock()
is_tutorial = False

global combo, max_combo, rate, key_press_time, miss_check_time, play_score, cur_pattern, timing_count, score_text, timing_text_list, is_ap, is_fc
cur_pattern = None

## 게임 플레이 변수를 초기화하는 함수
def play_init(cur_pattern_path):
    global combo, max_combo, rate, key_press_time, miss_check_time, play_score, cur_pattern, timing_count, music_start_time, music_playtime, is_ap, is_fc
    
    cur_pattern = Pattern(cur_pattern_path)
    combo = 0
    max_combo = 0
    rate = 6
    key_press_time = 0
    miss_check_time = 0
    play_score = 0
    music_start_time = 0
    music_playtime = 0
    # Perfect! / Great / Good / OK / Break / Miss
    timing_count = [0, 0, 0, 0, 0, 0]

    is_ap = False
    is_fc = False


## 곡 프리뷰를 반복 재생하는 함수
def preview_play(cursor):
    if gamemode == 1:
        if (not BgMusicChannel.get_busy() or BgMusicChannel.get_sound() != song_info_list[songlist_cursor][5]):
            BgMusicChannel.play(song_info_list[cursor][5])

## 커서에 해당하는 음악을 재생하는 함수
def music_play(cursor):
    PlayingMusicChannel.play(song_info_list[cursor][6])


## 커서에 해당하는 음악의 패턴을 불러오는 함수 pattern_load => play_init으로 통합. 
    #cur_pattern.noteq_1 = [Note(1, 1), Note(1, 2), Note(1, 3), Note(1, 4), Note(1, 5), Note(1, 6), Note(1, 7), Note(1, 8)]
    #cur_pattern.noteq_2 = [Note(2, 1.5), Note(2, 2.5)]
    #cur_pattern.noteq_3 = [Note(3, 3.5), Note(3, 4.5)]
    #cur_pattern.noteq_4 = [Note(4, 5), Note(4, 6)]

## 노트 큐에서 노트를 제거하는 함수
def remove_note(n):
        if n.linenum == 1:
            #notequeue_1.remove(note)
            cur_pattern.noteq_1.remove(n)
        elif n.linenum == 2:
            #notequeue_2.remove(note)
            cur_pattern.noteq_2.remove(n)
        elif n.linenum == 3:
            #notequeue_3.remove(note)
            cur_pattern.noteq_3.remove(n)
        elif n.linenum == 4:
            #notequeue_4.remove(note)
            cur_pattern.noteq_4.remove(n)


def remove_tail(tail):
        if tail.linenum == 1:
            cur_pattern.notetail_1.remove(tail)
        elif tail.linenum == 2:
            cur_pattern.notetail_2.remove(tail)
        elif tail.linenum == 3:
            cur_pattern.notetail_3.remove(tail)
        elif tail.linenum == 4:
            cur_pattern.notetail_4.remove(tail)

## 그냥 순수하게 노트 큐에 있는 노트를 떨어뜨리는 역할을 하는 함수.
        # 롱노트 테일을 추가해야 함!
def drop_notes():
    '''
    for tail in cur_pattern.notetail_1:
        if music_playtime/1000 >= tail.exact_hit_time - (500 / (FPS * speed)):
            tail.drop()
            SCREEN.blit(tail.image, (tail.rect.x, tail.rect.y))
    for tail in cur_pattern.notetail_2:
        if music_playtime/1000 >= tail.exact_hit_time - (500 / (FPS * speed)):
            tail.drop()
            SCREEN.blit(tail.image, (tail.rect.x, tail.rect.y))
    for tail in cur_pattern.notetail_3:
        if music_playtime/1000 >= tail.exact_hit_time - (500 / (FPS * speed)):
            tail.drop()
            SCREEN.blit(tail.image, (tail.rect.x, tail.rect.y))
    for tail in cur_pattern.notetail_4:
        if music_playtime/1000 >= note.exact_hit_time - (500 / (FPS * speed)):
            tail.drop()
            SCREEN.blit(tail.image, (tail.rect.x, tail.rect.y))
    '''
    #for note in notequeue_1:
    for note in cur_pattern.noteq_1:
        # FPS * speed = pixel/second, judgeline_pixel * second/pixel = 노트가 내려오는 시간
        if music_playtime/1000 >= note.exact_hit_time - (500 / (FPS * speed)):
            note.drop()
            #SCREEN.blit(note, (note.rect.x, note.rect.y))
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
    global rate, combo, key_press_time, play_score
    
    key_press_time = pygame.time.get_ticks()
    diff_time = key_press_time - note.exact_hit_time * 1000 - music_start_time
    print(diff_time)
    
    # 판정은 넉넉하게, 세부 판정(점수)를 짜게 (판정은 잘 나오니까 기분은 좋고 / 점수는 변별이 되고)
    if abs(diff_time) <= 30:
        print('Perfect!')
        rate = 0
        remove_note(note)
        combo += 1
        play_score += 900
        SoundFXChannel.play(keysounds_1[0])
        timing_count[0] += 1
    elif abs(diff_time) <= 60:
        print('Great')
        rate = 1
        remove_note(note)
        combo += 1
        play_score += 440
        SoundFXChannel.play(keysounds_1[1])
        timing_count[1] += 1
    elif abs(diff_time) <= 110:
        print('Good')
        rate = 2
        remove_note(note)
        combo += 1
        play_score += 210
        SoundFXChannel.play(keysounds_1[2])
        timing_count[2] += 1
    elif abs(diff_time) <= 210:
        print('OK')
        rate = 3
        remove_note(note)
        combo = 0
        play_score += 100
        SoundFXChannel.play(keysounds_1[3])
        timing_count[3] += 1
    elif abs(diff_time) <= 500:
        print('Break')
        rate = 4
        remove_note(note)
        combo = 0
        SoundFXChannel.play(keysounds_1[4])
        timing_count[4] += 1

def miss_check(n):
    global combo
    global rate
    global miss_check_time
    #diff_time = key_press_time - note.exact_hit_time * 1000 - music_start_time
    if n.rect.bottom >= 600:
        print('Miss')
        combo = 0
        rate = 5
        miss_check_time = pygame.time.get_ticks()
        timing_count[5] += 1
        if type(n) == Note:
            remove_note(n)
        elif type(n) == Note_Tail:
            remove_tail(n)
        

## 판정 이미지를 출력하는 함수 
def show_timing(rate):
    if pygame.time.get_ticks() - key_press_time < 250 or pygame.time.get_ticks() - miss_check_time < 250:
        try:      # 0.25초 동안 판정 보여주기 
            SCREEN.blit(timing_img_list[rate], (490, 400))
        except IndexError:
            pass


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


## 결과 화면 텍스트를 렌더하는 함수
def render_result_texts(grade, clearrate, score, perfect_num, great_num, good_num, ok_num, break_num, miss_num):
    global score_text, timing_text_list
    score_text = resultscorefont.render(str(score), True, WHITE)
    timing_text_list = [resulttimingfont.render(str(perfect_num), True, WHITE), resulttimingfont.render(str(great_num), True, WHITE), resulttimingfont.render(str(good_num), True, WHITE),
                        resulttimingfont.render(str(ok_num), True, WHITE), resulttimingfont.render(str(break_num), True, WHITE), resulttimingfont.render(str(miss_num), True, WHITE)]
    

## 튜토리얼을 출력하는 함수
def show_tutorial():
    if is_tutorial:
        #pygame.draw.rect(SCREEN, BLACK, (WIDTH/2-500, HEIGHT/2-250, 1000, 500))
        SCREEN.blit(black_alpha_bg, (0, 0))
        SCREEN.blit(tutorial_img, (30, 0))


while is_running:
    if gamemode == 0:       ## 시작 화면
        pygame.mixer.stop()
        is_tutorial = False
        SCREEN.blit(startscreen_img, (0, 0))
        start_text = mediumfont.render("튜토리얼을 진행하려면 T,바로 플레이하려면 Space를 눌러주세요.", True, BLACK)
        SCREEN.blit(start_text, start_text.get_rect(center=(WIDTH/2, 600)))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    is_tutorial = True
                    play_init(song_info_list[0][7])
                    song_selected_time = pygame.time.get_ticks()
                    gamemode = 2    # T를 누르면 튜토리얼 플레이 화면으로 전환
                elif event.key == pygame.K_SPACE:
                    gamemode = 1

                
    if gamemode == 1:       ## 곡 선택 화면
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # 곡 목록에서 선택했을 때
                for i in range(len(songlist_boxes)):
                    if songlist_boxes[i].collidepoint(pos):
                        songlist_cursor = i
                        
                if backbutton_rect.collidepoint(pos):
                    songlist_cursor = (songlist_cursor - 1) % len(song_info_list)

                if forwardbutton_rect.collidepoint(pos):
                    songlist_cursor = (songlist_cursor + 1) % len(song_info_list)

                if playbutton_rect.collidepoint(pos):
                    BgMusicChannel.stop()
                    SoundFXChannel.play(song_select_fx)
                    play_init(song_info_list[songlist_cursor][7])
                    gamemode = 2

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if is_tutorial:
                        is_tutorial = False
                    else:
                        gamemode = 0

                if event.key == pygame.K_SPACE:
                    if is_tutorial:
                        is_tutorial = False
                    else:
                        BgMusicChannel.stop()
                        SoundFXChannel.play(song_select_fx)
                        play_init(song_info_list[songlist_cursor][7])
                        gamemode = 2
  
                if event.key == pygame.K_1:
                    is_tutorial = True

                if event.key == pygame.K_2:
                    print('아직 구현하지 못했습니다.')
                    #gamemode = 4

                if event.key == pygame.K_3:
                    print('아직 구현하지 못했습니다.')
                    #gamemode = 5 (만든 사람들 크레딧)

                if event.key == pygame.K_UP:
                    songlist_cursor = (songlist_cursor - 1) % len(song_info_list)

                if event.key == pygame.K_DOWN:
                    songlist_cursor = (songlist_cursor + 1) % len(song_info_list)

                if event.key == pygame.K_RETURN:
                    BgMusicChannel.stop()
                    SoundFXChannel.play(song_select_fx)
                    play_init(song_info_list[songlist_cursor][7])
                    gamemode = 2

        SCREEN.blit(song_info_list[songlist_cursor][4], (0, 0))
        SCREEN.blit(black_alpha_bg, (0, 0))
        SCREEN.blit(white_alpha_bg, (80, 70))
        pygame.draw.rect(SCREEN, YELLOW, (0, 0, 1280, 80))
        SCREEN.blit(mediumfont.render("SONG SELECT", True, BLACK), (50, 15))
        SCREEN.blit(smallfont.render("1: 플레이 방법   2: 노트 낙하 속도 조절   3: 크레딧", True, GRAY), (770, 23))
        #pygame.draw.rect(SCREEN, RED, [130, 110, 380, 380])
        #pygame.draw.rect(SCREEN, GRAY, (80, 70, 480, 720))
        SCREEN.blit(song_info_list[songlist_cursor][3], (130, 110))
        SCREEN.blit(cover_gradient_bg, (130, 110))
        SCREEN.blit(mediumfont.render(song_info_list[songlist_cursor][0], True, WHITE), (150, 350))
        SCREEN.blit(smallfont.render(song_info_list[songlist_cursor][1], True, WHITE), (150, 400))
        SCREEN.blit(smallfont.render(song_info_list[songlist_cursor][2], True, WHITE), (150, 440))
        SCREEN.blit(playbutton, (260, 530))
        SCREEN.blit(backbutton, (130, 565))
        SCREEN.blit(forwardbutton, (435, 565))

        preview_play(songlist_cursor)

        for i in range(len(song_info_list)):
            if songlist_cursor == i:
                pygame.draw.rect(SCREEN, YELLOW, [640, (120*i+110), 560, 100])
                SCREEN.blit(smallfont.render(song_info_list[i][0], True, BLACK), (660, 120*i+125))
                SCREEN.blit(smallfont.render(song_info_list[i][1], True, BLACK), (660, 120*i+155))

            else:
                pygame.draw.rect(SCREEN, BLACK, [640, (120*i+110), 560, 100])
                SCREEN.blit(smallfont.render(song_info_list[i][0], True, WHITE), (660, 120*i+125))
                SCREEN.blit(smallfont.render(song_info_list[i][1], True, WHITE), (660, 120*i+155))

        show_tutorial()
        
    

    if gamemode == 2:       ## 플레이 화면
        SCREEN.blit(song_info_list[songlist_cursor][4], (0, 0))
        SCREEN.blit(black_alpha_bg, (0, 0))
        pygame.draw.rect(SCREEN, YELLOW, [WIDTH/2-200, HEIGHT/2+140, 400, 10])   # 540, 500, 200, 10
        # 나중에 bga / 아이캐치 / 기어 추가 

        pygame.event.pump()

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
                    PlayingMusicChannel.stop()
                    if is_tutorial:
                        is_tutorial = False
                    gamemode = 1

                if event.key == pygame.K_SPACE: 
                    if is_tutorial:
                        is_tutorial = False
                    elif music_playtime == 0:
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


        if music_start_time > 0:    # and music_playtime <= song_info_list[songlist_cursor][6].get_length() * 1000
            if cur_pattern:
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

                '''
                if cur_pattern.notetail_1:                   
                    miss_check(cur_pattern.notetail_1[0])
                if cur_pattern.notetail_2:                   
                    miss_check(cur_pattern.notetail_2[0])
                if cur_pattern.notetail_3:                   
                    miss_check(cur_pattern.notetail_3[0])
                if cur_pattern.notetail_4:                   
                    miss_check(cur_pattern.notetail_4[0])
                '''
            
            if music_playtime > song_info_list[songlist_cursor][6].get_length() * 1000 + 500 and music_playtime <= song_info_list[songlist_cursor][6].get_length() * 1000 + 2400:
                # 나중에 이미지 애니메이션으로 변경
                if timing_count[0] == 26:       # 나중에 변수로 변경
                    SCREEN.blit(combofont.render("All Perfect", True, WHITE), (0, 0))
                    is_ap = True
                elif max_combo == 26:
                    SCREEN.blit(combofont.render("Full combo", True, WHITE), (0, 0))
                    is_fc = True

            if music_playtime > song_info_list[songlist_cursor][6].get_length() * 1000 + 5000:
                render_result_texts(None, None, play_score, timing_count[0], timing_count[1], timing_count[2], timing_count[3], timing_count[4], timing_count[5])
                gamemode = 3

        #SCREEN.blit(bigfont.render(str(music_playtime/1000), True, WHITE), (20, 20))
        SCREEN.blit(bigfont.render("SCORE: " + str(play_score), True, WHITE), (50, 580))
        SCREEN.blit(bigfont.render("MAX COMBO: " + str(max_combo), True, WHITE), (50, 630))


        show_tutorial()

    if gamemode == 3:    # 리절트 창
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    BgMusicChannel.stop()
                    # 게임 오버 창?
                    gamemode = 1

        SCREEN.blit(song_info_list[songlist_cursor][4], (0, 0))
        SCREEN.blit(black_alpha_bg, (0, 0))
        # ui 가디자인 (아직 미완료)
        #SCREEN.blit(pygame.transform.scale(white_alpha_bg, (960, 720)), (160, 0))
        pygame.draw.rect(SCREEN, YELLOW, (0, 0, 1280, 80))
        SCREEN.blit(mediumfont.render("PLAY RESULT", True, BLACK), (50, 15))
        pygame.draw.rect(SCREEN, GREEN, (240, 100, 350, 350))
        #pygame.draw.rect(SCREEN, GRAY, (218, 465, 380, 60))
        if is_ap:
            SCREEN.blit(ap_img, (218, 465))
        elif is_fc:
            SCREEN.blit(fc_img, (218, 465))

        #pygame.draw.rect(SCREEN, WHITE, (240, 540, 350, 80)) 
        #pygame.draw.rect(SCREEN, YELLOW, (160, 660, 960, 30))
        #def draw_result_texts(grade, clearrate, score, perfect_num, great_num, good_num, ok_num, break_num, miss_num):
        SCREEN.blit(score_text, score_text.get_rect(center=(415, 580)))
        SCREEN.blit(smallfont.render("점수를 부스 담당 학생에게 알려 주세요!", True, WHITE), (500, 640))
            
        for i in range(len(timing_count)):
            SCREEN.blit(pygame.transform.scale(timing_img_list[i], (200, 40)), (690, 65*i+170))
            SCREEN.blit(timing_text_list[i], timing_text_list[i].get_rect(center=(1000, 65*i+193)))
            #pygame.draw.rect(SCREEN, WHITE, (920, 65*i+170, 100, 40))


    if gamemode == 4:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gamemode = 1
                if event.key == pygame.K_SPACE:
                    if not cur_pattern:
                        cur_pattern = Pattern('pattern/speedtest.bms')
                        music_start_time = pygame.time.get_ticks()
                if event.key == pygame.K_LEFT or event.key == pygame.K_DOWN:
                    speed -= 1
                if event.key == pygame.K_RIGHT or event.key == pygame.K_UP:
                    speed += 1

        SCREEN.fill(BLACK)
        pygame.mixer.stop()

        pygame.draw.rect(SCREEN, YELLOW, [WIDTH/2, HEIGHT/2+140, 200, 10])
        if pygame.key.get_pressed()[pygame.K_f]:
            SCREEN.blit(pink_keybeam, (590, 0))


        if music_start_time > 0:
            if cur_pattern.noteq_2:
                drop_notes()   
                miss_check(cur_pattern.noteq_2[0])



    pygame.display.update() 
    clock.tick(FPS)


pygame.quit()