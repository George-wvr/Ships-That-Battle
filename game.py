#Gameplay functions
#George Weaver
#06/03/2024
import pygame
from pygame.locals import *

sea_col = (68, 114, 196)
island_col = (140, 105, 0)
boat_p_col = (0, 0, 0)
bomb_col = (0, 0, 0)
black = (0, 0, 0)
caution_col = (255, 0, 0)
dock_col = (69, 89, 105)
boat_e_col = (167, 102, 173)

class Island(): #pygame.sprite.Sprite
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

#Main Function for the game
def run_game(displaysurf):
    print("Running")

    for island in all_islands:
        island.draw(displaysurf)