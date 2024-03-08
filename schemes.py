#Fonts and colours
#George Weaver
#08/03/2024

import pygame, sys
from pygame.locals import *


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