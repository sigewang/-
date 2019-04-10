import pygame,itertools,sys,time,random,math,os
from pygame.locals import *

class Point(object):
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    #X property
    def getx(self): return self.__x
    def setx(self, x): self.__x = x
    x = property(getx, setx)

    #Y property
    def gety(self): return self.__y
    def sety(self, y): self.__y = y
    y = property(gety, sety)

    def __str__(self):
        return "{X:" + "{:.0f}".format(self.__x) + \
            ",Y:" + "{:.0f}".format(self.__y) + "}"

'''class MySprite(pygame.sprite.Sprite):
    def __init__(self, target):
        pygame.sprite.Sprite.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.master_image = None
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
        self.direction = 0
        self.velocity = Point(0.0, 0.0)

    def load(self, filename, width, height, columns):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.rect = 0, 0, width, height
        self.columns = columns
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1

    def update(self, current_time, rate=60):
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time

        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = (frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame
'''


class MySprite(pygame.sprite.Sprite):

    def __init__(self,target):
        pygame.sprite.Sprite.__init__(self)  # 调用父类方法
        self.master_image = None
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
        self.direction = 0
        self.velocity = Point(0.0, 0.0)
        self.bullets = pygame.sprite.Group()
        self.dr_group = pygame.sprite.Group()
        self.drzd_group =pygame.sprite.Group()
        self.life = 0
        # X property

    def _getx(self):
        return self.rect.x

    def _setx(self, value):
        self.rect.x = value

    X = property(_getx, _setx)

    # Y property
    def _gety(self):
        return self.rect.y

    def _sety(self, value):
        self.rect.y = value

    Y = property(_gety, _sety)

    # position property
    def _getpos(self):
        return self.rect.topleft

    def _setpos(self, pos):
        self.rect.topleft = pos

    position = property(_getpos, _setpos)

    def load(self, filename, width, height, columns):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.rect = Rect(0, 0, width, height)
        self.columns = columns
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1

    def update(self, current_time, rate=30):
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time

        #
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame

    def __str__(self):
        return str(self.frame) + "," + str(self.first_frame) + \
               "," + str(self.last_frame) + "," + str(self.frame_width) + \
               "," + str(self.frame_height) + "," + str(self.columns) + \
               "," + str(self.rect)

    def shoot(self,arrow):
        self.bullets.add(arrow)

    def drupdate(self):
        dr_pos = random.randint(0,530),-70
        dr = dr_feiji(dr_pos)
        self.dr_group.add(dr)


def calc_velocity(Kw,Kd,Ks,Ka, vel=1.0):
    velocity = Point(0,0)
    if Kw == 1:  #上
        velocity.y = -vel
        if Ka == 1:
            velocity.x = -vel
        if Kd == 1:
            velocity.x = vel
    elif Kd == 1:  #右
        velocity.x = vel
        if Kw == 1:
            velocity.y = -vel
        if Ks == 1:
            velocity.y = vel
    elif Ks == 1:  #下
        velocity.y = vel
        if Ka == 1:
            velocity.x = -vel
        if Kd == 1:
            velocity.x = vel
    elif Ka == 1:  #左
        velocity.x = -vel
        if Kw == 1:
            velocity.y = -vel
        if Ks == 1:
            velocity.y = vel
    return velocity

#地图类
class MyMap(pygame.sprite.Sprite):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bg = pygame.image.load("chap04/blackroom1.png").convert_alpha()

    def map_rolling(self):
        if self.y > 800:
            self.y = -800
        else:
            self.y += 0.5

    def map_update(self):
        screen.blit(self.bg, (self.x, self.y))

    def set_pos(self,x, y):
        self.x = x
        self.y = y


