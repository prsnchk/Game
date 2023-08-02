import random

import os

import pygame

from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

# Initialize Pygame
pygame.init() 
pygame.mixer.init()

# Set the frame rate
FPS = pygame.time.Clock()

# Set the screen dimensions
HEIGHT = 700
WIDTH = 1000

# Set the font for displaying text
FONT = pygame.font.SysFont('Verduna',20)

# Define some color constants
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_RED = (255, 0, 0)

# Create the main game display window
main_display = pygame.display.set_mode((WIDTH, HEIGHT))

# Load and play the background music
pygame.mixer.music.load('Batko_nash_Bandera.mp3')
pygame.mixer.music.play(1)

# Load other sound effects used in the game
game_over_music = pygame.mixer.Sound('Game_over.mp3')
bonus_sound = pygame.mixer.Sound('Bonus.mp3')

# Load and set the background image
bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

# Define the path and load images for the player
IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)


# Player settings
player_size = (20, 20)
player = pygame.image.load('player.png').convert_alpha()
player_rect = player.get_rect()
player_rect.center = [100, 300]
main_display.get_rect().center

player_move_down = [0, 4]
player_move_right = [4, 0]
player_move_top = [0, -4]
player_move_left = [-4, 0]

# Function to show the "Game Over" screen
def show_game_over_screen():
    main_display.fill(COLOR_BLACK)
    game_over_text = FONT.render("Game Over", True, COLOR_WHITE)
    text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    main_display.blit(game_over_text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

def show_game_over_screen():
    pygame.mixer.music.pause()
    
    main_display.fill(COLOR_BLACK)
    game_over_text = FONT.render("Game Over", True, COLOR_WHITE)
    text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    main_display.blit(game_over_text, text_rect)
    pygame.display.flip()
    
    # Play the game over music
    game_over_music.play()
    
    pygame.time.wait(2000)
    
    # Stop the game over music after waiting
    game_over_music.stop()

# Function to create an enemy object
def create_enemy():
    enemy_sound = pygame.mixer.Sound('Enemy.mp3')
    enemy_size = (30,30)
    enemy = pygame.image.load('enemy.png').convert_alpha()
    enemy_rect = pygame.Rect(WIDTH,
                            random.randint(enemy.get_height(),HEIGHT - enemy.get_height()),
                            *enemy.get_size())                      
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move, enemy_sound]
 
# Function to create a bonus object
def create_bonus():
    bonus = pygame.image.load('bonus.png').convert_alpha()
    bonus_move = [0, random.randint(4, 8)]
    bonus_width = bonus.get_width()
    bonus_rect = pygame.Rect(random.randint(bonus_width, WIDTH - bonus_width),
                              -bonus.get_height(), 
                              *bonus.get_size())
    return [bonus, bonus_rect, bonus_move]

# Function to create another type of bonus object
def create_bonus2():
    bonus2 = pygame.image.load('bonus2.png').convert_alpha()
    bonus2_move = [0, random.randint(4, 8)]
    bonus2_width = bonus2.get_width()
    bonus2_rect = pygame.Rect(random.randint(bonus2_width, WIDTH - bonus2_width),
                              -bonus2.get_height(),
                              *bonus2.get_size())
    return [bonus2, bonus2_rect, bonus2_move]

# Set up custom events for creating enemies and bonuses
CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)

CREATE_BONUS2 = pygame.USEREVENT + 4
pygame.time.set_timer(CREATE_BONUS2, 5000)

CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

# Lists to store enemies and bonuses
enemies = []
bonuses = []

# Initialize the player's score
score = 0

# Index for changing the player's image
image_index = 0

# Variables to control game flow
playing = True
game_over = False 

# Game loop
playing = True
while playing:
    # Set the frame rate
    FPS.tick(120)

    # If the game is over, show the "Game Over" screen and stop the game
    if game_over:
        show_game_over_screen()
        playing = False
        break

    # Check for events
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append (create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CREATE_BONUS2:
            bonuses.append(create_bonus2())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0
   
    
    # Move the background
    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < - bg.get_width():
        bg_X2 = bg.get_width()

    # Draw the background
    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))


    # Player movement
    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move (player_move_down)
 
    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_top)

    if keys [K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    # Update and draw enemies
    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        # Check for collisions with the player
        if player_rect.colliderect(enemy[1]):
            game_over = True
            
    # Update and draw bonuses        
    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        # Check for collisions with the player
        if player_rect.colliderect(bonus[1]):
        # Play the bonus sound effect when the player collides with the bonus
         bonus_sound.play()
         if player_rect.colliderect(bonus[1]):
          score += 1
          bonuses.pop(bonuses.index(bonus))

    # Display the player's score
    main_display.blit(FONT.render(str(score),True, COLOR_BLACK),(WIDTH-50,20))

    # Draw the player if the game is not over
    if not game_over:
         main_display.blit(player, player_rect)
         
    # Update the display
    pygame.display.flip()  
 
    # Remove enemies that have passed the screen
    for enemy in enemies:
        if enemy[1].right < 0:
         enemies.pop(enemies.index(enemy))

    # Remove bonuses that have passed the screen
    for bonus in bonuses:
        if bonus[1].bottom > HEIGHT:
         bonuses.pop(bonuses.index(bonus))   
   