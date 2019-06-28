#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Імпортуємо бібліотеку pygame
import pygame
from  pygame import *
from random import *
import sys
from sys import *

# створюємо загальний  екран
window = pygame.display.set_mode((600, 630))
# завантажуєм космічний фон
bg = pygame.image.load("space.jpg")
# завантажеєм напис
pygame.display.set_caption("Arrow")
# завантажуєм фон меню
bg_menu = pygame.image.load("spaceship_fon1.jpg")
# створюєм ігрове полотно  на якому будуть відбуватись  ігрові події
screen = pygame.Surface((600, 600))
#створюєм полотно  для інформаційної стрічки
info_string=pygame.Surface((600, 30))

#створюємо окремий клас для ігрового  меню
class Menu:
    #створюємо меню
    def __init__(self, punkts = [400, 350, u'Punkt', (9, 0, 77), (11, 0, 77)]):
        self.punkts = punkts
    # функція  що відображає меню
    def render(self, pov, font, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                pov.blit(font.render(i[2], 1, i[4]), (i[0], i[1]-30))
            else:
                pov.blit(font.render(i[2], 1, i[3]), (i[0], i[1]-30))
    #функція  що обробляє дії гравця  в меню
    def menu(self):
        done = True
        font_menu = pygame.font.Font(None, 50)
        pygame.key.set_repeat(1,0)
        pygame.mouse.set_visible(True)
        punkt = 0
        while done:
            info_string.fill((0, 100, 200))
            info_string.blit(bg_menu, (0, 0))
            screen.fill((0, 100, 200))
            screen.blit(bg_menu, (0, 0))
            mp = pygame.mouse.get_pos()
            for i in self.punkts:
                if mp[0]>i[0] and mp[0]<i[0]+155 and mp[1]>i[1] and mp[1]<i[1]+50:
                    punkt = i[5]
            self.render(screen, font_menu, punkt)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    done=False
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        done=False
                    if e.key == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if e.key == pygame.K_DOWN:
                        if punkt < len(self.punkts)-1:
                            punkt += 1
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if punkt == 0:
                        done = False
                    elif punkt == 1:
                        done=False
                        sys.exit()
            window.blit(info_string, (0, 0))
            window.blit(screen, (0, 30))
            pygame.display.flip()
                
# клас спрайт  для ігрових об"єктів
class Sprite:
    def __init__(self, xpos, ypos, width, height, filename):
        self.x = xpos
        self.y = ypos
        self.w = width
        self.h = height
        self.bitmap=pygame.image.load(filename)
        self.bitmap.set_colorkey((255,255,255))
    #функція  для  відображення  ігрових об"єктів
    def render(self):
        screen.blit(self.bitmap, (self.x, self.y))

#функція  що  перевіряє чи стикаються  ігрові об"єкти
def intersect(x1,y1,w1,h1,x2,y2,w2,h2):
    if (x2+w2>=x1>=x2 and y2+h2>=y1>=y2):
        return True
    elif (x2+w2>=x1+w1>=x2 and y2+h2>=y1>=y2):
        return True
    elif (x2+w2>=x1>=x2 and y2+h2>=y1+h1>=y2):
        return True
    elif (x2+w2>=x1+w1>=x2 and y2+h2>=y1+h1>=y2):
        return 1
    else:
        return 0
# функція що вбиває космічний  корабель головного героя
def die(self):
    time.wait(1000)
    self.x = 0
    self.y = 560

# викликаємо font для створення поверхні  з текстом
pygame.font.init()
#створюємо об"єкт  з текстом з заданими параметрами
inf_font=pygame.font.Font(None, 32)

x=0
y=0
done = True
# створюємо  об"єкт  космічний корабель
ship = Sprite(0,560, 40, 40, "disk.png")
#створюємо об"єкт, що  буде  відображатись в  разі  остаточного програшу 
end = Sprite(0,0, 600, 600, "game_over.png")

ship.go_right = False
ship.go_down = False
ship.go_left = False
ship.go_up = False
ship.superforce=0

pygame.key.set_repeat(1, 0)
enemies = []
bullets = []
blasts = []
presents=[]
timer = pygame.time.Clock()
score=0
ship.lifes=3

# створюємо розділи меню і відображаємо його
punkts=[(270, 280, u'Game', (250, 250, 30), (250,30,250), 0), (280, 380, u'Quit', (250, 250, 30), (250,30,250), 1)]
game=Menu(punkts)
game.menu()

# цикл  безпосередньо  для  гри
while done:
    timer.tick(60)
    for e  in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key==pygame.K_ESCAPE):
            game.menu()
    screen.fill((50,50,50))
    screen.blit(bg, (0, 0))
    info_string.fill((45,80,45))

    #створюємо і  відображаємо  ворогів
    for i in range(5):
        if  len (enemies)<5:
            if randint(0, 10)>5:
                target = Sprite((randint(0, 560)),0, 40, 40, "goal2.png")
                target.type=0
            else:
                target = Sprite((randint(0, 560)),0, 40, 40, "goal.png")
                target.type=1
            target.go_right= True
            target.go_down = True
            target.ind=randint(0, 1000)
            #print(target.ind)
            enemies.append(target)
    #створюємо і відображаємо  бонуси
    for i in range(2):
        if  len (presents)<2:
            if randint(0, 10)>5:
                #print("randint", randint(0, 10))
                present = Sprite((randint(0, 560)),0, 40, 40, "life.png")
                present.life=1
            else:
                #print("randint", randint(0, 10))
                present = Sprite((randint(0, 560)),0, 40, 40, "super.png")
                present.life=0
            present.go_right= True
            present.go_down = True
            presents.append(present)
            


