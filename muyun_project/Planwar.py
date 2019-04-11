#-*-coding:utf-8-*-
"""
   个人尝试pygame第一个游戏
"""
import pygame,sys
from pygame.locals import *
import user
import enemy
import enemyBOSS
import bullet
pygame.init()
ruler = wigth,height =550,750
bg_one = "F:\muyun_project\pic/fillgroud.png"
screen = pygame.display.set_mode(ruler)
title = pygame.display.set_caption("Planwar")
bg_zero = pygame.image.load(bg_one)
def add_small_enemies(group1,group2,num):
    for i in range(num):
        e1 = enemy.SmallEnemy(ruler)
        group1.add(e1)
        group2.add(e1)

def add_big_enemies(group1,group2,num):
    for i in range(num):
        e2 = enemy.BigEnemy(ruler)
        group1.add(e2)
        group2.add(e2)
i = user.Nwang(ruler)
# def add_user_zidan(group1,num):
#     for en in range(num):
#         e3 = bullet.Bullet1(i.rect.midtop)
#         group1.add(e3)

# def main():
#生成角色

#角色子弹
# user_zidan = pygame.sprite.Group()
# add_user_zidan(user_zidan,4)
# user_zidan.draw(screen)
# user_zidan.update()
bullet1 = []
bullet1_index = 0
BULLET1_NUM = 4
for en in range(BULLET1_NUM):
    bullet1.append(bullet.Bullet1(i.rect.midtop))
    


#生成敌机汇总组
enemies = pygame.sprite.Group()

# samlldi = enemy.SmallEnemy(ruler)
small_enemies = pygame.sprite.Group()
add_small_enemies(small_enemies,enemies,10)
big_enemies = pygame.sprite.Group()
add_big_enemies(big_enemies,enemies,4)

clock = pygame.time.Clock()
#生成boss
Boss = enemyBOSS.Boss(ruler)

#用于延迟播放
delay = 100
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    #检测用户的键盘操作
    key_in = pygame.key.get_pressed()

    if key_in[K_w] or key_in[K_UP]:
        i.moveup()
    if key_in[K_s] or key_in[K_DOWN]:
        i.movedown()
    if key_in[K_a] or key_in[K_LEFT]:
        i.moveleft()
    if key_in[K_d] or key_in[K_RIGHT]:
        i.moveright()

    #boss移动
    Boss.Bmove()
    screen.blit(bg_zero,(0,0))
    #发射子弹
    if not(delay % 10):
        bullet1[bullet1_index].reset(i.rect.midtop)
        bullet1_index = (bullet1_index + 1) % BULLET1_NUM

    #检测子弹是否击中敌机
    for b in bullet1:
        if b.touches:
            b.move()
            screen.blit(b.image, b.rect)
            enemy_hit = pygame.sprite.spritecollide(b,enemies,False,pygame.sprite.collide_mask)
            if enemy_hit:
                b.touches = False
                for e in enemy_hit:
                    e.touches=False

    # small_enemies.draw(screen)
    # small_enemies.update()
    #绘制玩家
    #绘制玩家
    screen.blit(i.image,i.rect)
    #绘制敌机
    enemies.draw(screen)
    enemies.update()

    delay -= 1
    screen.blit(i.image,i.rect)
    #绘制boss
    screen.blit(Boss.image,Boss.rect)
    pygame.display.update()
    clock.tick(60)
# if __name__ == "__main__":
#     main()