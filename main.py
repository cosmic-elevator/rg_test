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

playbutton = pygame.image.load('playbutton.png')
pygame.mixer.music.load('test.wav')
MusicChannel = pygame.mixer.Channel(1)

WIDTH = 1280
HEIGHT = 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('rhythm game test')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 255)


def music_play():
    if not pygame.mixer.get_busy():
        MusicChannel.play(pygame.mixer.Sound('test.wav'))

SCREEN.fill(BLACK)
SCREEN.blit(playbutton, (0, 0))
pygame.display.flip()

is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            music_play()


pygame.quit()