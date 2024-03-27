#Main Game file

#importing Libraries
import pygame,sys
from pygame.locals import *
from pygame import mixer
import random
import math
#Setting up pygame instance:
pygame.init()

#variables and constants
menu = "game" #so that the start menu loads on start up
previous_menu = "start"

user_name_text = "ADMIN"
user_age_input = "100"
active_box = None
invalid_inputs = [None, "\b", "\n", "\t", "\r", "^[", '"', "#"]
n_message = ""
a_message = ""

boat_speed = 1
enemy_boat_speed = 0.75
cool_down = 0  # the cooldown for between missile fires
score = 0
health = 100

mins = 2
seconds = 0
frame_count = 0

music = 1 # 1 is playing, 2 is stopping, 3 is continuing as normal (no changes)
music_changeto = "play" # Shows what the previous change was to do
s_effects = 1 # same as for music

m_button_down = False

graph = {
    0:{1:75},
    1:{0:75, 2:60},
    2:{1:60, 3:33},
    3:{2:33, 4:72, 8:65},
    4:{3:72, 5:50},
    5:{4:50, 6:50},
    6:{5:50, 7:140, 12:171, 69:58},
    7:{6:140, 13:150, 70:58},
    8:{3:65, 9:85},
    9:{8:85, 10:75, 11:78, 14:90},
    10:{9:75, 11:71, 14:79, 19:105, 20:51},
    11:{9:78, 10:75, 12:70, 20:102},
    12:{6:171, 11:70, 22:60, 23:95, 25:148, 69:130},
    13:{7:150, 24:85, 70:104},
    14:{9:90, 10:79, 15:70},
    15:{14:70, 16:70},
    16:{15:70, 17:60},
    17:{16:60, 18:70, 28:82, 29:97},
    18:{17:70, 19:75},
    19:{10:105, 18:75, 20:81, 30:84},
    20:{10:51, 11:102, 19:81, 21:64, 22:90},
    21:{20:64, 22:70, 30:114, 31:90},
    22:{12:60, 20:90, 21:70, 23:78, 25:64},
    23:{12:95, 24:90, 22:78, 25:77, 26:85},
    24:{23:90, 26:90, 13:85, 27:75},
    25:{12:148, 22:64, 23:77, 26:60},
    26:{25:60, 23:85, 27:50, 24:90},
    27:{24:75, 26:50, 32:40},
    28:{17:82, 29:75, 36:100},
    29:{28:75, 30:115, 17:97},
    30:{19:84, 21:114, 29:115},
    31:{21:90, 35:100},
    32:{27:40, 33:100},
    33:{32:100, 34:80},
    34:{33:80, 45:60},
    35:{31:100, 42:80},
    36:{28:100, 37:80},
    37:{36:80, 38:55, 46:110},
    38:{37:55, 49:110, 39:55},
    39:{38:55, 40:60, 52:110},
    40:{39:60, 41:50},
    41:{40:50, 42:40},
    42:{35:80, 41:40, 43:70, 57:110},
    43:{42:70, 60:110, 44:70},
    44:{43:70, 45:70, 63:110},
    45:{34:60, 44:70, 66:110},
    46:{37:110, 47:100, 49:55},
    47:{46:100, 48:70, 50:55},
    48:{47:70, 51:55},
    49:{38:110, 46:55, 50:100, 52:55},
    50:{47:55, 49:100, 51:70, 53:55},
    51:{48:55, 50:70, 54:55},
    52:{39:110, 49:55, 53:100},
    53:{50:55, 52:100, 54:70, 55:60},
    54:{51:55, 53:70, 56:60},
    55:{53:60, 56:70, 58:90},
    56:{54:60, 55:70, 59:90},
    57:{42:110, 58:100, 60:70},
    58:{55:90, 57:100, 59:70, 61:70},
    59:{56:90, 58:70, 62:70},
    60:{43:110, 57:70, 61:100, 63:70},
    61:{58:70, 60:100, 62:70, 64:70},
    62:{61:70, 59:70, 65:70},
    63:{44:110, 60:70, 64:100, 66:70},
    64:{63:100, 61:70, 65:70, 67:70},
    65:{62:70, 64:70, 68:70},
    66:{45:110, 63:70, 67:100},
    67:{66:100, 64:70, 68:70},
    68:{65:70, 67:70},
    69:{6:58, 12:130, 70:80},
    70:{7:58, 13:104, 69:80}
    }

######################################################################################
#Importing music and audio
#This is the background audio which will repeat
mixer.music.load("background.wav")
#These are the sound effects that will play over the top of the background music
cannon_sound = pygame.mixer.Sound("cannon2.wav")
wood_crash = pygame.mixer.Sound("wood_hit.wav")
water_splosh = pygame.mixer.Sound("water_splosh.wav")
ship_sink = pygame.mixer.Sound("ship_sink.wav")
thump = pygame.mixer.Sound("thump.wav")

######################################################################################

#Colours
screen_default = (88, 155, 213)
screen_alt = (0, 32, 96)
current_screen_col = screen_default

game_defult = (128, 128, 128)

txt_default = (0,0,0)
txt_alt = (255, 255, 255)
txt_error_col = (255, 0, 0)
current_text_col = txt_default

active_box_col = (0, 255, 0)

sea_col = (68, 114, 196)
island_col = (140, 105, 0)
boat_p_col = (0, 0, 0)
bomb_col = (0, 0, 0)
black = (0, 0, 0)
caution_col = (255, 0, 0)
dock_col = (69, 89, 105)
boat_e_col = (167, 102, 173)
game_box_col = (175, 171, 171)

#Fonts:
fnt_title_defult = pygame.font.SysFont("Calibri", 60)
fnt_title_alt = pygame.font.Font("OpenDyslexic-Regular.ttf", 40)

fnt_standard_defult = pygame.font.SysFont("Calibri", 40)
fnt_standard_alt = pygame.font.Font("OpenDyslexic-Regular.ttf", 30)

current_title_fnt = fnt_title_defult
current_standard_fnt = fnt_standard_defult

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

#Changing the current colours when the game starts
def toggle_colours_gameandmenu():
    if current_screen_col == screen_default:
        current_screen_col = game_defult
    elif current_screen_col == game_defult:
        current_screen_col = screen_default


#Functions to render text
#Title text, current scheme
def rendertxt_title_current(text):
    rendertext = current_title_fnt.render(text, True, current_text_col)
    return rendertext

def rendertxt_standard_current(text):
    rendertxt =current_standard_fnt.render(text, True, current_text_col)
    return rendertxt

######################################################################################

#Game window
swidth = 1250
sheight = 600

displaysurf = pygame.display.set_mode((swidth,sheight))
pygame.display.set_caption("Ships That Battle")

# setting FPS
FPS = 60
framesps = pygame.time.Clock()

#####################################################################################

