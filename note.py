import pygame
from pygame.sprite import AbstractGroup

speed = 15
FPS = 60

class Note(pygame.sprite.Sprite):
    def __init__(self, linenum, exact_hit_time):
        super(Note, self).__init__()
        self.linenum = linenum
        self.exact_hit_time = exact_hit_time
        self.image = pygame.image.load('img/purple_note.png')

        #rect를 어떻게 좀 해야 하는데...
        self.rect = self.image.get_rect()

        self.rect.x = 440 + (linenum - 1) * 100
        self.rect.y = 0    # x좌표와 y좌표는 직사각형의 왼쪽 위 꼭짓점으로 정해짐 (...?) 그러면 


    def drop(self):
        self.rect.y += speed
        

    #def tail_drop(self):
        

    #def boom(self):
        

## 롱노트의 꼬리를 별개의 객체로 만들어서 저장한다
class Note_Tail(pygame.sprite.Sprite):
    def __init__(self, linenum, exact_hit_time, tail_time):
        super(Note_Tail, self).__init__()
        self.exact_hit_time = exact_hit_time
        self.tail_time = tail_time
        self.tail_length = self.calculate_length(self.tail_time)
        #transform.scale에서 문제가 생가는 듯. 
        #self.image = pygame.transform.scale(pygame.image.load('img/note_tail.png'), (100, self.tail_length))
        self.image = pygame.image.load('img/note_tail.png')
        #self.image = pygame.transform.scale(self.image, (100, self.length))
        
        self.rect = self.image.get_rect()
        self.rect.x = 440 + (linenum - 1) * 100
        self.rect.y = 0 - 100


    def drop(self):
        self.rect.y += speed


    def calculate_length(self, tail_time):
        #롱노트 길이 구하는 함수 ~~~~~~~~
        #music_playtime/1000 >= note.exact_hit_time - (500 / (FPS * speed)):
        return tail_time * (1 / FPS) * speed