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
menu = "endgame" #so that the start menu loads on start up
user_name_text = ""
user_age_input = ""
active_box = None
invalid_inputs = [None, "\b", "\n", "\t", "\r", "^[", '"', "#"] 
n_message = ""
a_message = ""
boat_speed = 0.5
enemy_boat_speed = 0.25
cool_down = 0  # the cooldown for between missile fires
score = 0
health = 100
mins = 2
seconds = 0
frame_count = 0

######################################################################################
#Importing music and audio
#This is the background audio which will repeat
mixer.music.load("background.mp3")
#These are the sound effects that will play over the top of the background music
cannon_sound = pygame.mixer.Sound("cannon2.wav")
wood_crash = pygame.mixer.Sound("wood_hit.wav")
water_splosh = pygame.mixer.Sound("water_splosh.wav")
ship_sink = pygame.mixer.Sound("ship_sink.wav")
thump = pygame.mixer.Sound("thump.wav")

# Play the music:
mixer.music.play(-1)

######################################################################################

#Colours
screen_default = (88, 155, 213)
screen_alt = (0, 32, 96)
current_screen_col = screen_default

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
menu_col = (128, 128, 128)
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
FPS = 120
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
        if event.type == pygame.MOUSEBUTTONUP and self.hover() == True:
            return True

#Buttons
#Format: x_pos, y_pos, width, height, colourchange, fontchange, text to display, type, action
#colour/font changes: 0 = same as current theme, 1 = always default, 2 = always alt
#Type defines if the button leads to a menu change (0) or a colour/font change (1) or run a function (2)

#General buttons
home_btn = Button(10, 10, 200, 50, 0, 0, "Home", 0, "start")

#Start Menu
start_btn = Button(50, 200, 200, 50, 0, 0, "Start Game", 0, "validation")
how_play_btn = Button(50, 250, 200, 50, 0, 0, "How to play", 0, "how_play")
h_score_btn = Button(50, 300, 200, 50, 0, 0, "Highscores", 0, "scores")
settings_btn = Button(50, 350, 200, 50, 0, 0, "Settings", 0, "start")
quit_game_btn = Button(50, 400, 200, 50, 0, 0, "Quit game", 0, "quit")
colour1_btn = Button(1000, 200, 155, 50, 1, 0, "Colour 1", 1, "col1")
colour2_btn = Button(1000, 275, 155, 50, 2, 0, "Colour 2", 1, "col2")
font1_btn = Button(1000, 350, 155, 50, 0, 1, " Font 1", 1, "fnt1")
font2_btn = Button(1000, 425, 155, 50, 0, 2, " Font 2", 1, "fnt2")
start_buttons = [start_btn, how_play_btn, h_score_btn, settings_btn, quit_game_btn, colour1_btn, colour2_btn, font1_btn, font2_btn]

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

#End Game
h_score_btn2 = Button(525, 300, 200, 50, 0, 0, "Leader Board", 0, "scores")

#########################################################################################

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

#####################################################################################

#Menus
#Start Menu
def main_menu():
    global menu
    #Renders the title words
    text = rendertxt_title_current("Ships That Battle")
    text_rect = text.get_rect(center = (swidth/2, 30))
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
#########################################################################################
#Validation page
def validation_page():
    global menu
    global active_box
    global user_name_text
    global user_age_input
    global n_message
    global a_message
    submit = False

    text = rendertxt_title_current("Ships That Battle")
    text_rect = text.get_rect(center = (swidth/2, 30))
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

#####################################################################################
#How to play page
def how_play():
    global menu

    text =current_title_fnt.render("Ships That Battle",True, current_text_col)
    text_rect = text.get_rect(center = (swidth/2, 30))
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
    text_rect = text.get_rect(center = (swidth/2, 30))
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
    text_rect = gamename_txt_title.get_rect(center = (swidth/2, 30))
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

#Quit Game
def endgame():
    global menu

    text =current_title_fnt.render("Ships That Battle",True, current_text_col)
    text_rect = text.get_rect(center = (swidth/2, 30))
    displaysurf.blit(text, text_rect)
    text =current_title_fnt.render("Game Over",True, current_text_col)
    text_rect = text.get_rect(center = (swidth/2, 150))
    displaysurf.blit(text, text_rect)
    #Buttons
    for button in end_game_page_buttons:
        button.draw()
        #checks if the mouse is over the button
        if button.hover() == True:
            #checks if the button has been clicked on
            if button.clicked() == True:
                if button.type == 0:
                    menu = button.action
                elif button.type == 1:
                    scheme_change(button.action)

################################## GAME FUNCTION #####################################

def run_game():
    global cool_down
    global health
    global score
    global seconds
    global menu

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

    #Player Collision with the islands
    if pygame.sprite.spritecollideany(player_boat, islands):
        #Set the island colour to red temperelally
        pygame.sprite.spritecollideany(player_boat, islands).colour(caution_col)
        health = 100
        time_penalty()
        player_boat.goto(swidth - 75, sheight - 50)

    #Shooting player missiles
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1 and cool_down <= 0:
            cool_down = 50
            pygame.mixer.Sound.play(cannon_sound)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Adds a new instance of the bomb to the list
            player_bombs.append(Bomb(player_boat.x, player_boat.y, mouse_x, mouse_y, 0))

    #Players Bullets
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

    #Enemies bullets
    for bullet in enemy_bombs:
        bullet.move()
        # checks if the bullet colides with an island
        for island in islands:
            if island.rect.collidepoint(bullet.x, bullet.y):
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


    if cool_down > 0:
        cool_down -= 1

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
        self.boat = pygame.Surface((self.width, self.height))
        self.get_rectgl()
        self.cooldown = 0

    def get_rectgl(self):
        pygame.draw.rect(self.boat, boat_e_col, pygame.Rect(self.x, self.y, self.width, self.height))
        self.rect = self.boat.get_rect()
        self.rect.center = ((self.x), (self.y))

    def draw(self):
        distance = math.sqrt(((player_boat.x - self.x)**2)+((player_boat.y - self.y)**2))
        if distance <200:
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
        if distance < 75:
            enemy_bombs.append(Bomb(self.x, self.y, player_boat.x, player_boat.y, 1))
            self.cooldown = 100
            pygame.mixer.Sound.play(cannon_sound)
enemy_boat1 = Eboat(300, 100)
enemy_boat2 = Eboat(300, 500)

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

######################### GROUPING THINGS TOGETHER ##################################
player_bombs = []
enemy_bombs = []

islands = pygame.sprite.Group()
islands.add(island1, island2, island3, island4, island5, island6, island7)


allsprites = pygame.sprite.Group()
allsprites.add(island1, island2, island3, island4, island5, island6, island7)

enemies = pygame.sprite.Group()
enemies.add(enemy_boat1, enemy_boat2)

############################# FUNCTIONS FOR THE GAME##################################
############################ GENERAL LAYOUT OF SCREEN ################################

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

    if frame_count == 120:
        seconds -= 1
        frame_count = 0
    if mins == 0 and seconds == 0:
        print("Update")
        menu = "start"
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
        print("penalty")
        menu = "start"
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

    if menu == "start":
        main_menu()

    if menu == "validation":
        validation_page()

    if menu == "how_play":
        how_play()

    if menu == "scores":
        scores()

    if menu == "quit":
        quitgame()
    
    if menu == "leave_game":
        pygame.quit()
        sys.exit()

    if menu == "game":
        run_game()

    if menu == "endgame":
        endgame()

    pygame.display.update()
    pygame.display.flip()
    framesps.tick(FPS)