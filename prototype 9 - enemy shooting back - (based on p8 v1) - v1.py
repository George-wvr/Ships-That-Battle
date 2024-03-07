import pygame
from pygame.locals import *
import sys
import time
import random
import math

from pygame import mixer

# colours
sea_col = (68, 114, 196)
island_col = (140, 105, 0)
boat_p_col = (0, 0, 0)
bomb_col = (0, 0, 0)
black = (0, 0, 0)
caution_col = (255, 0, 0)
dock_col = (69, 89, 105)
boat_e_col = (167, 102, 173)

# General Constants
boat_speed = 1.5
enemy_boat_speed = 0.5
cool_down = 0  # the cooldown for between missile fires
score = 0
health = 100

# setting FPS
FPS = 120
framesps = pygame.time.Clock()

# Setting up pygame instance:
pygame.init()

#Importing music and audio
#This is the background audio which will repeat
mixer.music.load("background.mp3")
#These are the sound effects that will play over the top of the background music
cannon_sound = pygame.mixer.Sound("cannon2.wav")
wood_crash = pygame.mixer.Sound("wood_hit.wav")
water_splosh = pygame.mixer.Sound("water_splosh.wav")
ship_sink = pygame.mixer.Sound("ship_sink.wav")
thump = pygame.mixer.Sound("thump.wav")

# Game window
swidth = 1250
sheight = 600

displaysurf = pygame.display.set_mode((swidth, sheight))
displaysurf.fill(sea_col)
pygame.display.set_caption("Ships That Battle")

dock = pygame.Surface((100, 100))
dock.fill(dock_col)

edock = pygame.Surface((100, 100))
edock.fill(dock_col)

water = pygame.Surface((75, 40))
water.fill(sea_col)

#Fonts
fnt_title = pygame.font.SysFont("Calibre", 60)
fnt_standard = pygame.font.SysFont("Calibri", 40)


class Island(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, width, height):
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.width = width
        self.height = height
        self.island = pygame.Surface((self.width, self.height))
        self.rect = self.island.get_rect()
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        self.island.fill(island_col)
        displaysurf.blit(self.island, (self.x, self.y))

    def colour(self, col):
        self.island.fill(col)
        displaysurf.blit(self.island, (self.x, self.y))
        pygame.display.update()


island1 = Island(50, 100, 100, 200)
island2 = Island(1000, 250, 75, 75)
island3 = Island(475, 250, 50, 100)
island4 = Island(650, 100, 50, 25)
island5 = Island(700, 350, 200, 150)
island6 = Island(75, 400, 25, 100)


# dock = Island(swidth - 100, sheight - 100,100,100)

