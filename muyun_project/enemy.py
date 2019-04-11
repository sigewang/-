import pygame
from random import *
class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self,ruler):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("pic/miniE.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width,self.height = ruler[0],ruler[1]
        self.speed = 2
        for i in range(7):
            self.rect.left, self.rect.top = i,i
    def update(self):
        self.rect=self.rect.move(self.speed,1)
        if self.rect.left<0 or self.rect.right>self.width:
            self.speed=-self.speed
        if self.rect.top>self.height:
            self.reset()
    def reset(self):
        self.rect.left, self.rect.top = randint(0,self.width - self.rect.width),randint(-5 * self.height,0)

class BigEnemy(pygame.sprite.Sprite):
    def __init__(self,ruler):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("pic/bigE.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width,self.height = ruler[0],ruler[1]
        self.speed = 1
        self.rect.left, self.rect.top = randint(0,self.width - self.rect.width),randint(-10 * self.height,0)
        # self.speed = 2
        # self.speedy = 1
    def update(self):
        # self.rect = self.rect.move(self.speedx,self.speedy)
        # if self.rect.left<0 or self.rect.right>self.width:
        #     self.speedx=-self.speedx
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()
    def reset(self):
        self.rect.left, self.rect.top = randint(0,self.width - self.rect.width),randint(-5 * self.height,0)
