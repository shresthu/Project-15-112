import pygame as pg
import random
vec = pg.math.Vector2
#____________________________________________________________________________________________________________________________________
#constants
PLAYER_ACC = 0.4
PLAYER_FRICTION = -0.2
WIDTH = 750
HEIGHT = 500
PLATFORM_LIST = [(WIDTH/2 -50 , HEIGHT *(3/4) ,100 ,20),
                 (125,HEIGHT -350 ,100,20),(350,200,100,20),(175,300,100,20),
                 (550,100,100,20),(550,300,100,20)]
#___________________________________________________________________________________________________________________________________
#this class creates the player
class Player(pg.sprite.Sprite):
    def __init__(self,main): 
        pg.sprite.Sprite.__init__(self)
        self.game=main 
        self.image=pg.image.load("standing-2.png")
        self.rect = self.image.get_rect() 
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(20,HEIGHT-40)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.facing=1
        
    def update(self):
        self.acc = vec(0, 0.8)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.facing=-1
            self.image = pg.image.load("standing-2.png")
            self.image = pg.transform.flip(self.image, True, False)
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.facing=1
            self.image=pg.image.load("standing-2.png")
            self.acc.x = PLAYER_ACC

        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + (0.5 * self.acc)
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0
        self.rect.midbottom = self.pos

    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self,self.game.platforms,False)
        self.rect.x -= 1
        if hits:
            self.vel.y= -15
            
    def shoot(self):
        bullet=Bullet(self.rect.centerx,self.rect.centery,self.facing)
        self.game.all_sprites.add(bullet)
        self.game.bullets.add(bullet)

    def ushoot(self):
        bullet=UBullet(self.rect.centerx,self.rect.centery)
        self.game.all_sprites.add(bullet)
        self.game.bullets.add(bullet)
        
#this class creates the platforms
class Platform(pg.sprite.Sprite):
    def __init__(self,x,y,w,h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("platform1.jpg")
        self.image = pg.transform.scale(self.image,(w,h))
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
#this class creates the Enemy sprite intial values
class Enemy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("enemyn.png")
        self.image = pg.transform.scale(self.image,(20,30))
        self.rect = self.image.get_rect()
        self.lst = random.choice(PLATFORM_LIST)
        self.rect.x = self.lst[0]
        self.rect.y = self.lst[1] - 22 
        self.speedx=1.5
        
    def update(self):
        if self.rect.x>= self.lst[0] and self.rect.x <=self.lst[0]+82:
            self.rect.x += self.speedx
        if self.rect.x  > self.lst[0]+82:
            self.speedx=-0.9*self.speedx
            self.rect.x += self.speedx
        if self.rect.x < self.lst[0]:
            self.speedx=1.5
            self.rect.x += self.speedx
#this class is used to create the gate to the net level         
class FGate(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("door.png")
        self.image = pg.transform.scale(self.image,(40,35))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 20
        self.rect.y = HEIGHT-75
#this class is used to initialze bullet sprites   
class Bullet(pg.sprite.Sprite):
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
#this class is used to initialze vertical bullet sprites
class UBullet(pg.sprite.Sprite):
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
#this class is used to create explosion when collision happens 
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
#this class is used to initialze all the values and create the runnig loop
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
        self.fgates = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        x=Platform(0,HEIGHT -40,WIDTH,40)
        self.all_sprites.add(x)
        self.platforms.add(x) 
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        for enemy in range(7):
            e = Enemy()
            self.all_sprites.add(e)
            self.enemies.add(e)
        self.explosions = [pg.image.load("regularExplosion00.png"),pg.image.load("regularExplosion01.png"),pg.image.load("regularExplosion02.png"),pg.image.load("regularExplosion03.png"),pg.image.load("regularExplosion04.png"),pg.image.load("regularExplosion05.png"),pg.image.load("regularExplosion06.png"),pg.image.load("regularExplosion07.png"),pg.image.load("regularExplosion08.png")]
        self.run1()
#this runs the main loop of the game
    def run1(self):
        self.play = True
        while self.play:
            self.clock.tick(55)
            self.events()
            self.update()
            self.draw()
    def update(self):
        # Game Loop - Update
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
        if not self.enemies:
            f = FGate()
            self.all_sprites.add(f)
            self.fgates.add(f)
        hits1=pg.sprite.spritecollide(self.player,self.fgates,False)
        if hits1:
            import newlevel
            newlevel.main()
    def events(self):
    # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.play:
                    self.play = False
                self.run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.player.jump()
                if event.key == pg.K_SPACE:
                    self.player.shoot()
                if event.key == pg.K_s:
                    self.player.ushoot()
#draws all the starting sprites and background      
    def draw(self):
        bg=pg.image.load("bg1.png")
        bg_rect = bg.get_rect()
        self.win.blit(bg,bg_rect)
        self.all_sprites.draw(self.win)
        self.platforms.draw(self.win)
        pg.display.update()

game=main()
while game.run:
    game.new()
pg.quit()
































    