# 子弹类，继承自Sprite类
class Bullet(pygame.sprite.Sprite):
    def __init__(self,zidan_pos,zdlx,zydx):#zydx = 作用对象
        # 调用父类的构造方法
        pygame.sprite.Sprite.__init__(self)
        # 设置属性
        if zdlx == 'player':
            self.image = pygame.image.load("chap04/playzidan.png").subsurface(pygame.Rect(0, 0, 42, 50))  # image属性：子弹图片
            self.speed_y = 20  # speed属性：子弹移动速度
        elif zdlx == 'drfeiji':
            self.image = pygame.image.load("chap04/drzd_01.png").subsurface(pygame.Rect(0, 0, 15, 15))    # image属性：子弹图片
            self.speed_y = random.randint(-4,-2)  # speed属性：子弹Y轴移动速度
            self.speed_x = 1    # speed属性：子弹X轴移动速度
        self.rect = self.image.get_rect()  # rect属性：矩形
        self.rect.topleft = zidan_pos  # 矩形左上角坐标
        self.zydx = zydx
        self.zdlx = zdlx
        self.zdscwz_x, self.zdscwz_y = zidan_pos
        self.player_x = player.X
    # 移动方法
    def update(self):
        # 修改子弹坐标
        if self.zdlx == 'drfeiji':
            if self.zdscwz_x<self.player_x:
                self.rect.top -= self.speed_y
                self.rect.left += self.speed_x
            elif self.zdscwz_x>self.player_x:
                self.rect.top -= self.speed_y
                self.rect.left -= self.speed_x
            else:
                self.rect.top -= self.speed_y
        elif self.zdlx == 'player':
            self.rect.top -= self.speed_y
        # 如果子弹移出屏幕上方，右方，左方，则销毁子弹对象
        if self.rect.top < -10 or self.rect.left >610 or self.rect.left<-10:
            self.kill()
        wjbjz = pygame.sprite.spritecollideany(player, drfeiji.drzd_group) #玩家被击中时给wjbjz赋值
        if wjbjz :
            if pygame.sprite.collide_circle_ratio(0.5)(player, wjbjz):
                player.life-=10
                drfeiji.drzd_group.remove(wjbjz)

    def __del__(self):
        if self.zydx == 'drfeiji':
            player_zdhh = NewBoom(screen)
            player_zdhh.load("chap04/player_zdhh.png", 40, 40, 4)
            player_zdhh.position = self.rect.left, self.rect.top
            if self.rect.top > -10:
                player_zdhh_group.add(player_zdhh)


# 敌机类，继承自Sprite类
class dr_feiji(pygame.sprite.Sprite):
    def __init__(self,dr_pos):
        # 调用父类的构造方法
        pygame.sprite.Sprite.__init__(self)
        # 设置属性
        self.image = pygame.image.load("chap04/dr-01.png").subsurface(pygame.Rect(0,0,70,70))  # image属性：飞机图片
        self.rect = self.image.get_rect()  # rect属性：矩形
        self.rect.topleft = dr_pos  # 矩形左上角坐标
        self.speed_y = random.randint(2,4)  # speed属性：敌人y轴移动速度
        self.speed_x = random.randint(1,3)  # speed属性：敌人x轴移动速度
        self.drms_sj = random.randint(1,3)#敌人行动模式随机
        self.drzd_group = pygame.sprite.Group() #敌人子弹精灵组

    # 移动方法
    def update(self):
        # 修改敌人坐标

        if self.drms_sj == 1:
            self.rect.top += self.speed_y
        elif self.drms_sj ==2:
            self.rect.left += self.speed_x
            self.rect.top += self.speed_y*1.5
        elif self.drms_sj ==3:
            self.rect.left += self.speed_x
            self.rect.top += 0.5*self.speed_y
        # 如果敌人移出屏幕下方，则销毁敌人对象
        if self.rect.top > 800:
            self.kill()
        if self.rect.left > 530:
            self.speed_x=-self.speed_x
        elif self.rect.left < 0:
            self.speed_x-=self.speed_x

        drpzzd = pygame.sprite.groupcollide(drfeiji.dr_group,playerzidan.bullets,False,False) #敌人碰到子弹
        if drpzzd:
            for n in drfeiji.dr_group:
                for m in playerzidan.bullets:
                    if pygame.sprite.collide_mask(n,m):
                        n.kill()
                        m.kill()

        wjboom = pygame.sprite.spritecollideany(player,drfeiji.dr_group)
        if wjboom:
            if pygame.sprite.collide_circle_ratio(0.5)(player, wjboom):
                player.life-=10
                drfeiji.dr_group.remove(wjboom)

        if drzdjg % 100 ==10:
            drzd = Bullet((self.rect.left + 26, self.rect.top + 70), 'drfeiji','player')
            drfeiji.drzd_group.add(drzd)

    def __del__(self):
        boom_x = self.rect.left
        boom_y = self.rect.top
        drboom = NewBoom(screen)
        drboom.load("chap04/boom.png", 70, 70, 6)
        drboom.position = boom_x,boom_y
        drboom_group.add(drboom)