#Button Class
class Button():
    def __init__(self, x_pos, y_pos, width, height, colourtype, fonttype, text, type, action):
        self.x = x_pos
        self.y = y_pos
        self.width = width
        self.height = height
        self.colours = colourtype # 0=changes, 1=always defalt, 2=always alt
        self.fonts = fonttype
        self.text = text
        self.type = type
        self.action = action
        self.shape = pygame.Surface((self.width,self.height))
        self.rct = self.shape.get_rect(topleft=(self.x, self.y))

    def draw(self):        
        if self.fonts == 0:
            words = current_standard_fnt.render(self.text,True,current_text_col) # creates text

        elif self.fonts == 1:
            words = fnt_standard_defult.render(self.text,True,current_text_col)

        elif self.fonts == 2:
            words = fnt_standard_alt.render(self.text,True,current_text_col)

        if self.colours == 0:
            self.shape.fill(current_screen_col)

        elif self.colours == 1:
            self.shape.fill(screen_default)
            #Includes a change in font colour for the correct background colour
            words = current_standard_fnt.render(self.text,True, txt_default)

        elif self.colours == 2:
            self.shape.fill(screen_alt)
            #colour change of the text for the background
            words = current_standard_fnt.render(self.text,True, txt_alt)

        #changes the positioning of the text within the button depending on the font so they stay inline
        #due to different sizes with the fonts
        if current_standard_fnt == fnt_standard_defult or self.fonts == 1:
            self.shape.blit(words,(10,10)) # adds the text to the button surface

        elif current_standard_fnt == fnt_standard_alt or self.fonts == 2:
            self.shape.blit(words,(10,0))
        displaysurf.blit(self.shape,(self.x,self.y)) # adds the button surface to the displaysurf

    def hover(self):
        m_pos = pygame.mouse.get_pos()
        if self.rct.collidepoint(m_pos):
            return True

    def clicked(self):
        global m_button_down
        if event.type == pygame.MOUSEBUTTONDOWN and self.hover() == True:
            m_button_down = True
        if m_button_down == True and event.type == pygame.MOUSEBUTTONUP:
            m_button_down = False
            return True

#Buttons
#Format: x_pos, y_pos, width, height, colourchange, fontchange, text to display, type, action
#colour/font changes: 0 = same as current theme, 1 = always default, 2 = always alt
#Type defines if the button leads to a menu change (0) or a colour/font change (1) or run a function (2) store the current menu, but goes to the action menu (3) or goes to the previous stored node (4)

#General buttons
home_btn = Button(10, 10, 200, 50, 0, 0, "Home", 0, "start")

#Start Menu
start_btn = Button(50, 200, 200, 50, 0, 0, "Start Game", 0, "validation")
how_play_btn = Button(50, 250, 200, 50, 0, 0, "How to play", 0, "how_play")
h_score_btn = Button(50, 300, 200, 50, 0, 0, "Highscores", 0, "scores")
settings_btn = Button(50, 350, 200, 50, 0, 0, "Settings", 3, "settings")
quit_game_btn = Button(50, 400, 200, 50, 0, 0, "Quit game", 0, "quit")
toggle_sounds = Button(50, 500, 220, 50, 0, 0, "Toggle Music", 2, "t_music")
colour1_btn = Button(1000, 200, 155, 50, 1, 0, "Colour 1", 1, "col1")
colour2_btn = Button(1000, 275, 155, 50, 2, 0, "Colour 2", 1, "col2")
font1_btn = Button(1000, 350, 155, 50, 0, 1, " Font 1", 1, "fnt1")
font2_btn = Button(1000, 425, 155, 50, 0, 2, " Font 2", 1, "fnt2")
start_buttons = [start_btn, how_play_btn, h_score_btn, settings_btn, quit_game_btn, toggle_sounds, colour1_btn, colour2_btn, font1_btn, font2_btn]

#Validation page
submit_btn = Button(575, 550, 200, 50, 0, 0, "Start Game", 2, "validate")
validation_buttons = [home_btn, submit_btn]

#How to play page
how_play_buttons = [home_btn]

#Score page
score_buttons = [home_btn]

#quitpage
yes_btn = Button(400, 275, 200, 50, 0, 0, "Yes", 0, "leave_game")
no_btn = Button(700, 275, 200, 50, 0, 0, "No", 0, "start")
quit_page_buttons = [yes_btn, no_btn, home_btn]

#Game Screen
toggle_music_game = Button(25, 350, 220, 50, 0, 0, "Toggle Music", 2, "t_music")
toggle_sound_e_game = Button(25, 400, 230, 50, 0, 0, "Toggle Effects", 2, "t_sound")
pause_btn = Button(25, 475, 200, 50, 0, 0, "Pause", 0, "pause")
game_screen_buttons = [toggle_music_game, toggle_sound_e_game, pause_btn]

#End Game
h_score_btn2 = Button(175, 300, 350, 50, 0, 0, "Leader Board", 0, "scores")
returnto_main = Button(525, 300, 200, 50, 0, 0, "Main Menu", 0, "start")
play_again = Button(825, 300, 200, 50, 0, 0, "Play Again", 0, "game")
end_game_page_buttons = [h_score_btn2, returnto_main, play_again]

#pause screen
resumegame_btn = Button(500, 300, 300, 50, 0, 0, "Resume Game", 0, "game")
settings_btn_2 = Button(175, 300, 200, 50, 0, 0, "Settings", 3, "settings")
endround_btn = Button(900, 300, 200, 50, 0, 0, "End Round", 0, "endround")

pausescreen_buttons = [resumegame_btn, settings_btn_2, endround_btn]

#endround
yes_btn2 = Button(400, 275, 200, 50, 0, 0, "Yes", 0, "start")
no_btn2 = Button(700, 275, 200, 50, 0, 0, "No", 0, "pause")
endround_buttons = [yes_btn2, no_btn2]

#Settings screen
return_btn = Button(10, 10, 200, 50, 0, 0, "Return", 4, "")
settings_btn_2 = Button(175, 300, 200, 50, 0, 0, "Settings", 0, "settings")
endround_btn = Button(900, 300, 200, 50, 0, 0, "End Round", 0, "endround")

settingsmenu_buttons = [return_btn, colour1_btn, colour2_btn, font1_btn, font2_btn]

#################################################### MENU FUNCTIONS #######################################################

#Validation functions
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
#Name validation:

def name_validate(text):
    returnmessage = None
    for letter in text:
        if letter == " ":
            returnmessage = "Name can't contain spaces"

        elif letter in numbers:
            returnmessage =  "Name can't contain numbers"

    if len(text) > 15:
        returnmessage =  "Name is too long, maximum length is 15 characters"

    return returnmessage

#Age validation:
def age_validate(text):
    passed = 2 #a check to make sure that the string is only converted to an int if it contains no spaces or letters - this is to avoid it crashing
    returnmessage = None
    for number in text:
        if number == " ":
            returnmessage =  "Age can't contain spaces"
            passed -= 1

        if number in letters:
            returnmessage =  "Age can't contain letters"
            passed -= 1

    if passed == 2 and text != "":
        numoftext = int(text)
        if numoftext < 10:
            returnmessage = "Sorry, you must be at least 10 years old to play this game"
        elif numoftext >= 150:
            returnmessage = "That seems unlikely, please enter your real age"

    return returnmessage