# блок  керування кораблем (рух + стрільба)
    for e  in pygame.event.get():
        if (e.type == pygame.KEYDOWN):
            if e.key == pygame.K_UP or e.key == pygame.K_w:
                ship.y-=5
                if  ship.y<0:
                    ship.y=0
            elif e.key == pygame.K_LEFT or  e.key == pygame.K_a:
                ship.x-=5
                if  ship.x<0:
                    ship.x=0
            elif e.key == pygame.K_RIGHT or  e.key == pygame.K_d:
                ship.x+=5
                if  ship.x>560:
                    ship.x=560 
            elif e.key == pygame.K_DOWN or e.key == pygame.K_s:
                ship.y+=5
                if  ship.y>560:
                    ship.y=560

        if e.type == pygame.MOUSEMOTION:
            pygame.mouse.set_visible(False)
            m=pygame.mouse.get_pos()
            if m[0]>0 and m[0]<560:
                ship.x=m[0]
            if m[1]>0 and m[1]<560:
                ship.y=m[1]

        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                if len(bullets)<5:
                    strela=Sprite(-50,650, 20, 20, "strila.png")
                    strela.push=False
                    bullets.append(strela)
                    strela.x=ship.x+10
                    strela.y=ship.y-30
                    strela.push=True
                    if ship.superforce>0:
                        ship.superforce=ship.superforce-5
                    print("ship.superforce", ship.superforce)
            

        if e.type == pygame.KEYDOWN:
            if e.key==pygame.K_SPACE:
                if len(bullets)<5:
                    strela=Sprite(-50,650, 15, 15, "strila.png")
                    strela.push=False
                    bullets.append(strela)
                    strela.x=ship.x+10
                    strela.y=ship.y-30
                    strela.push=True
                    if ship.superforce>0:
                        ship.superforce=ship.superforce-5
                    print("ship.superforce", ship.superforce)

# блок, що  задає рух ворогів
    for en in enemies:
        if en.go_down==True:
            en.y+=1
            if en.go_right==True:
                en.x +=1
            else:
                en.x-=1
            if  en.y>560:
                en.go_down=False
            if  en.x>560:
                en.go_right=False
            if en.x<0:
                en.go_right=True
        else:
            en.y-=1
            if en.go_right==True:
                en.x +=1
            else:
                en.x-=1
            if en.y<0:
                en.go_down=True
            if en.x<0:
                en.go_right=True

# блок,  що  задає рух бонусів        
    for p in presents:
        if p.go_down==True:
            p.y+=1
            if  p.y>560:
                p.go_down=False
        else:
            p.y-=1
            if p.y<0:
                p.go_down=True       

# блок, що задає рух снарядів
    for s in bullets:
        if s.y<0:
            s.push=False
        if s.push==False:
            s.x=-50
            s.y=650
            bullets.pop(0)
        else:
            s.y-=7
            if ship.superforce>0:
                s.x +=randint(-25, 25)
                s.y-=10

#блок  перевірки, чи перетинаються ігрові  об"єкти (вороги і корабель, бонуси і корабель, снаряди і  вороги)
    for en in enemies:
        if intersect(ship.x, ship.y, ship.w, ship.h,  en.x, en.y, en.w, en.h)==1:
            blast = Sprite(ship.x,ship.y, 80, 80, "blast.png")
            die(ship)
            blast.x=en.x
            blast.y=en.y
            en.x = randint(0, 560)
            en.y = -100
            die(ship)
            blasts.append(blast)
            print("len(blasts)", len(blasts))
            ship.lifes=ship.lifes-1
            ship.superforce=0 
        for s  in bullets:
            if intersect(s.x, s.y, s.w, s.h,  en.x, en.y, en.w, en.h)==1:
                blast = Sprite(ship.x,ship.y, 80, 80, "blast.png")
                blast.x=en.x
                blast.y=en.y
                s.x=-50
                s.y=650
                en.x = randint(0, 560)
                en.y = -100
                s.push=False
                enemies.remove(en)
                bullets.pop(bullets.index(s))
                blasts.append(blast)
                score=score+10
                
    for  p in presents:
        if intersect(ship.x, ship.y, ship.w, ship.h,  p.x, p.y, p.w, p.h)==1:
            if p.life==1:
                ship.lifes=ship.lifes+1
            else:
                ship.superforce=100
            p.x = randint(0, 560)
            p.y = -200

# на екрані  повинно  бути не більше 5 вибухів
    if  len(blasts)>5:
        blasts.pop(0)
# на екрані  повинно  бути не більше 2 бонусів
    if  len(presents)>2:
        presents.pop(0)

# блок  обновлення  ігрових об"єктів
    for  en  in enemies:
        en.render()
    for  s  in bullets:
        s.render()
    for  b  in blasts:
        b.render()
    for pr in presents:
        pr.render()   
    ship.render()

# якщо в корабля не залишилось  життів, гра  закінчується
    if  ship.lifes<1:
        end.render()
        done=False
    # обновляємо інфо про кількість  життів
    info_string.blit(inf_font.render(u"Кількість  життів: " +str(ship.lifes), 1, (255, 255,255)), (10, 5))
    #обновляємо інфо про ігровий  рахунок
    info_string.blit(inf_font.render(u"Рахунок: " +str(score), 1, (255, 255,255)), (250, 5))
    # малюємо заново іфнормаційну  стрічку
    window.blit(info_string, (0,0))
    #малюємо заново ігровий екран
    window.blit(screen, (0,30))
    # обновляємо весь екран заново
    pygame.display.flip()
    pygame.time.delay(5)
 
    
    
    