# 爆炸精灵类，继承自Sprite类
class NewBoom(pygame.sprite.Sprite):
    def __init__(self,zidan_pos):
        # 调用父类的构造方法
        pygame.sprite.Sprite.__init__(self)
        # 设置属性
        self.master_image = None #爆炸图片
        self.frame = 0      #当前帧
        self.old_frame = -1     #上一帧
        self.frame_width = 1    #帧宽度
        self.frame_height = 1   #帧高度
        self.first_frame = 0    #第一帧
        self.last_frame = 0     #最后一帧
        self.columns = 1        #图片列数
        self.last_time = 0      #循环一次的时间

    def _getx(self):
        return self.rect.x

    def _setx(self, value):
        self.rect.x = value

    X = property(_getx, _setx)

    # Y property
    def _gety(self):
        return self.rect.y

    def _sety(self, value):
        self.rect.y = value

    Y = property(_gety, _sety)

    # position property
    def _getpos(self):
        return self.rect.topleft

    def _setpos(self, pos):
        self.rect.topleft = pos

    position = property(_getpos, _setpos)

    def load(self, filename, width, height, columns):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.rect = Rect(0, 0, width, height)
        self.columns = columns
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1

    def update(self, current_time, rate=30):
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
                self.kill()
            self.last_time = current_time

        #
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame

    def __str__(self):
        return str(self.frame) + "," + str(self.first_frame) + \
               "," + str(self.last_frame) + "," + str(self.frame_width) + \
               "," + str(self.frame_height) + "," + str(self.columns) + \
               "," + str(self.rect)

    def shoot(self,arrow):
        self.bullets.add(arrow)

    def drupdate(self):
        dr_pos = random.randint(400,530),0
        dr = dr_feiji(dr_pos)
        self.dr_group.add(dr)

def print_text(font, x, y, text, color=(255,255,255)):
    imgText = font.render(text, True, color)
    screen = pygame.display.get_surface()
    screen.blit(imgText, (x,y))

pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50,50)
screen = pygame.display.set_mode((600, 800))
pygame.display.set_caption("飞机大战")
font = pygame.font.Font(None, 36)
framerate = pygame.time.Clock()

#游戏开始界面图片
Start_image = pygame.image.load("chap04/Gameblackgroud.png").convert_alpha()

#精灵组
player_group = pygame.sprite.Group()
drboom_group = pygame.sprite.Group()
playerboom_group = pygame.sprite.Group()
player_zdhh_group = pygame.sprite.Group()#玩家子弹击中效果精灵组

#初始化玩家精灵
player = MySprite(screen)
player.load("chap04/feijif.png", 100,100, 5)
player.position = 250,600
player.life = 100
player_group.add(player)
vel = 5.0
Kw=Ks=Ka=Kd=0
#初始化地图
bg1 = MyMap(0,0)
bg2 = MyMap(0,800)
player_moving = False
#敌人爆炸
drboom = NewBoom(screen)
drboom.load("chap04/boom.png", 70, 70, 6)
#玩家爆炸
playerboom = NewBoom(screen)
playerboom.load("chap04/player_boom.png", 100, 100, 6)
playerboomjs = False
#敌人精灵
drfeiji = MySprite(screen)
#子弹精灵
playerzidan = MySprite(screen)
#子弹间隔
zidanjg = 0
#爆炸事件
boomtime = 0
#敌人间隔
drjg=0
#敌人子弹间隔
drzdjg=0


GameOver = False
GameStart =False