#Overall validation
#Combining the validations for the submit button before launcing the game
def submit_validate(name_text, age_text):
    name = name_validate(name_text)
    age = age_validate(age_text)

    if name == None and age == None and name_text != "" and age_text != "":
        return True
    else:
        return False

################################## UPDATING SCORE TXT FILE ######################################

def update_score_text(num_high):
    file = open("all scores.txt","r")
    filedata = file.read()
    if num_high == "":
        write_text = user_name_text + " - " + str(score) + "\n" + filedata
    else:
        splitdata = filedata.split(num_high)
        #print(splitdata, "old")
        ogtext = splitdata[0]
        newtext = ogtext + num_high + "\n" + user_name_text + " - " + str(score)
        splitdata[0] = newtext
        #print(splitdata, "new")
        write_text = splitdata[0] + splitdata[1]
    file.close()

    return write_text

def update_score_files():
    #Highscore?
    written = False
    filer = open("high score.txt","r")
    num = ""
    highscore = False
    for line in filer:
        #print("line:", line)
        for letter in line:
            #print("Letter", letter)
            if letter in numbers:
                num += letter
                #print(num)
            fileread = True
        if int(num) < score and written == False:
            filer2 = open("high score.txt","r")
            data = filer2.readline()
            filer2.close()
            #print("data",data)
            f = open("high score.txt","w")
            lineto_write = user_name_text, " - ", str(score)
            f.writelines(lineto_write)
            f.close()
            highscore = True
            allfile = open("all scores.txt","r")
            olddata = allfile.read()
            allfile.close()
            newdata = data + "\n" + olddata
            allfile = open("all scores.txt","w")
            allfile.writelines(newdata)
            written = True
            allfile.close()


    #Not a High Score
    if highscore == False:
        num = ""
        previous_num = ""
        scorefile = open("all scores.txt","r")
        positioned = False
        #Loops each line in the file
        for line in scorefile:
            #loops each letter in the line
            for letter in line:
                #if the character is a number it adds to a thing
                if letter in numbers:
                    num += letter
                    #print(num)

            #At the end of the line, if the lines number is less than the players score
            #Checking if the value of num is "" - the end of the document
            if num == "":
                file = open("all scores.txt","a")
                text = user_name_text + " - " + str(score) + "\n"
                file.writelines(text)
                file.close()
            elif int(num) < score and positioned == False:
                #print("New Score")
                text = update_score_text(previous_num)
                positioned = True
                file = open("all scores.txt","w")
                file.writelines(text)
                file.close

            previous_num = num
            #print("previouse num", previous_num)
            num = ""
        scorefile.close()

############################################## RESET GAME ##################################################

def reset_game():
    global score, health, mins, seconds, enemy_boat1, enemy_boat2, player_boat
    score = 0
    health = 100
    mins = 2
    seconds = 0
    player_boat.goto(1175, 500)
    enemy_boat1.goto(300, 100)
    enemy_boat2.goto(1000, 100)
    enemy_boat1.health = 6
    enemy_boat2.health = 6
    enemy_boat1.colour = (22, 224, 25)
    enemy_boat2.colour = (22, 224, 25)

################################################ TOGLLE MUSIC #####################################################
def toggle_music():
    global music, music_changeto
    if music_changeto == "play":
        #print("toggle music to stop")
        music = 2
        music_changeto = "stop"
    elif music_changeto == "stop":
        #("Toggle music to play")
        music = 1
        music_changeto = "play"

def toggle_sound():
    global s_effects
    #flips the value of the sound effect variable
    if s_effects == 1:
        s_effects = 2
    elif s_effects == 2:
        s_effects = 1



#################################################### MENUS ########################################################
#Menus
#Start Menu
def main_menu():
    global menu, previous_menu
    #Renders the title words
    text = rendertxt_title_current("Ships That Battle")
    text_rect = text.get_rect(center = (swidth/2, 35))
    displaysurf.blit(text, text_rect)

    #Loops each button in the start menu
    for button in start_buttons:
        button.draw()
        #checks if the mouse is over the button
        if button.hover() == True:
            #checks if the button has been clicked on
            if button.clicked() == True:
                if button.type == 0:
                    menu = button.action
                elif button.type == 1:
                    scheme_change(button.action)
                elif button.type == 2:
                    if button.action == "t_music":
                        toggle_music()
                elif button.type == 3:
                    previous_menu = menu
                    menu = button.action
#########################################################################################
#Validation page
def validation_page():
    global menu, active_box, user_name_text, user_age_input, n_message, a_message, mins, seconds
    submit = False

    text = rendertxt_title_current("Ships That Battle")
    text_rect = text.get_rect(center = (swidth/2, 35))
    displaysurf.blit(text, text_rect)

    #Name input
    #Creating title for the box:
    text = rendertxt_standard_current("Name")
    text_rect = text.get_rect(center = (swidth/2, 120))
    displaysurf.blit(text, text_rect)
    #Creates the background box for the input
    name_surf = pygame.Surface((swidth-40, 80))
    name_rect = name_surf.get_rect(topleft=(swidth-(swidth-20), 175))
    #colour is the alternative to whatever the current display colour is
    if active_box == "name":
        name_surf.fill(active_box_col)
    elif current_screen_col == screen_default:
        name_surf.fill(screen_alt)
    else:
        name_surf.fill(screen_default)
    displaysurf.blit(name_surf, (swidth-(swidth-20), 150))

    #Creates a new surface ontop where the content will be written to
    name_text = pygame.Surface((swidth-80, 60))
    name_text.fill(current_screen_col)
    displaysurf.blit(name_text, (swidth-(swidth-40), 160))

    #Writes the text entered to the box, in the middle
    text =current_standard_fnt.render(user_name_text,True, current_text_col)
    text_rect = text.get_rect(center = (swidth/2, 190))
    displaysurf.blit(text, text_rect)

    #Writes the information abt validation below the box
    text =current_standard_fnt.render(n_message,True, txt_error_col)
    text_rect = text.get_rect(center = (swidth/2, 270))
    displaysurf.blit(text, text_rect)

    #Age input
    #works in same way to name box
    #Creating title for the box:
    text =current_standard_fnt.render("Age",True, current_text_col)
    text_rect = text.get_rect(center = (swidth/2, 330))
    displaysurf.blit(text, text_rect)

    age_surf = pygame.Surface((swidth-40, 80))
    age_rect = age_surf.get_rect(topleft=(swidth-(swidth-40), 385))
    if active_box == "age":
        age_surf.fill(active_box_col)
    elif current_screen_col == screen_default:
        age_surf.fill(screen_alt)
    else:
        age_surf.fill(screen_default)
    displaysurf.blit(age_surf, (swidth-(swidth-20), 375))

    age_text = pygame.Surface((swidth-80, 60))
    age_text.fill(current_screen_col)
    displaysurf.blit(age_text, (swidth-(swidth-40), 385))

    text =current_standard_fnt.render(user_age_input,True, current_text_col)
    text_rect = text.get_rect(center = (swidth/2, 415))
    displaysurf.blit(text, text_rect)

    text =current_standard_fnt.render(a_message,True, txt_error_col)
    text_rect = text.get_rect(center = (swidth/2, 500))
    displaysurf.blit(text, text_rect)

    #renders each button in the page
    for button in validation_buttons:
        button.draw()
        #checks if the mouse is over the button
        if button.hover() == True:
            #checks if the button has been clicked on
            #Dont need all the options as this doesnt have any scheme change buttons
            if button.clicked() == True:
                if button.type == 0:
                    menu = button.action
                    if button.action == "game":
                        print("Reset")
                        reset_game()
                        #toggle_colours_gameandmenu()
                elif button.type == 2:
                    submit = True

    #Checks what box has been clicked on to make that the active box
    m_pos = pygame.mouse.get_pos()
    if event.type == MOUSEBUTTONUP:
        if name_rect.collidepoint(m_pos):
            active_box = "name"
        elif age_rect.collidepoint(m_pos):
            active_box = "age"

    #If the backspace is presses takes away the last item in the approprate box
    if event_key_pressed == "\b" and active_box == "name":
        user_name_text = user_name_text[0:-1]

    elif event_key_pressed == "\b" and active_box == "age":
        user_age_input = user_age_input[0:-1]

    elif active_box == "name" and event_key_pressed not in invalid_inputs and len(user_name_text)<60:
        user_name_text += event_key_pressed


    elif active_box == "age" and event_key_pressed not in invalid_inputs and len(user_age_input)<50:
        user_age_input += event_key_pressed

    #Validates the input as you type to give quicker feedback
    n_message = name_validate(user_name_text)
    a_message = age_validate(user_age_input)

    #Runs if the submit button is pressed as 'submit' will be set to true
    if submit == True:
        play_game = submit_validate(user_name_text, user_age_input)
        if play_game == True:
            # To do
            menu = "game"
            reset_game()
            mins = 2
            seconds = 0