class Boat(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.width = 25
        self.height = 25
        self.boat = pygame.Surface((self.width, self.height),8)
        self.rect = self.boat.get_rect(center=(self.x, self.y))

    def draw(self):
        self.move()
        self.rect = self.boat.get_rect(center=(self.x, self.y))
        self.boat.fill(boat_p_col)
        displaysurf.blit(self.boat, self.rect)

    def goto(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos
        self.rect = self.boat.get_rect(topleft=(self.x, self.y))
        displaysurf.blit(self.boat, self.rect)
        pygame.display.update()

    def move(self):
        pressedkey = pygame.key.get_pressed()

        if pressedkey[K_a]:
            if self.rect.left > 0:
                # print("left")
                self.x -= boat_speed

        if self.rect.left < swidth - (self.width):
            if pressedkey[K_d]:
                # print("right")
                self.x += boat_speed

        if self.rect.top > 0:
            if pressedkey[K_w]:
                # print("up")
                self.y -= boat_speed

        if self.rect.top < sheight - self.height:
            if pressedkey[K_s]:
                # print("down")
                self.y += boat_speed


class Eboat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 70
        self.y = 50
        self.width = 25
        self.height = 25
        self.reset_offset = 0
        self.x_offset = 0
        self.y_offset = 0
        self.colour = (22, 224, 25)
        self.boat = pygame.Surface((self.width, self.height))
        self.get_rectgl()
        self.cooldown = 0

    def get_rectgl(self):
        pygame.draw.rect(self.boat, boat_e_col, pygame.Rect(self.x, self.y, self.width, self.height))
        self.rect = self.boat.get_rect()
        self.rect.center = ((self.x), (self.y))

    def draw(self):
        self.sail()
        self.boat.fill(self.colour)
        displaysurf.blit(self.boat, self.rect)

        #print(self.x, self.y)

    def sail(self):
        if self.reset_offset == 0:
            self.x_offset = random.randint(-100, 100)
            self.y_offset = random.randint(-100, 100)
            self.reset_offset = random.randint(100, 120)
        else:
            self.reset_offset -= 1

        if (self.x + self.x_offset) < player_boat.x:
            self.x += enemy_boat_speed
        elif (self.x + self.x_offset) > player_boat.x:
            self.x -= enemy_boat_speed

        if (self.y + self.y_offset) < player_boat.y:
            self.y += enemy_boat_speed
        elif (self.y + self.y_offset) > player_boat.y:
            self.y -= enemy_boat_speed

        self.get_rectgl()
        displaysurf.blit(self.boat, self.rect)

        if self.cooldown == 0:
            self.fire()
        else:
            self.cooldown -= 1

    def hit(self):
        global score
        sound = 1
        if self.colour == (22, 224, 25):
            self.colour = (113, 224, 22)
        elif self.colour == (113, 224, 22):
            self.colour = (170, 224, 22)
        elif self.colour == (170, 224, 22):
            self.colour = (224, 211, 22)
        elif self.colour == (224, 211, 22):
            self.colour = (224, 110, 22)
        elif self.colour == (224, 110, 22):
            self.colour = (224, 22, 22)
        elif self.colour == (224, 22, 22):
            print("Sink")
            sound = 2
        if sound == 1:
            pygame.mixer.Sound.play(wood_crash)
        else:
            pygame.mixer.Sound.play(ship_sink)
            score += 5

    def fire(self):
        x_distance = (self.x - player_boat.x)**2
        y_distance = (self.y - player_boat.y)**2
        distance = math.sqrt(x_distance + y_distance)
        do_random = random.randint(0,1)
        if distance < 100:
            #go for the exact point of the boat half of the time
            if do_random == 0:
                print("Direct")
                enemy_bombs.append(Bomb(self.x, self.y, player_boat.x, player_boat.y, 1))
                self.cooldown = 50
                pygame.mixer.Sound.play(cannon_sound)
            if do_random == 1:
                print("Random")
                random_influence_x = random.randint(-25, 25)
                random_influence_y = random.randint(-25, 25)
                enemy_bombs.append(Bomb(self.x, self.y, (player_boat.x + random_influence_x), (player_boat.y + random_influence_y), 1))



# Class for the missiles and bombs
class Bomb:
    def __init__(self, x_pos, y_pos, target_x_pos, target_y_pos, type):
        self.x = x_pos
        self.y = y_pos
        self.speed = 7
        self.crash = False
        # life defines how long the missile will last before 'crashing into the sea'
        self.life = 30
        self.type = type # an intiger 0 or 1 that defines if it is a player on enemy bomb
        # Setting the angles for the missiles to move at based on the position of the mouse at the time its called
        # Uses trigonometry to find the angle between the y position and the x position of the boat and mouse
        self.angle = (math.atan2(y_pos - target_y_pos, x_pos - target_x_pos))
        # Calculates the rate that it must move up or down to be on the angle
        self.x_angle = math.cos(self.angle) * self.speed
        # Calculates the rate at which it moves left or right to move along the angle
        self.y_angle = math.sin(self.angle) * self.speed

    def move(self):
        if self.crash == False and self.life > 0:
            # Changes the x position of the sprite dependign on the pre-calculated rate
            self.x -= self.x_angle
            # Same for the y position
            self.y -= self.y_angle
            # Displays the bomb on the screen in the new position
            pygame.draw.circle(displaysurf, bomb_col, (self.x, self.y), 5)
            self.life -= 1

        #Plays audio if the missile 'hits the sea'
        if self.life <= 0:
            pygame.mixer.Sound.play(water_splosh)

        # If the missile has collided with something it is moved off of the screen so it cant be collided with again
        if self.crash == True or self.life <= 0:
            if self in player_bombs:
                player_bombs.remove(self)
            elif self in enemy_bombs:
                enemy_bombs.remove(self)

    def set_crash(self):
        self.crash = True
        self.x = 1000
        self.y = 1000


player_bombs = []
enemy_bombs = []

# Grouping island sprites
islands = pygame.sprite.Group()
islands.add(island1)
islands.add(island2)
islands.add(island3)
islands.add(island4)
islands.add(island5)
islands.add(island6)
# islands.add(dock)

allsprites = pygame.sprite.Group()
allsprites.add(island1)
allsprites.add(island2)
allsprites.add(island3)
allsprites.add(island4)
allsprites.add(island5)
allsprites.add(island6)

enemy_boat = Eboat()
enemies = pygame.sprite.Group()
enemies.add(enemy_boat)

player_boat = Boat(swidth - 75, sheight - 50)


# Play the music:
mixer.music.play(-1)

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    displaysurf.fill(sea_col)

    allsprites.add(player_boat)
    allsprites.add(enemy_boat)

    displaysurf.blit(dock, (swidth - 100, sheight - 100))
    displaysurf.blit(edock, (0, 0))
    displaysurf.blit(water, (swidth - 100, sheight - 70))

    scoretext = "Score: "+str(score)
    score_text = fnt_standard.render(scoretext, True, black)
    displaysurf.blit(score_text, (swidth-200, 10))

    healthtext = "Health: " + str(health)
    health_text = fnt_standard.render(healthtext, True, black)
    displaysurf.blit(health_text, (swidth - 500, 10))


    for thing in allsprites:
        thing.draw()

    if pygame.sprite.spritecollideany(player_boat, islands):
        pygame.sprite.spritecollideany(player_boat, islands).colour(caution_col)
        time.sleep(1)
        health = 100
        player_boat.goto(swidth - 75, sheight - 50)

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1 and cool_down <= 0:
            cool_down = 50
            pygame.mixer.Sound.play(cannon_sound)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Adds a new instance of the bomb to the list
            player_bombs.append(Bomb(player_boat.x, player_boat.y, mouse_x, mouse_y, 0))

    for bullet in player_bombs:
        bullet.move()
        # checks if the bullet colides with an island
        for island in islands:
            if island.rect.collidepoint(bullet.x, bullet.y):
                pygame.mixer.Sound.play(thump)
                bullet.set_crash()

        # Checks if the Bullet collides with an enemy boat
        for enemy in enemies:
            if enemy.rect.collidepoint(bullet.x, bullet.y):
                bullet.set_crash()
                enemy.hit()
                score += 5

    for bullet in enemy_bombs:
        bullet.move()
        # checks if the bullet colides with an island
        for island in islands:
            if island.rect.collidepoint(bullet.x, bullet.y):
                pygame.mixer.Sound.play(thump)
                bullet.set_crash()

        if player_boat.rect.collidepoint(bullet.x, bullet.y):
            health -= 1
            bullet.set_crash()

    if cool_down > 0:
        cool_down -= 1

    pygame.display.flip()
    framesps.tick(FPS)
