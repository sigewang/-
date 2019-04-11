import pygame

class Bullet1(pygame.sprite.Sprite):
    def __init__(self,weizhi):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("pic/zidan0.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left , self.rect.top = weizhi
        self.speed = 12
        self.touches = True
        self.mask = pygame.mask.from_surface(self.image)
    
    def move(self):
        self.rect.top = self.rect.top - self.speed

        if self.rect.top<0:
            self.touches = False
    def reset(self,weizhi):
        self.rect.left , self.rect.top = weizhi
        self.touches = True