#####################################################################################
#How to play page
def how_play():
    global menu

    text =current_title_fnt.render("Ships That Battle",True, current_text_col)
    text_rect = text.get_rect(center = (swidth/2, 35))
    displaysurf.blit(text, text_rect)

    text =current_standard_fnt.render("How to play:",True, current_text_col)
    text_rect = text.get_rect(center = (swidth/2, 100))
    displaysurf.blit(text, text_rect)

    #rendering a backing box for the text.
    #Two are needed as it will highlight the text but keep it the same as the default background for easy reading
    box = pygame.Surface((1200,475))
    #if statement to determin the alternat colour of the big box depending on the background
    if current_screen_col == screen_default:
        box.fill(screen_alt)
    elif current_screen_col == screen_alt:
        box.fill(screen_default)
    displaysurf.blit(box, (25, 125))

    #Adding a new box over the top of the selected background colour
    box = pygame.Surface((1150, 425))
    box.fill(current_screen_col)
    displaysurf.blit(box, (50, 150))

    #Opening a file that will contain the instructions on how to play
    #this will be displayed on the screen after beign read
    file = open("How to play.txt","r") # read only mode
    #has to be read one line at a time to get it on different lines        

    #Starting position - to be incromented each line:
    yposition = 160
    #renderign the text
    for eachline in file:
        eachline = eachline[:-1] #Removes the carrige return at the end of each line from the render
        text = current_standard_fnt.render(eachline, True, current_text_col)
        displaysurf.blit(text, (55, yposition))
        yposition += 35

    #Buttons
    for button in how_play_buttons:
        button.draw()
        #checks if the mouse is over the button
        if button.hover() == True:
            #checks if the button has been clicked on
            if button.clicked() == True:
                if button.type == 0:
                    menu = button.action
                elif button.type == 1:
                    scheme_change(button.action)

########################################################################################
#High Scores
def scores():
    global menu

    text = current_title_fnt.render("Ships That Battle", True, current_text_col)
    text_rect = text.get_rect(center = (swidth/2, 35))
    displaysurf.blit(text, text_rect)

    #Buttons
    for button in score_buttons:
        button.draw()
        #checks if the mouse is over the button
        if button.hover() == True:
            #checks if the button has been clicked on
            if button.clicked() == True:
                if button.type == 0:
                    menu = button.action

    #Page title:
    text = current_standard_fnt.render("High Scores", True, current_text_col)
    text_rect = text.get_rect(center=(swidth/2, 80))
    displaysurf.blit(text, text_rect)

    #box for all scores
    box = pygame.Surface((1000,350))
    box_rect = box.get_rect(center = (swidth/2,sheight/2))
    #Draws an empty box with a border to display the text in later
    #format: surface to draw on, colour, rect, border width, corner rounding
    pygame.draw.rect(displaysurf, current_text_col, box_rect, 5, 10)

    #file handeling and rendering text for the highscore
    filetext = "High Score: "
    file = open("high score.txt","r")
    filetext += file.readline()
    file.close()
    text = current_standard_fnt.render(filetext, True, current_text_col)
    text_rect = text.get_rect(topright = (1115, 535))

    #Background box for High score
    #setup after text so that it is adaptable to the size of the text within
    x, y = text_rect.topright # assigsn the two coords of the topright to the values x and y respectivly
    a, b = text_rect.topleft # same with topleft
    box = pygame.Surface((((x-a)+20),75))
    box_rect = box.get_rect(topright = (x+10, y-20))
    pygame.draw.rect(displaysurf, current_text_col, box_rect, 5, 10)

    #Displaying the text after the box
    displaysurf.blit(text, text_rect)    

    #All scores:
    #middle of each column is 375 and 875
    column_no = 1
    line_no = 1
    yposition = 160
    file = open("all scores.txt","r")
    for line in file:
        filetext = line
        filetext = filetext[:-1] #to remove return at the end of the line
        text = current_standard_fnt.render(filetext, True, current_text_col)
        if column_no == 1:
            middle = 375
            text_rect = text.get_rect(center = (middle,yposition))
            if line_no <= 8:
                line_no += 1
                yposition += 40
            elif line_no > 8:
                line_no = 1
                column_no = 2
                yposition = 160
        if column_no == 2:
            middle = 875
            text_rect = text.get_rect(center = (middle,yposition))
            if line_no <= 8:
                line_no += 1
                yposition += 40
            elif line_no > 8:
                line_no = 1
                column_no = 3

        if column_no == 1 or column_no == 2:
            displaysurf.blit(text,text_rect)
    file.close()
#####################################################################################

#Quit Game
def quitgame():
    global menu

    gamename_txt_title =current_title_fnt.render("Ships That Battle",True, current_text_col)
    text_rect = gamename_txt_title.get_rect(center = (swidth/2, 35))
    displaysurf.blit(gamename_txt_title, text_rect)
    question_text =current_title_fnt.render("Are you sure you want to quit the game?",True, current_text_col)
    text_rect = question_text.get_rect(center = (swidth/2, 150))
    displaysurf.blit(question_text, text_rect)
    for button in quit_page_buttons:
        button.draw()
        #checks if the mouse is over the button
        if button.hover() == True:
            #checks if the button has been clicked on
            if button.clicked() == True:
                if button.type == 0:
                    menu = button.action
                elif button.type == 1:
                    scheme_change(button.action)
