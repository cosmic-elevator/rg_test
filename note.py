import pygame
from pygame.sprite import AbstractGroup
from settings import *

initialize_speed()

class Note(pygame.sprite.Sprite):
    def __init__(self, linenum, exact_hit_time):
        super(Note, self).__init__()
        self.linenum = linenum
        self.exact_hit_time = exact_hit_time
        self.image = pygame.image.load('img/purple_note.png')

        #rect를 어떻게 좀 해야 하는데...
        self.rect = self.image.get_rect()

        self.rect.x = 440 + (linenum - 1) * 100
        self.rect.y = 0


    def drop(self, spd):
        self.rect.y += spd



        
'''
## 롱노트의 꼬리를 별개의 객체로 만들어서 저장한다
class Note_Tail(pygame.sprite.Sprite):
    def __init__(self, linenum, exact_hit_time, tail_time):
        super(Note_Tail, self).__init__()
        self.linenum = linenum
        self.exact_hit_time = exact_hit_time
        #self.tail_time = tail_time
        self.tail_length = self.calculate_length(tail_time)
        self.image = pygame.transform.scale(pygame.image.load('img/note_tail.png'), (100, self.tail_length))
        
        self.rect = self.image.get_rect()
        self.rect.x = 440 + (linenum - 1) * 100
        self.rect.y = - self.tail_length


    def drop(self):
        self.rect.y += speed


    def boom(self):
        print('asdf')


    def calculate_length(self, tail_time):
        #롱노트 길이 구하는 함수 ~~~~~~~~
        #music_playtime/1000 >= note.exact_hit_time - (500 / (FPS * speed)):
        return tail_time * FPS * speed
'''
