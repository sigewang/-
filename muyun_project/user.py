import pygame
class Nwang(pygame.sprite.Sprite):
    def __init__(self,ruler):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("pic/nvwang.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width,self.height = ruler[0],ruler[1]
        self.rect.left,self.rect.top = (self.width - self.rect.width)//2,self.height-self.rect.height-50
        self.speed = 5
    def moveup(self):
        self.rect.top -= self.speed
        x=self.rect.top
        self.rect.top=[0,x][self.rect.top>0]
    def movedown(self):
        if self.rect.bottom < self.height-50:
            self.rect.top += self.speed
        else:
            self.rect.bottom = self.height-50
    def moveleft(self):
        self.rect.left -= self.speed
        x=self.rect.left
        self.rect.left=[0,x][self.rect.left>0]
    def moveright(self):
        if self.rect.right < self.width:
            self.rect.right += self.speed
        else:
            self.rect.right = self.width