##################################### END OF GAME ##############################################

#End of Game
def endgame():
    global menu, mins, seconds

    text =current_title_fnt.render("Ships That Battle",True, current_text_col)
    text_rect = text.get_rect(center = (swidth/2, 35))
    displaysurf.blit(text, text_rect)
    text =current_title_fnt.render("Game Over",True, current_text_col)
    text_rect = text.get_rect(center = (swidth/2, 150))
    displaysurf.blit(text, text_rect)

    #Displying your Score
    textto_render = ("Your Score: "+ str(score))
    text =current_standard_fnt.render(textto_render,True, current_text_col)
    text_rect = text.get_rect(center = (swidth/2, 450))
    displaysurf.blit(text, text_rect)  

    #Displaying high score message if needed
    f = open("high score.txt","r")
    num = ""
    for line in f:
        for letter in line:
            if letter in numbers:
                num += letter
                #print(num)
        if int(num) < score:
            text =current_standard_fnt.render("New High Score",True, txt_error_col)
            text_rect = text.get_rect(center = (swidth/2, 500))
            displaysurf.blit(text, text_rect)

    f.close()                        

    #Buttons
    for button in end_game_page_buttons:
        button.draw()
        #checks if the mouse is over the button
        if button.hover() == True:
            #checks if the button has been clicked on
            if button.clicked() == True:
                if button.type == 0:
                   update_score_files()
                   menu = button.action
                   if button.action == "game":
                        reset_game()
                        #toggle_colours_gameandmenu()
                elif button.type == 1:
                    scheme_change(button.action)

###################################### PAUSE ########################################

def pause():
    global menu, previous_menu

    text =current_title_fnt.render("Ships That Battle",True, current_text_col)
    text_rect = text.get_rect(center = (swidth/2, 35))
    displaysurf.blit(text, text_rect)
    text =current_title_fnt.render("Game Paused",True, current_text_col)
    text_rect = text.get_rect(center = (swidth/2, 150))
    displaysurf.blit(text, text_rect)

    #Displying current Score
    textto_render = ("Your Current Score: "+ str(score))
    text =current_standard_fnt.render(textto_render,True, current_text_col)
    text_rect = text.get_rect(center = (swidth/2, 550))
    displaysurf.blit(text, text_rect)

    #Buttons
    for button in pausescreen_buttons:
        button.draw()
        #checks if the mouse is over the button
        if button.hover() == True:
            #checks if the button has been clicked on
            if button.clicked() == True:
                if button.type == 0:
                    menu = button.action
                elif button.type == 3:
                    previous_menu = menu
                    menu = button.action

################################## SETTINGS ########################################

def settings():
    global menu

    text =current_title_fnt.render("Ships That Battle",True, current_text_col)
    text_rect = text.get_rect(center = (swidth/2, 35))
    displaysurf.blit(text, text_rect)
    text =current_title_fnt.render("Settings",True, current_text_col)
    text_rect = text.get_rect(center = (swidth/2, 150))
    displaysurf.blit(text, text_rect)

    #Buttons
    for button in settingsmenu_buttons:
        button.draw()
        #checks if the mouse is over the button
        if button.hover() == True:
            #checks if the button has been clicked on
            if button.clicked() == True:
                if button.type == 0:
                    menu = button.action
                elif button.type == 1:
                    scheme_change(button.action)
                elif button.type == 2:
                    if button.action == "t_music":
                        toggle_music()
                elif button.type == 4:
                    menu = previous_menu
                    print(previous_menu)

def endround():
    global menu

    text =current_title_fnt.render("Ships That Battle",True, current_text_col)
    text_rect = text.get_rect(center = (swidth/2, 35))
    displaysurf.blit(text, text_rect)
    text =current_title_fnt.render("Are you sure you want to end the round?",True, current_text_col)
    text_rect = text.get_rect(center = (swidth/2, 150))
    displaysurf.blit(text, text_rect)
    text =current_standard_fnt.render("Your progress in the round will be lost",True, current_text_col)
    text_rect = text.get_rect(center = (swidth/2, 200))
    displaysurf.blit(text, text_rect)

    #Buttons
    for button in endround_buttons:
        button.draw()
        #checks if the mouse is over the button
        if button.hover() == True:
            #checks if the button has been clicked on
            if button.clicked() == True:
                if button.type == 0:
                    menu = button.action




################################## GAME FUNCTION #####################################

