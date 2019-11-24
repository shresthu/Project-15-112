import pygame
import random
pygame.init()
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width,display_height))
clock = pygame.time.Clock()
def message_display(text):
    Text=pygame.font.Font(None,25)
    TextSurf,TextRect = text_objects(text,largeText) 
    TextRect.center = ((width//2),(height//2))
    win.blit(TextSurf,TextRect)
    pygame.display.update()
def text_objects(text,font):
    textSurface = font.render(text,True,[0,0,0])
    return textSurface,textSurface.get_rect()
def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()         
        gameDisplay.fill((255,255,255,255))
        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = text_objects("GAAAMEE", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)
        button("GO!",150,450,100,50,(0,255,0,255),(0,255,100,255),main)
        button("Quit",550,450,100,50,(255,0,0,255),(255,100,0,255),quitgame)
        pygame.display.update()
        clock.tick(15)
def quitgame():
    pygame.quit()
    quit()  
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)
def main():
    width=500
    height=480
    wnd=[width,height]
    win = pygame.display.set_mode(wnd)
    walkRight = [pygame.image.load('RN11.png'), pygame.image.load('RN22.png'), pygame.image.load('RN33.png'), pygame.image.load('RN44.png'), pygame.image.load('RN55.png'), pygame.image.load('RN66.png')]
    pygame.display.set_caption("CONTRA")
    bg=pygame.image.load("bg1.png")
    standing=pygame.image.load('standing-2.png')    
    BLACK = (0, 0, 0, 255)
    WHITE = (255, 255, 255, 255)
    GREEN = (0,255,0,255)
    class platform():
        def __init__(self, x, y):
            self.x1 = x
            self.y = y
            self.x2 = x + 50
        def test(self, player):
            if player.x < self.x1 or player.x > self.x2:
                return None
            if player.y <= self.y  and player.y + player.velocity >= self.y and player.x > self.x1 and player.x < self.x2:
                return self
            return None
    class platforms():
        def __init__(self):
            self.container = []
        def addp(self, p):
            self.container.append(p)
        def draw(self):
            global GREEN
            display = pygame.display.get_surface()
            for p in self.container:
                pygame.draw.rect(display,(0,255,0,255),[p.x1,p.y,50,30])
        def checkcollision(self,man):
            if (not man.falling):
                return False
            for p in self.container:
                    result = p.test(man)
                    if result:
                            man.currentPlatform = result
                            man.y = result.y
                            man.falling = False
                            return True
            return False
        def do(self,man):
            self.checkcollision(man)
            self.draw()
            
    class player(object):
        def __init__(self,x,y,width,height,maxJump,velocity):
            self.x=x
            self.y=y
            self.width=width
            self.height=height
            self.vel=5
            self.isJump = False
            self.left=False
            self.right=False
            self.walkcount = 0
            self.jumpCount=10
            self.standing=True
            self.onPlatform=None
            self.maxjump=maxJump
            self.falling= False
            self.velocity = velocity    
            
        def draw(self,win):
            if self.walkcount+1>=6:
                self.walkCount = 0
            elif self.right:
                win.blit(walkRight[self.walkCount%6], (self.x,self.y))
                self.walkCount +=1
            else:
                 win.blit(standing,(self.x,self.y))
            print(man.x,"xxxx",man.y,"yyyy")
        def move(self):
            if self.onPlatform:
                    if not self.onPlatform.test(self):
                            self.falling = True
                            self.onPlatform = None
    def drawGameWindow():   
        win.blit(bg,(0,0))
        man.draw(win)
        PLATFORMS.do(man)
        man.move()
        pygame.display.update()
    man=player(100,410,64,64,height,3)
    PLATFORMS = platforms()
    PLATFORMS.addp(platform(150,380)) 
    for i in range(0, 2):
    	PLATFORMS.addp(platform(random.randint(0, width - 50), random.randint(50, height - 60)))
    run=True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            keys = pygame.key.get_pressed ()
        if keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
            man.x += man.vel
            man.right = True
            man.left = False
            man.standing = False
        else:
            man.standing = True
            man.walkCount = 0
        if not(man.isJump):
            if keys[pygame.K_UP]:
                man.isJump = True
                man.right = False
                man.walkCount = 0
        else:
            if man.jumpCount >= -10:
                neg = 1
                if man.jumpCount < 0:
                    neg = -1
                man.y -= (man.jumpCount ** 2) * 0.5 * neg
                man.jumpCount -= 1
            else:
                man.isJump = False
                man.falling=True
                man.jumpCount = 10
        drawGameWindow()
        pygame.display.update()
        clock.tick(15)
    pygame.quit()    
             
game_intro()
































        
        
    
    
