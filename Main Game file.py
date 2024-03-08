#Main Game file

#importing Libraries
import pygame,sys
from pygame.locals import *
from menus import *
#Setting up pygame instance:
pygame.init()

#variables and constants
menu = "start" #so that the start menu loads on start up
user_name_text = ""
user_age_input = ""
active_box = None
invalid_inputs = [None, "\b", "\n", "\t", "\r", "^[", '"', "#"] 
n_message = ""
a_message = ""

#Colours
screen_default = (88, 155, 213)
screen_alt = (0, 32, 96)
current_screen_col = screen_default

txt_default = (0,0,0)
txt_alt = (255, 255, 255)
txt_error_col = (255, 0, 0)
current_text_col = txt_default

active_box_col = (0, 255, 0)




#Game window
swidth = 1250
sheight = 600

displaysurf = pygame.display.set_mode((swidth,sheight))
pygame.display.set_caption("Ships That Battle")

# setting FPS
FPS = 120
framesps = pygame.time.Clock()

while True:
    displaysurf.fill(current_screen_col)
    #sets the key pressed to noting so that nothing is inputed in the textboxes at this point
    event_key_pressed = None
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        #assigns the letter press to a variable
        if event.type == KEYDOWN:
            event_key_pressed = event.unicode

    if menu == "start":
        main_menu(displaysurf)


    pygame.display.update()
    pygame.display.flip()
    framesps.tick(FPS)