def run_game():
    global cool_down
    global health
    global score
    global seconds
    global menu
    global graph

    layout(displaysurf)
    #for island in all_islands:
    #island.draw(displaysurf)
    render_text(displaysurf, current_standard_fnt, current_text_col)

    #Addign the new rects of the players and enimis to the all sprites group so they can be rendered together
    allsprites.add(player_boat)
    allsprites.add(enemy_boat1, enemy_boat2)
    #Drawing all the sprites in one go
    for thing in allsprites:
        thing.draw()
        graph = {
    0:{1:75},
    1:{0:75, 2:60},
    2:{1:60, 3:33},
    3:{2:33, 4:72, 8:65},
    4:{3:72, 5:50},
    5:{4:50, 6:50},
    6:{5:50, 7:140, 12:171, 69:58},
    7:{6:140, 13:150, 70:58},
    8:{3:65, 9:85},
    9:{8:85, 10:75, 11:78, 14:90},
    10:{9:75, 11:71, 14:79, 19:105, 20:51},
    11:{9:78, 10:75, 12:70, 20:102},
    12:{6:171, 11:70, 22:60, 23:95, 25:148, 69:130},
    13:{7:150, 24:85, 70:104},
    14:{9:90, 10:79, 15:70},
    15:{14:70, 16:70},
    16:{15:70, 17:60},
    17:{16:60, 18:70, 28:82, 29:97},
    18:{17:70, 19:75},
    19:{10:105, 18:75, 20:81, 30:84},
    20:{10:51, 11:102, 19:81, 21:64, 22:90},
    21:{20:64, 22:70, 30:114, 31:90},
    22:{12:60, 20:90, 21:70, 23:78, 25:64},
    23:{12:95, 24:90, 22:78, 25:77, 26:85},
    24:{23:90, 26:90, 13:85, 27:75},
    25:{12:148, 22:64, 23:77, 26:60},
    26:{25:60, 23:85, 27:50, 24:90},
    27:{24:75, 26:50, 32:40},
    28:{17:82, 29:75, 36:100},
    29:{28:75, 30:115, 17:97},
    30:{19:84, 21:114, 29:115},
    31:{21:90, 35:100},
    32:{27:40, 33:100},
    33:{32:100, 34:80},
    34:{33:80, 45:60},
    35:{31:100, 42:80},
    36:{28:100, 37:80},
    37:{36:80, 38:55, 46:110},
    38:{37:55, 49:110, 39:55},
    39:{38:55, 40:60, 52:110},
    40:{39:60, 41:50},
    41:{40:50, 42:40},
    42:{35:80, 41:40, 43:70, 57:110},
    43:{42:70, 60:110, 44:70},
    44:{43:70, 45:70, 63:110},
    45:{34:60, 44:70, 66:110},
    46:{37:110, 47:100, 49:55},
    47:{46:100, 48:70, 50:55},
    48:{47:70, 51:55},
    49:{38:110, 46:55, 50:100, 52:55},
    50:{47:55, 49:100, 51:70, 53:55},
    51:{48:55, 50:70, 54:55},
    52:{39:110, 49:55, 53:100},
    53:{50:55, 52:100, 54:70, 55:60},
    54:{51:55, 53:70, 56:60},
    55:{53:60, 56:70, 58:90},
    56:{54:60, 55:70, 59:90},
    57:{42:110, 58:100, 60:70},
    58:{55:90, 57:100, 59:70, 61:70},
    59:{56:90, 58:70, 62:70},
    60:{43:110, 57:70, 61:100, 63:70},
    61:{58:70, 60:100, 62:70, 64:70},
    62:{61:70, 59:70, 65:70},
    63:{44:110, 60:70, 64:100, 66:70},
    64:{63:100, 61:70, 65:70, 67:70},
    65:{62:70, 64:70, 68:70},
    66:{45:110, 63:70, 67:100},
    67:{66:100, 64:70, 68:70},
    68:{65:70, 67:70},
    69:{6:58, 12:130, 70:80},
    70:{7:58, 13:104, 69:80}
    }

    #Player Collision with the islands
    if pygame.sprite.spritecollideany(player_boat, islands):
        #Set the island colour to red temperelally
        pygame.sprite.spritecollideany(player_boat, islands).colour(caution_col)
        health = 100
        time_penalty()
        player_boat.goto(swidth - 75, sheight - 50)

    #Shooting player missiles
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if event.type == pygame.MOUSEBUTTONDOWN and mouse_x > 275:
    #Ensures that the mouse is within the gamespace, so that its not shot when clicking buttons
        if event.button == 1 and cool_down <= 0:
            cool_down = 50
            if s_effects == 1:
                pygame.mixer.Sound.play(cannon_sound)
            # Adds a new instance of the bomb to the list
            player_bombs.append(Bomb(player_boat.x, player_boat.y, mouse_x, mouse_y, 0))

    #Players Bullets
    for bullet in player_bombs:
        bullet.move()
        # checks if the bullet colides with an island
        for island in islands:
            if island.rect.collidepoint(bullet.x, bullet.y):
                if s_effects == 1:
                    pygame.mixer.Sound.play(thump)
                bullet.set_crash()

        # Checks if the Bullet collides with an enemy boat
        for enemy in enemies:
            if enemy.rect.collidepoint(bullet.x, bullet.y):
                bullet.set_crash()
                enemy.hit()
                score += 5

    #Enemies bullets
    for bullet in enemy_bombs:
        bullet.move()
        # checks if the bullet colides with an island
        for island in islands:
            if island.rect.collidepoint(bullet.x, bullet.y):
                if s_effects == 1:
                    pygame.mixer.Sound.play(thump)
                bullet.set_crash()

        #Player Boat collision
        if player_boat.rect.collidepoint(bullet.x, bullet.y):
            health -= 5
            bullet.set_crash()

    if health < 1:
        health = 100
        time_penalty()
        player_boat.goto(swidth - 75, sheight - 50)

    for node in nodes:
        node.draw()

    if cool_down > 0:
        cool_down -= 1

    #Loops each button in the start menu
    for button in game_screen_buttons:
        button.draw()
        #checks if the mouse is over the button
        if button.hover() == True:
            #checks if the button has been clicked on
            if button.clicked() == True:
                if button.type == 0:
                    menu = button.action
                elif button.type == 1:
                    scheme_change(button.action)
                elif button.type == 2:
                    if button.action == "t_music":
                        toggle_music()
                    elif button.action == "t_sound":
                        toggle_sound()

    update_time()

################################ CLASSES FOR GAME ###################################
################################## PLAYER BOAT ######################################

