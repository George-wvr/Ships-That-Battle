#Gameplay functions
#George Weaver
#06/03/2024
import pygame
from pygame.locals import *

#Colours
sea_col = (68, 114, 196)
island_col = (140, 105, 0)
boat_p_col = (0, 0, 0)
bomb_col = (0, 0, 0)
black = (0, 0, 0)
caution_col = (255, 0, 0)
dock_col = (69, 89, 105)
boat_e_col = (167, 102, 173)
menu_col = (128, 128, 128)
game_box_col = (175, 171, 171)

#Variables and constants
swidth = 1250
sheight = 600
boat_speed = 0.117
enemy_boat_speed = 0.5
cool_down = 0  # the cooldown for between missile fires
score = 0
health = 100

#Island class
class Island():
    def __init__(self, x_pos, y_pos, width, height):
        #super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.width = width
        self.height = height
        self.island = pygame.Surface((self.width, self.height))
        self.rect = self.island.get_rect()
        self.rect.topleft = (self.x, self.y)

    def draw(self, displaysurf):
        self.island.fill(island_col)
        displaysurf.blit(self.island, (self.x, self.y))

    def colour(self,displaysurf, col):
        self.island.fill(col)
        displaysurf.blit(self.island, (self.x, self.y))
        pygame.display.update()


island1 = Island(50, 100, 100, 200)
island2 = Island(1000, 250, 75, 75)
island3 = Island(475, 250, 50, 100)
island4 = Island(650, 100, 50, 25)
island5 = Island(700, 350, 200, 150)
island6 = Island(75, 400, 25, 100)

all_islands = [island1, island2, island3, island4, island5, island6]

#Player boat class
class Boat(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.width = 10
        self.height = 10
        self.boat = pygame.Surface((self.width, self.height),8)
        self.rect = self.boat.get_rect(center=(self.x, self.y))

    def draw(self, displaysurf):
        self.move()
        self.rect = self.boat.get_rect(center=(self.x, self.y))
        self.boat.fill(boat_p_col)
        displaysurf.blit(self.boat, self.rect)

    def goto(self, x_pos, y_pos, displaysurf):
        self.x = x_pos
        self.y = y_pos
        self.rect = self.boat.get_rect(topleft=(self.x, self.y))
        displaysurf.blit(self.boat, self.rect)
        pygame.display.update()

    def move(self):
        pressedkey = pygame.key.get_pressed()

        if pressedkey[K_a] or pressedkey[K_LEFT]:
            if self.rect.left > 275:
                # print("left")
                self.x -= boat_speed

        if self.rect.left < 1225 - (self.width):
            if pressedkey[K_d] or pressedkey[K_RIGHT]:
                # print("right")
                self.x += boat_speed

        if self.rect.top > 25:
            if pressedkey[K_w] or pressedkey[K_UP]:
                # print("up")
                self.y -= boat_speed

        if self.rect.top < 575 - self.height:
            if pressedkey[K_s] or pressedkey[K_DOWN]:
                # print("down")
                self.y += boat_speed

#Players Boat
player_boat = Boat(280, 30)

#Screen design
def layout(displaysurf):
    displaysurf.fill(menu_col)

    #Information boxes
    box = pygame.Surface((225,50))
    box.fill(game_box_col)
    #timer
    displaysurf.blit(box, (25,25))

    #Health
    displaysurf.blit(box, (25,125))
    
    #Score
    displaysurf.blit(box, (25,225))

    #High Score
    displaysurf.blit(box, (25,525))

    #Box Borders
    #Timer
    box_rect = box.get_rect(topleft = (25,25))
    pygame.draw.rect(displaysurf, black, box_rect, 5)

    #Health
    box_rect = box.get_rect(topleft = (25,125))
    pygame.draw.rect(displaysurf, black, box_rect, 5)

    #Score
    box_rect = box.get_rect(topleft = (25,225))
    pygame.draw.rect(displaysurf, black, box_rect, 5)

    #High Score
    box_rect = box.get_rect(topleft = (25,525))
    pygame.draw.rect(displaysurf, black, box_rect, 5)

    #Game Space
    box = pygame.Surface((950,550))
    box.fill(sea_col)
    displaysurf.blit(box,(275,25))

#Main Function for the game
def run_game(displaysurf):

    layout(displaysurf)

    #for island in all_islands:
        #island.draw(displaysurf)

    player_boat.draw(displaysurf)