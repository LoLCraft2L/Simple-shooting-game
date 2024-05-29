#Importings
import pygame
import random
import math

#Initialization
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Goofy shooting game")
clock = pygame.time.Clock()
font = pygame.font.Font('Horison.ttf', 32)
score = 0

#In game Objects
projectiles = []
objects = []
exp = [random.randint(20,screen_width-20),random.randint(20,screen_height-20)]
status = True


#Classes
#Bullet
class Bullet():
    def __init__(self,direction,posx,posy):
        self.posx = posx
        self.posy = posy
        self.direction = direction
        self.speed = 20

    def update(self,score):
        points = 0
        self.posx += self.speed*math.cos(self.direction)
        self.posy += self.speed*math.sin(self.direction)
        pygame.draw.circle(screen, 'red', (self.posx,self.posy) , 5)
        if self.posx > screen_width or self.posx < 0 or self.posy > screen_height or self.posx < 0:
            projectiles.remove(self)
        if objects != []:
            for i in objects:
                if self.posx > i.posx and self.posx < i.posx + i.size  and self.posy > i.posy and self.posy < i.posy + i.size:
                    projectiles.remove(self)
                    points += 1
                    objects.remove(i)
        if points != 0 and objects == []:
            for i in range(1+(points+score)//5):
                objects.append(Obstacle(random.randint(20,screen_width-20),random.randint(20,screen_height-20),random.randint(20,40)))
        return points

#Class for player       
class Player:
    def __init__(self, posx, posy,speed):
        self.posx = posx
        self.posy = posy
        self.speed = speed
        
    def update(self,exp):
        status = True
        keys = pygame.key.get_pressed()
        move_by = self.speed
        oldx = self.posx
        oldy = self.posy
        mouse_pos = pygame.mouse.get_pos()
        if (keys[pygame.K_d] - keys[pygame.K_a]) != 0 and (keys[pygame.K_s] - keys[pygame.K_w]) != 0:
            move_by = math.sqrt(self.speed*self.speed/2) + self.speed/5
        self.posx += move_by * (keys[pygame.K_d] - keys[pygame.K_a])
        self.posy += move_by * (keys[pygame.K_s] - keys[pygame.K_w])
        self.posx = screen_width-25 if self.posx > screen_width-25 else self.posx
        self.posx = 0 if self.posx < 0 else self.posx
        self.posy = screen_height-25 if self.posy > screen_height-25 else self.posy
        self.posy = 0 if self.posy < 0 else self.posy
        pygame.draw.rect(screen, 'white', (self.posx,self.posy,25,25))
        if keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
           # Calculate angle between object and mouse
            angle = math.atan2(mouse_pos[1] - self.posy, mouse_pos[0] - self.posx)
            projectiles.append(Bullet(angle,self.posx+12,self.posy+12))
        if objects != []:
            for i in objects:
                for x, y in zip([self.posx,self.posx+25,self.posx+15],[self.posy,self.posy+25,self.posy+15]):
                    if x > i.posx and x < i.posx + i.size  and y > i.posy and y < i.posy + i.size:
                      status = False
        for x, y in zip([self.posx,self.posx+25,self.posx+15],[self.posy,self.posy+25,self.posy+15]):
            if x > exp[0] and x < exp[0] + 20  and y > exp[1] and y < exp[1] + 20:
                self.speed += 0.5
                exp = [random.randint(20,screen_width-20),random.randint(20,screen_height-20)]
        if move_by > 19:
            for i in range(int(move_by/19)):
                for x, y in zip([oldx,oldx+25,oldx+15],[oldy,oldy+25,oldy+15]):
                   if x > exp[0] and x < exp[0] + 20  and y > exp[1] and y < exp[1] + 20:
                      self.speed += 0.5
                      exp = [random.randint(20,screen_width-20),random.randint(20,screen_height-20)]
                oldx += 20
                oldy += 20

        return status, exp


player = Player(screen_width/2,screen_height/2,24)

#Class for obstacles
class Obstacle:
    def __init__(self,posx,posy,size):
        self.posx = posx
        self.posy = posy
        self.size = size
    
    def update(self):
        pygame.draw.rect(screen, 'blue', (self.posx,self.posy,self.size,self.size))
objects.append(Obstacle(random.randint(20,screen_width-20),random.randint(20,screen_height-20),random.randint(20,40)))
#Functions

#Draw player


#Game Code
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
    text = font.render(f'Score = {score}   Speed = {player.speed}', True, 'green')
    screen.fill(0)
    if projectiles != []:
        for i in projectiles:
            score += i.update(score)
    if objects != []:
        for i in objects:
            i.update()
    status,exp = player.update(exp)
    if not status:
        death = font.render(f'Game Over', True, 'red')
        screen.blit(death,(200,200))
        run = False
    pygame.draw.rect(screen, 'green', (exp[0],exp[1],20,20))
    screen.blit(text,(250,10))
    pygame.display.update()
    clock.tick(60)