while True:
    if GameStart ==True:
        if GameOver == False:
            framerate.tick(60)
            ticks = pygame.time.get_ticks()
            zidanjg+=1
            drjg+=1
            drzdjg+=1
            if drzdjg == 400:
                drzdjg=0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                sys.exit()
            elif keys[K_w]:
                Kw=1
                player_moving = True
                if keys[K_a]:
                    Ka=1
                    Kw=1
                elif keys[K_d]:
                    Kd=1
                    Kw=1
            elif keys[K_s]:
                Ks=1
                player_moving = True
                if keys[K_a]:
                    Ka=1
                    Ks=1
                elif keys[K_d]:
                    Kd=1
                    Ks=1
            elif keys[K_a]:
                Ka=1
                player_moving = True
                if keys[K_w]:
                    Kw=1
                    Ka=1
                elif keys[K_s]:
                    Ks=1
                    Ka=1
            elif keys[K_d]:
                Kd=1
                player_moving = True
                if keys[K_w]:
                    Kw=1
                    Kd=1
                elif keys[K_s]:
                    Ks=1
                    Kd=1

            else:
                player_moving = False

            if Kw==1 or Ks==1:
                if Kd == 1:
                    player.first_frame = 0
                    player.last_frame = 1
                    if player.frame == player.last_frame:
                        player.first_frame = 1
                elif Ka == 1:
                    player.first_frame = 3
                    player.last_frame = 4
                    if player.frame == player.last_frame:
                         player.first_frame = 4
                else:
                    player.first_frame = player.last_frame = 2
            elif Kd==1:
                player.first_frame=0
                player.last_frame=1
                if player.frame == player.last_frame:
                    player.first_frame = 1
            elif Ka==1:
                player.first_frame =3
                player.last_frame = 4
                if player.frame == player.last_frame:
                    player.first_frame = 4

            if not player_moving:
                # 当停止按键（即人物停止移动的时候），停止更新动画帧
                player.last_frame = player.first_frame = 2
            else:
                player.velocity = calc_velocity(Kw,Kd,Ks,Ka,5.0)
                player.velocity.x *= 1.5
                player.velocity.y *= 1.5
                Kw = 0
                Ks = 0
                Ka = 0
                Kd = 0

            #绘制地图
            bg1.map_update()
            bg2.map_update()
            bg1.map_rolling()
            bg2.map_rolling()

            player_group.update(ticks,50)
            # 移动玩家
            if player_moving:
                player.X += player.velocity.x
                player.Y += player.velocity.y
                if player.X < 0:
                    player.X = 0
                elif player.X > 500:
                    player.X = 500
                if player.Y < 0:
                    player.Y = 0
                elif player.Y > 700:
                    player.Y = 700

            if zidanjg % 10 == 0:
                zidan_pos = player.X+30,player.Y-30
                arrow = Bullet(zidan_pos,'player','drfeiji')
                playerzidan.shoot(arrow)
                # 子弹移动
            playerzidan.bullets.update()  # 精灵组update时，会调用所有精灵的update方法


            if drjg % 100 ==0:
                drfeiji.drupdate()
                #生成敌机

            drfeiji.dr_group.update()
            drfeiji.drzd_group.update()

            drboom_group.update(ticks, 80)
            player_zdhh_group.update(ticks,80)


            player_group.draw(screen)
            playerzidan.bullets.draw(screen)
            drfeiji.dr_group.draw(screen)
            drfeiji.drzd_group.draw(screen)
            drboom_group.draw(screen)
            player_zdhh_group.draw(screen)

            #玩家血条
            pygame.draw.rect(screen, (50, 150, 50, 180), Rect(400, 775, player.life * 2, 25))
            pygame.draw.rect(screen, (100, 200, 100, 180), Rect(400, 775, 200, 25), 2)
            if player.life<=0:
                player.kill()
                playerboom.position=player.X,player.Y
                if playerboomjs ==False:
                    playerboom_group.add(playerboom)
                playerboom_group.update(ticks, 50)
                playerboom_group.draw(screen)
                if playerboom.frame >= playerboom.last_frame:
                    playerboomjs=True
            if playerboomjs==True:
                time.sleep(2)
                GameOver =True
                for n in drfeiji.dr_group:      #初始化敌人
                    n.kill()
                for n in drfeiji.drzd_group:    #初始化敌人子弹
                    n.kill()
                for n in drboom_group:          #初始化敌人爆炸
                    n.kill()
        else:
            framerate.tick(10)
            screen.fill((0,0,0))
            print_text(font, 200,400 , "G A M E   O V E R")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            ckeys = pygame.key.get_pressed()
            if ckeys[K_BACKSPACE]:
                player.life=100
                player.position = 250, 600
                player_group.add(player)
                GameOver = False
                playerboomjs=False
    else:
        framerate.tick(3)
        screen.blit(Start_image,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            keys = pygame.key.get_pressed()
            if keys[K_F1]:
                GameStart = True
    pygame.display.update()