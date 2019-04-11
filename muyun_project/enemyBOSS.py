import pygame
from random import *
class Boss(pygame.sprite.Sprite):
    def __init__(self,ruler):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("pic/boss1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width,self.height = ruler[0],ruler[1]
        self.rect.left,self.rect.top = (self.width -self.rect.width)//2,0
        self.speed = 1
    def Bmove(self):
        self.rect=self.rect.move(self.speed,0)
        if self.rect.left<0 or self.rect.right>self.width:
            self.speed=-self.speed