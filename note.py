import pygame

speed = 15

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
        self.rect.y += speed
        
        
    