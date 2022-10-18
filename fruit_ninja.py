# import libraries
import pygame, sys
import os
import random

player_lives = 3                                                #keeps track of remaining lives
score = 0                                                       #keeps track of score
fruits = ['melon', 'orange', 'pomegranate', 'guava', 'bomb']    #entities in the game

# create display window and initialize pygame
WIDTH = 800
HEIGHT = 500
FPS = 12                                                        #refreshes gameDisplay every 1/12th second

pygame.init()
pygame.display.set_caption('FRUIT NINJA GAME')                  #set the caption of the game window
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))          #set the game display size
clock = pygame.time.Clock()

# define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

gameDisplay.fill((BLACK))
background = pygame.image.load('back.jpg')                      #game background image
font = pygame.font.Font(os.path.join(os.getcwd(), 'comic.ttf'), 42)
score_text = font.render('Score : ' + str(score), True, (255,255,255)) #displays the score
lives_icon = pygame.image.load('images/white_lives.png')         #images showing the remaining lives

# generate random fruits and generalize structure
def generate_random_fruits(fruit):
    fruit_path = "images/" + fruit + ".png"
    data[fruit] = {
        'img': pygame.image.load(fruit_path),
        'x' : random.randint(100,500),                          #the fruit's position on the x-coordinate  
        'y' : 800,                                              #the fruit's position on the y-coordinate
        'speed_x': random.randint(-10,10),                      #key to control the speed and diagonal movements of the fruits in the x-direction
        'speed_y': random.randint(-80, -60),                    #key to control the speed and diagonal movements of the fruits in the y-direction (UP)
        'throw': False,                                         #key to determine if the fruit's coordinate is outside the gameplay
        't': 0,                               
        'hit': False,
    }
    if random.random() >= 0.75:                                #return the next random floating-point number in the range [0.0, 1.0) to keep the fruits inside the gameDisplay
        data[fruit]['throw'] = True
    else:
        data[fruit]['throw'] = False

# dictionary used to hold the data of the random fruit generation
data = {}                                                      
for fruit in fruits:
    generate_random_fruits(fruit)

def hide_cross_lives(x, y):
    gameDisplay.blit(pygame.image.load("images/red_lives.png"), (x, y))     #what does this do??

# Generic method to draw fonts on the screen
font_name = pygame.font.match_font('comic.ttf')
def draw_text(display, text, size, x, y):                       #function to help draw text on the screen
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    gameDisplay.blit(text_surface, text_rect)                   # blit() draws images or writes text at a specific position

# draw players lives
def draw_lives(display, x, y, lives, image) :
    for i in range(lives) :
        img = pygame.image.load(image)
        img_rect = img.get_rect()                               #gets the (x,y) coordinates of the cross icons (lives on the the top rightmost side)
        img_rect.x = int(x + 35 * i)                            #sets the next cross icon 35 pixels from the previous one
        img_rect.y = y                                          #takes care of how many pixels the cross icon should be positioned from the top of the screen
        display.blit(img, img_rect)

# show game over display & front display
def show_gameover_screen():
    gameDisplay.blit(background, (0,0))
    draw_text(gameDisplay, "FRUIT NINJA!", 90, WIDTH / 2, HEIGHT / 4)
    if not game_over :
        draw_text(gameDisplay,"Score : " + str(score), 50, WIDTH / 2, HEIGHT /2)

    draw_text(gameDisplay, "Press a key to begin!", 64, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()                                       #updates the screen
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                       #game quits
                pygame.quit()
            if event.type == pygame.KEYUP:                      #event that occurs when the key is pressed and released
                waiting = False

# Game Loop
first_round = True
game_over = True        #terminates the game While loop if more than 3-Bombs are cut
game_running = True     #used to manage the game loop
while game_running :
    if game_over :
        if first_round :
            show_gameover_screen()
            first_round = False
        game_over = False
        player_lives = 3
        draw_lives(gameDisplay, 690, 5, player_lives, 'images/red_lives.png')
        score = 0

    for event in pygame.event.get():
        # checking for closing window
        if event.type == pygame.QUIT:
            game_running = False

    gameDisplay.blit(background, (0, 0))
    gameDisplay.blit(score_text, (0, 0))
    draw_lives(gameDisplay, 690, 5, player_lives, 'images/red_lives.png')

    for key, value in data.items():
        if value['throw']:
            value['x'] += value['speed_x']          #moving the fruits in x-coordinates
            value['y'] += value['speed_y']          #moving the fruits in y-coordinate
            value['speed_y'] += (1 * value['t'])    #increasing y-corrdinate
            value['t'] += 1                         #increasing speed_y for next loop

            if value['y'] <= 800:
                gameDisplay.blit(value['img'], (value['x'], value['y']))    #displaying the fruit inside screen dynamically
            else:
                generate_random_fruits(key)

            current_position = pygame.mouse.get_pos()   #gets the current coordinate (x, y) in pixels of the mouse

            if not value['hit'] and current_position[0] > value['x'] and current_position[0] < value['x']+60 \
                    and current_position[1] > value['y'] and current_position[1] < value['y']+60:
                if key == 'bomb':
                    player_lives -= 1
                    if player_lives == 0:
                        
                        hide_cross_lives(690, 15)
                    elif player_lives == 1 :
                        hide_cross_lives(725, 15)
                    elif player_lives == 2 :
                        hide_cross_lives(760, 15)
                    #if the user clicks bombs for three time, GAME OVER message should be displayed and the window should be reset
                    if player_lives < 0 :
                        show_gameover_screen()
                        game_over = True

                    half_fruit_path = "images/explosion.png"
                else:
                    half_fruit_path = "images/" + "half_" + key + ".png"

                value['img'] = pygame.image.load(half_fruit_path)
                value['speed_x'] += 10
                if key != 'bomb' :
                    score += 1
                score_text = font.render('Score : ' + str(score), True, (255, 255, 255))
                value['hit'] = True
        else:
            generate_random_fruits(key)

    pygame.display.update()
    clock.tick(FPS)      # keep loop running at the right speed (manages the frame/second. The loop should update afer every 1/12th pf the sec
                        

pygame.quit()
