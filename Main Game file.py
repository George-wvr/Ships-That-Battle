#Main Game file

#importing Libraries
import pygame,sys
from pygame.locals import *
from menus import main_menu
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

#function to change colours and fonts:
def scheme_change(change):
    global current_screen_col
    global current_title_fnt
    global current_standard_fnt
    global current_text_col
    if change == "col1":
        current_screen_col = screen_default
        current_text_col = txt_default
    elif change == "col2":
        current_screen_col = screen_alt
        current_text_col = txt_alt
    elif change == "fnt1":
        current_title_fnt = fnt_title_defult
        current_standard_fnt = fnt_standard_defult
    elif change == "fnt2":
        current_title_fnt = fnt_title_alt
        current_standard_fnt = fnt_standard_alt
        

#Fonts:
fnt_title_defult = pygame.font.SysFont("Calibri", 60)
fnt_title_alt = pygame.font.Font("OpenDyslexic-Regular.ttf", 40)

fnt_standard_defult = pygame.font.SysFont("Calibri", 40)
fnt_standard_alt = pygame.font.Font("OpenDyslexic-Regular.ttf", 30)

current_title_fnt = fnt_title_defult
current_standard_fnt = fnt_standard_defult


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