class Boat(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.width = 10
        self.height = 10
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
player_boat = Boat(1175, 500)

##################################### ENEMY BOAT ####################################

class Eboat(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.width = 10
        self.height = 10
        self.reset_offset = 0
        self.x_offset = 0
        self.y_offset = 0
        self.colour = (22, 224, 25)
        self.health = 6
        self.randomnode = 80
        self.previous_x = 0
        self.previous_y = 0
        self.boat = pygame.Surface((self.width, self.height))
        self.get_rectgl()
        self.cooldown = 0

    def get_rectgl(self):
        pygame.draw.rect(self.boat, boat_e_col, pygame.Rect(self.x, self.y, self.width, self.height))
        self.rect = self.boat.get_rect()
        self.rect.center = ((self.x), (self.y))

    def draw(self):
        distance = math.sqrt(((player_boat.x - self.x)**2)+((player_boat.y - self.y)**2))
        self.move()
        self.boat.fill(self.colour)
        displaysurf.blit(self.boat, self.rect)

        #print(self.x, self.y)

    def not_moved(self):
        global frame_count
        if frame_count == 30:
            travelled = math.sqrt(((self.x - self.previous_x)**2)+((self.y - self.previous_y)**2))
            self.previous_x = self.x
            self.previous_y = self.y
            if travelled < 10:
                print("Not Moved")
                return True
            else:
                print("Moved")
                return False
        return False
        
        

    def move(self):
        global player_boat
        currentnode = self.current_node()
        #Distance to player
        player_dist = math.sqrt(((player_boat.x - self.x)**2) + ((player_boat.y - self.y)**2))
        if player_dist < 250 and self.not_moved() == False:
            targetnode = self.target_node()

        elif self.randomnode == currentnode or self.randomnode == 80 or self.not_moved() == True:
            randomnum = random.randint(0,70)
            self.randomnode = self.get_node(randomnum)
            targetnode = self.randomnode

        else:
            targetnode = self.randomnode

        #print("Current Node", currentnode.id)
        #print("Target Node", targetnode.id)

        path = self.path(targetnode.id, currentnode.id, graph)
        nextnode = self.get_node(path[0])
        #print("nextnode",nextnode.id)
        if self.x < nextnode.x:
            self.x+=enemy_boat_speed
        if self.x > nextnode.x:
            self.x-=enemy_boat_speed
        if self.y < nextnode.y:
            self.y+=enemy_boat_speed
        if self.y > nextnode.y:
            self.y-=enemy_boat_speed

        self.get_rectgl()
        displaysurf.blit(self.boat, self.rect)

        if self.cooldown == 0:
            self.fire()
        else:
            self.cooldown -= 1

    def target_node(self):
        distances = []
        for eachnode in nodes:
            xdistance = (eachnode.x - player_boat.x)**2
            #print(xdistance)
            ydistance = (eachnode.y - player_boat.y)**2
            #print(ydistance)
            #math.sqrt is the square root
            totaldistance = math.sqrt(xdistance+ydistance)
            #print(totaldistance)
            distances.append(totaldistance)

        #print(distances)
        #math.inf is infinity
        #high number so that all routes are shorter
        smallestdis = math.inf

        #sets the closest node to 0 - this will be changed
        closenode = 0
        #print((len(distances)-1))

        for i in range (len(distances)):
            if distances[i] < smallestdis:
                smallestdis = distances[i]
                closenode = i

        #print(closenode)
        return self.get_node(closenode)

    def current_node(self):
        distances = []
        for eachnode in nodes:
            xdistance = (eachnode.x - self.x)**2
            #print(xdistance)
            ydistance = (eachnode.y - self.y)**2
            #print(ydistance)
            #math.sqrt is the square root
            totaldistance = math.sqrt(xdistance+ydistance)
            #print(totaldistance)
            distances.append(totaldistance)

        #print(distances)
        #math.inf is infinity
        #high number so that all routes are shorter
        smallestdis = math.inf

        #sets the closest node to 0 - this will be changed
        closenode = 0
        #print((len(distances)-1))

        for i in range (len(distances)):
            if distances[i] < smallestdis:
                smallestdis = distances[i]
                closenode = i

        #print(closenode)

        return self.get_node(closenode)

    def goto(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos
        self.rect = self.boat.get_rect(topleft=(self.x, self.y))
        displaysurf.blit(self.boat, self.rect)
        pygame.display.update()

    def path(self, currentnode, targetnode, graph):
        previouse_node = {}
        distances = {}

        #sets the distance between each node to infinity
        for i in graph:
            distances[i] = math.inf

        distances[currentnode] = 0

        while graph:
        #finding the node that needs to be explored (with the shortest distance)
            shortest = None

            for node in graph:
                if shortest == None:
                    shortest = node
                elif distances[node] < distances[shortest]:
                    shortest = node
                #print(shortest)

            for connection, dist in graph[shortest].items():
                #print("Connection",connection,"Distance", dist)

                if connection in graph:
                    #print("In graph")
                    if distances[connection] > (dist + distances[shortest]):
                        distances[connection] = (dist + distances[shortest])
                        previouse_node[connection] = shortest

                #print("distances", distances)
                #print("previouse", previouse_node)

            graph.pop(shortest)
            #print("graph",graph)
        #print("Exited loop")

        shortest_path = [targetnode]
        location = targetnode
        while location != currentnode:
            #print("location",location)
            toadd = previouse_node[location]
            shortest_path.insert(0,toadd)
            location = toadd
        shortest_path.reverse()
        if len(shortest_path) > 1:
            shortest_path.pop(0)
        #print("Shorest path:", shortest_path)    
        return shortest_path

    def get_node(self, id):
        if id == 0:
            return node0
        elif id == 1:
            return node1
        elif id == 2:
            return node2
        elif id == 3:
            return node3
        elif id == 4:
            return node4
        elif id == 5:
            return node5
        elif id == 6:
            return node6
        elif id == 7:
            return node7
        elif id == 8:
            return node8
        elif id == 9:
            return node9
        elif id == 10:
            return node10
        elif id == 11:
            return node11
        elif id == 12:
            return node12
        elif id == 13:
            return node13
        elif id == 14:
            return node14
        elif id == 15:
            return node15
        elif id == 16:
            return node16
        elif id == 17:
            return node17
        elif id == 18:
            return node18
        elif id == 19:
            return node19
        elif id == 20:
            return node20
        elif id == 21:
            return node21
        elif id == 22:
            return node22
        elif id == 23:
            return node23
        elif id == 24:
            return node24
        elif id == 25:
            return node26
        elif id == 27:
            return node27
        elif id == 28:
            return node28
        elif id == 29:
            return node29
        elif id == 30:
            return node30
        elif id == 31:
            return node31
        elif id == 31:
            return node31
        elif id == 32:
            return node32
        elif id == 33:
            return node33
        elif id == 34:
            return node34
        elif id == 35:
            return node35
        elif id == 36:
            return node36
        elif id == 37:
            return node37
        elif id == 38:
            return node38
        elif id == 39:
            return node39
        elif id == 40:
            return node40
        elif id == 41:
            return node41
        elif id == 42:
            return node42
        elif id == 43:
            return node43
        elif id == 44:
            return node44
        elif id == 45:
            return node45
        elif id == 46:
            return node46
        elif id == 47:
            return node47
        elif id == 48:
            return node48
        elif id == 49:
            return node49
        elif id == 50:
            return node50
        elif id == 51:
            return node51
        elif id == 52:
            return node52
        elif id == 53:
            return node53
        elif id == 54:
            return node54
        elif id == 55:
            return node55
        elif id == 56:
            return node56
        elif id == 57:
            return node57
        elif id == 58:
            return node58
        elif id == 59:
            return node59
        elif id == 60:
            return node60
        elif id == 61:
            return node61
        elif id == 62:
            return node62
        elif id == 63:
            return node63
        elif id == 64:
            return node64
        elif id == 65:
            return node65
        elif id == 66:
            return node66
        elif id == 67:
            return node67
        elif id == 68:
            return node68
        elif id == 69:
            return node69
        elif id == 70:
            return node70
        else:
            return node0

    def hit(self):
        global score
        sound = 1
        self.health -= 1
        if self.health == 5:
            self.colour = (113, 224, 22)
        elif self.health == 4:
            self.colour = (170, 224, 22)
        elif self.health == 3:
            self.colour = (224, 211, 22)
        elif self.health == 2:
            self.colour = (224, 110, 22)
        elif self.health == 1:
            self.colour = (224, 22, 22)
        elif self.health == 0:
            #print("Sink")
            self.sink()
            sound = 2
        if sound == 1:
            if s_effects == 1:
                pygame.mixer.Sound.play(wood_crash)
        else:
            if s_effects == 1:
                pygame.mixer.Sound.play(ship_sink)
            score += 5

    def fire(self):
        x_distance = (self.x - player_boat.x)**2
        y_distance = (self.y - player_boat.y)**2
        distance = math.sqrt(x_distance + y_distance)
        if distance < 75:
            enemy_bombs.append(Bomb(self.x, self.y, player_boat.x, player_boat.y, 1))
            self.cooldown = 100
            if s_effects == 1:
                pygame.mixer.Sound.play(cannon_sound)

    def sink(self):
        self.goto(1000,1000)
        self.health = 6
        self.colour = (22, 224, 25)

enemy_boat1 = Eboat(300, 100)
enemy_boat2 = Eboat(1000, 100)

###################################### BOMBS ########################################
class Bomb:
    def __init__(self, x_pos, y_pos, target_x_pos, target_y_pos, type):
        self.x = x_pos
        self.y = y_pos
        self.speed = 7
        self.crash = False
        # life defines how long the missile will last before 'crashing into the sea'
        self.life = 15
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
            if s_effects == 1:
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

################################### ISLANDS #########################################

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

#x_pos, y_pos, width, height
island1 = Island(650, 350, 200, 150)
island2 = Island(775, 100, 75, 200)
island3 = Island(950, 200, 100, 50)
island4 = Island(375, 50, 50, 160)
island5 = Island(550, 125, 50, 75)
island6 = Island(350, 250, 75, 100)
island7 = Island(400, 450, 100, 50)

######################################## NODES ##############################################

class Node(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, id):
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.width = 10
        self.height = 10
        self.id = id
        self.surf = pygame.Surface((self.width, self.height))
        self.rect = self.surf.get_rect()
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        self.surf.fill(black)
        displaysurf.blit(self.surf, (self.x, self.y))


######################### GROUPING THINGS TOGETHER ##################################
player_bombs = []
enemy_bombs = []

islands = pygame.sprite.Group()
islands.add(island1, island2, island3, island4, island5, island6, island7)


allsprites = pygame.sprite.Group()
allsprites.add(island1, island2, island3, island4, island5, island6, island7)

enemies = pygame.sprite.Group()
enemies.add(enemy_boat1, enemy_boat2)

node0 = Node(300, 50, 0)
node1 = Node(300, 125, 1)
node2 = Node(300, 185, 2)
node3 = Node(300, 218, 3)
node4 = Node(300, 290, 4)
node5 = Node(300, 340, 5)
node6 = Node(300, 390, 6)
node7 = Node(300, 530, 7)
node8 = Node(365, 225, 8)
node9 = Node(450, 225, 9)
node10 = Node(525, 225, 10)
node11 = Node(470, 300, 11)
node12 = Node(470, 370, 12)
node13 = Node(450, 530, 13)
node14 = Node(500, 150, 14)
node15 = Node(500, 80, 15)
node16 = Node(570, 80, 16)
node17 = Node(630, 80, 17)
node18 = Node(630, 150, 18)
node19 = Node(630, 225, 19)
node20 = Node(570, 280, 20)
node21 = Node(620, 320, 21)
node22 = Node(570, 370, 22)
node23 = Node(535, 440, 23)
node24 = Node(535, 530, 24)
node25 = Node(610, 420, 25)
node26 = Node(610, 480, 26)
node27 = Node(610, 530, 27)
node28 = Node(710, 60, 28)
node29 = Node(710, 135, 29)
node30 = Node(710, 250, 30)
node31 = Node(710, 320, 31)
node32 = Node(650, 530, 32)
node33 = Node(750, 530, 33)
node34 = Node(830, 530, 34)
node35 = Node(810, 320, 35)
node36 = Node(810, 60, 36)
node37 = Node(890, 60, 37)
node38 = Node(890, 115, 38)
node39 = Node(890, 170, 39)
node40 = Node(890, 230, 40)
node41 = Node(890, 280, 41)
node42 = Node(890, 320, 42)
node43 = Node(890, 390, 43)
node44 = Node(890, 460, 44)
node45 = Node(890, 530, 45)
node46 = Node(1000, 60, 46)
node47 = Node(1100, 60, 47)
node48 = Node(1170, 60, 48)
node49 = Node(1000, 115, 49)
node50 = Node(1100, 115, 50)
node51 = Node(1170, 115, 51)
node52 = Node(1000, 170, 52)
node53 = Node(1100, 170, 53)
node54 = Node(1170, 170, 54)
node55 = Node(1100, 230, 55)
node56 = Node(1170, 230, 56)
node57 = Node(1000, 320, 57)
node58 = Node(1100, 320, 58)
node59 = Node(1170, 320, 59)
node60 = Node(1000, 390, 60)
node61 = Node(1100, 390, 61)
node62 = Node(1170, 390, 62)
node63 = Node(1000, 460, 63)
node64 = Node(1100, 460, 64)
node65 = Node(1170, 460, 65)
node66 = Node(1000, 530, 66)
node67 = Node(1100, 530, 67)
node68 = Node(1170, 530, 68)
node69 = Node(350, 420, 69)
node70 = Node(350, 500, 70)


nodes = pygame.sprite.Group()
nodes.add(
node0,node1,node2,node3,node4,node5,node6,node7,node8,node9,node10,node11,node12,node13,node14,node15,node16,node17,node18,node19,
node20,node21,node22,node23,node24,node25,node26,node27,node28,node29,node30,node31,node32,node33,node34,node35,node36,node37,node38,node39,
node40,node41,node42,node43,node44,node45,node46,node47,node48,node49,node50,node51,node52,node53,node54,node55,node56,node57,node58,node59,
node60,node61,node62,node63,node64,node65,node66,node67,node68,node69,node70)

############################# FUNCTIONS FOR THE GAME##################################
############################ GENERAL LAYOUT OF SCREEN ################################

def layout(displaysurf):
    displaysurf.fill(current_screen_col)

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

################################ TEXT ON BOXES #######################################
#Rendering text on boxes
def render_text(displaysurf, current_standard_fnt, current_text_col):
#Health Text
    textto_render = "Health: " + str(health)
    text = current_standard_fnt.render(textto_render,True, current_text_col)
    text_rect = text.get_rect(center = (137.5, 150))
    displaysurf.blit(text,text_rect)
#Score text
    textto_render = "Score: "+ str(score)
    text = current_standard_fnt.render(textto_render, True, current_text_col)
    text_rect = text.get_rect(center = (137.5, 250))
    displaysurf.blit(text,text_rect)
#Time
    if seconds <10:
        textto_render = str(mins)+":0"+str(seconds)
    else:
        textto_render = str(mins)+":"+str(seconds)

    text = current_standard_fnt.render(textto_render, True, current_text_col)
    text_rect = text.get_rect(center = (137.5, 50))
    displaysurf.blit(text,text_rect)

######################################## TIMER UPDATES ###########################################

def update_time():
    global mins
    global seconds
    global frame_count
    global menu

    if frame_count == 60:
        seconds -= 1
        frame_count = 0
    if mins == 0 and seconds == 0:
        menu = "endgame"
    if seconds == 0:
        mins -= 1
        seconds = 59

    frame_count += 1

def time_penalty():
    global mins
    global seconds
    global menu

    if seconds > 9:
        seconds -= 10
    elif mins < 1 and seconds < 10 :
        menu = "endgame"
    else:
        mins = 0
        take_off = 10 - seconds #to get how many from the next minute too
        seconds = 60 - take_off

#################################### GAME LOOP #######################################
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

    if music == 1:
        #print("Play Music")
        # Play the music:
        mixer.music.play(-1)
        music = 3
    elif music == 2:
        #print("stop music")
        mixer.music.stop()
        music = 3

    if menu == "start":
        main_menu()

    if menu == "validation":
        validation_page()

    if menu == "how_play":
        how_play()

    if menu == "scores":
        scores()

    if menu == "settings":
        settings()

    if menu == "quit":
        quitgame()

    if menu == "leave_game":
        pygame.quit()
        sys.exit()

    if menu == "game":
        run_game()

    if menu == "endgame":
        endgame()

    if menu == "pause":
        pause()

    if menu == "endround":
        endround()

    pygame.display.update()
    pygame.display.flip()
    framesps.tick(FPS)