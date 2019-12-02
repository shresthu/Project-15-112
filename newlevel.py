def main():
    import pygame as pg
    import random
    import tkinter
    from tkinter import messagebox
#_________________________________________________________________________________________________________________________________
#initializes the constants
    vec = pg.math.Vector2
    PLAYER_ACC = 0.5
    PLAYER_FRICTION = -0.17
    WIDTH = 750
    HEIGHT = 500
    PLATFORM_LIST = [(WIDTH/2 -50 , HEIGHT *(3/4) ,78 ,20),
                     (350,200,78,20),(175,300,78,20)
                     ,(550,300,78,20)]
    smallpimage=pg.image.load("standing-2.png")
    smallpimage=pg.transform.scale(smallpimage,(25,19))
#______________________________________________________________________________________________________________________________
    class Player(pg.sprite.Sprite):
        def __init__(self,main):
            pg.sprite.Sprite.__init__(self)
            self.game=main
            self.image=pg.image.load("standing-2.png")
            self.rect = self.image.get_rect() 
            self.rect.center = (WIDTH / 2, HEIGHT / 2)
            self.pos = vec(WIDTH-50,50)
            self.vel = vec(0, 0)
            self.acc = vec(0, 0)
            self.facing =1
            self.lives=4
            self.hidden=False
            self.hide_timer = pg.time.get_ticks()
            
        def update(self):
            self.acc = vec(0, 0.8)
            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT]:
                self.facing=-1
                self.image = pg.image.load("standing-2.png")
                self.image = pg.transform.flip(self.image, True, False)
                self.acc.x = -(PLAYER_ACC +0.2)
            if keys[pg.K_RIGHT]:
                self.facing=1
                self.image=pg.image.load("standing-2.png")
                self.acc.x = (PLAYER_ACC +0.2)

            self.acc.x += self.vel.x * PLAYER_FRICTION
            self.vel += self.acc
            self.pos += self.vel + (0.5 * self.acc)
            if self.pos.x > WIDTH:
                self.pos.x = WIDTH
            if self.pos.x < 0:
                self.pos.x = 0
            self.rect.midbottom = self.pos
            if self.hidden and (pg.time.get_ticks() - self.hide_timer) >1000:
                self.hidden = False
                self.pos = (WIDTH-50,50)

        def jump(self):
            self.rect.x += 1
            hits = pg.sprite.spritecollide(self,self.game.platforms,False)
            self.rect.x -= 1
            if hits:
                self.vel.y= -15
                
        def shoot(self):
            bullet=Bullet(self.rect.centerx,self.rect.centery)
            self.game.all_sprites.add(bullet)
            self.game.bullets.add(bullet)

        def hshoot(self):
            bullet=hBullet(self.rect.centerx,self.rect.centery,self.facing)
            self.game.all_sprites.add(bullet)
            self.game.bullets.add(bullet)
            
        def hide(self):
            self.hidden=True
            self.hide_timer = pg.time.get_ticks()
            self.pos = vec(1000,1000)
            

    class hBullet(pg.sprite.Sprite):
        def __init__(self,x,y,facing):
            pg.sprite.Sprite.__init__(self)
            self.image = pg.image.load("bulletr.png")
            self.image = pg.transform.scale(self.image,(15,10))
            self.rect = self.image.get_rect()
            self.rect.bottom=y
            self.rect.centerx =x
            self.speedx = 5
            self.facing = facing
            
        def update(self):
            if self.facing == 1:
                self.rect.x += self.speedx
            if self.facing == -1:
                self.rect.x -= self.speedx
            if self.rect.bottom <0:
                self.kill()
            if self.rect.left>WIDTH:
                self.kill()
            
    class Flames(pg.sprite.Sprite):
        def __init__(self,x,y):
            pg.sprite.Sprite.__init__(self)
            self.image=pg.image.load("flamesn.png")
            self.image = pg.transform.scale(self.image,(50,50))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
    class Explosion(pg.sprite.Sprite):
        def __init__(self,center,lst):
            pg.sprite.Sprite.__init__(self)
            self.lst=lst
            self.image=self.lst[0]
            self.image=pg.transform.scale(self.image,(60,60))
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.frame =0
            self.last_update = pg.time.get_ticks()
            self.frame_rate =50
            
        def update(self):
            now=pg.time.get_ticks()
            if now-self.last_update > self.frame_rate:
                self.last_update =now
                self.frame +=1
                if self.frame == len(self.lst):
                    self.kill()
                else:
                    center = self.rect.center
                    self.image = self.lst[self.frame]
                    self.image=pg.transform.scale(self.image,(60,60))
                    self.rect = self.image.get_rect()
                    self.rect.center = center
            
    class Platform(pg.sprite.Sprite):
        def __init__(self,x,y,w,h):
            pg.sprite.Sprite.__init__(self)
            self.image=pg.image.load("cloudsn1.png")
            self.image = pg.transform.scale(self.image,(w,h))
            self.rect = self.image.get_rect()
            self.rect.x=x
            self.rect.y=y

    class FGate(pg.sprite.Sprite):
        def __init__(self):
            pg.sprite.Sprite.__init__(self)
            self.image = pg.image.load("door.png")
            self.image = pg.transform.scale(self.image,(40,35))
            self.rect = self.image.get_rect()
            self.rect.x = 0
            self.rect.y = HEIGHT-115

    class Enemy(pg.sprite.Sprite):
        def __init__(self,main):
            pg.sprite.Sprite.__init__(self)
            self.game = main
            self.image = pg.image.load("dragonn.png")
            self.image = pg.transform.scale(self.image,(20,30))
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(WIDTH//2)
            self.rect.y = random.randrange(55,75)
            self.speedx=3
            self.speedy=1
            
        def update(self):
            if self.rect.x < WIDTH and self.rect.x > 0:
                if self.rect.x >0: 
                    self.rect.x += self.speedx
                if self.rect.y > 50 :
                    self.rect.y += self.speedy
                if self.rect.left==0:
                    self.speedx =2
                    self.rect.x += self.speedx
                if (self.rect.x + 30) == WIDTH:
                    self.speedx=-2
                    self.rect.x += self.speedx
                if self.rect.bottom == 150:
                    self.speedy=-1
                    self.rect.y += self.speedy
                if self.rect.top == 50:
                    self.speedy =1
                    self.rect.y += self.speedy
                    
    class wEnemy(pg.sprite.Sprite):
        def __init__(self):
            pg.sprite.Sprite.__init__(self)
            self.image = pg.image.load("enemyn.png")
            self.image = pg.transform.scale(self.image,(20,30))
            self.rect = self.image.get_rect()
            self.lst = random.choice(PLATFORM_LIST)
            self.rect.x = self.lst[0]
            self.rect.y = self.lst[1] - 22 
            self.speedx=6
            
        def update(self):
            if self.rect.x>= self.lst[0] and self.rect.x <=self.lst[0]+82:
                self.rect.x += self.speedx
            if self.rect.x  > self.lst[0]+82:
                self.speedx=-1.9*self.speedx
                self.rect.x += self.speedx
            if self.rect.x < self.lst[0]:
                self.speedx=6
                self.rect.x += self.speedx
            
            
    class Bullet(pg.sprite.Sprite):
        def __init__(self,x,y):
            pg.sprite.Sprite.__init__(self)
            self.image=pg.image.load("bulletu.png")
            self.image = pg.transform.scale(self.image,(10,20))
            self.rect = self.image.get_rect()
            self.rect.bottom=y
            self.rect.centerx =x
            self.speedy = 5
            
        def update(self):
            self.rect.y -= self.speedy
            if self.rect.bottom >HEIGHT:
                self.kill()
        
        
        
    class main():
        def __init__(self):
        # initialize game window, etc
            pg.init()
            self.width = 750
            self.height = 500
            self.win = pg.display.set_mode((self.width,self.height))
            pg.display.set_caption("CONTRA")
            self.clock = pg.time.Clock()
            self.run = True
        def new(self):
        # start a new game
            self.all_sprites = pg.sprite.Group()
            self.platforms = pg.sprite.Group()
            self.bullets = pg.sprite.Group()
            self.enemies = pg.sprite.Group()
            self.ebullets = pg.sprite.Group()
            self.fgates = pg.sprite.Group()
            self.flames = pg.sprite.Group()
            self.player = Player(self)
            self.all_sprites.add(self.player)
            for flms in range(0,750,50):
                f = Flames(flms,HEIGHT - 50)
                self.all_sprites.add(f)
                self.flames.add(f)
            x=Platform(0,HEIGHT-80,100,20)
            self.all_sprites.add(x)
            self.platforms.add(x)
            x1=Platform(WIDTH-120,HEIGHT-80,120,20)
            self.all_sprites.add(x1)
            self.platforms.add(x1)
            for plat in PLATFORM_LIST:
                p = Platform(*plat)
                self.all_sprites.add(p)
                self.platforms.add(p)
            e = Enemy(self)
            self.all_sprites.add(e)
            self.enemies.add(e)
            e1 = Enemy(self)
            self.all_sprites.add(e1)
            self.enemies.add(e1)
            self.explosions = [pg.image.load("regularExplosion00.png"),pg.image.load("regularExplosion01.png"),pg.image.load("regularExplosion02.png"),pg.image.load("regularExplosion03.png"),pg.image.load("regularExplosion04.png"),pg.image.load("regularExplosion05.png"),pg.image.load("regularExplosion06.png"),pg.image.load("regularExplosion07.png"),pg.image.load("regularExplosion08.png")]
            for enemy in range(3):
                e = wEnemy()
                self.all_sprites.add(e)
                self.enemies.add(e)
            self.run1()
        def run1(self):
            self.play = True
            start_ticks=pg.time.get_ticks() 
            while self.play:
                self.clock.tick(60)
                self.events()
                self.update()
                self.draw()
                seconds=(pg.time.get_ticks()-start_ticks)/1000
                if seconds>15: 
                    self.run=False
                    self.play=False
                    pg.quit()
                    messagebox.showinfo("RESULT"," TIME IS UP YOU LOST")
                

        def drawlife(self,surf,x,y,lives,img):
            for i in range(lives):
                img_rect = img.get_rect()
                img_rect.x = x + (40*i)
                img_rect.y = y
                if self.run!= False and self.play!= False:
                    surf.blit(img,img_rect)
                lives-=1
            
        def update(self):
            self.all_sprites.update()
            if self.player.vel.y > 0:
                hits=pg.sprite.spritecollide(self.player,self.platforms,False)
                if hits:
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = 0
            hits=pg.sprite.groupcollide(self.bullets,self.enemies,True,True)
            for hit in hits:
                expl = Explosion(hit.rect.center,self.explosions)
                self.all_sprites.add(expl)
            hits1=pg.sprite.groupcollide(self.bullets,self.platforms,True,False)
            hits2=pg.sprite.spritecollide(self.player,self.flames,True)
            for hits in hits2:
                exp2 = Explosion(hits.rect.center,self.explosions)
                self.all_sprites.add(exp2)
                self.player.hide()
                self.player.lives -=1
                
            hits3=pg.sprite.spritecollide(self.player,self.enemies,True)
            for hit in hits3:
                exp3 = Explosion(hit.rect.center,self.explosions)
                self.all_sprites.add(exp3)
                self.player.hide()
                self.player.lives -=1
            if self.player.lives<0:
                self.player.kill()
            if not self.enemies:
                f = FGate()
                self.all_sprites.add(f)
                self.fgates.add(f)
            hits4=pg.sprite.spritecollide(self.player,self.fgates,False)
            if hits4:
                self.run=False
                self.play=False
                pg.quit()
                messagebox.showinfo("RESULT","YOU WON")
                
                
        def events(self):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    if self.play:
                        self.play = False
                    self.run = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        self.player.jump()
                    if event.key == pg.K_SPACE:
                        self.player.hshoot()
                    if event.key == pg.K_s:
                        self.player.shoot()
                
        def draw(self):
            if self.run!= False and self.play!= False:
                bg=pg.image.load("bg2.png")
                bg_rect = bg.get_rect()
                self.win.blit(bg,bg_rect)
                self.drawlife(self.win,WIDTH-100,25,self.player.lives,smallpimage)
                self.all_sprites.draw(self.win)
                self.platforms.draw(self.win)
                pg.display.update()

    game=main()
    while game.run:
        game.new()
    pg.quit()








main()


















        

