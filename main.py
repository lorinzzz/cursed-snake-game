# implementation notes:
# multiple snakes (upwards of 8, user can choose how many to spawn in)
# user can choose what food he is 
# the food can be moved diagonally, while the snakes move like they originally do
# snakes, however cannot be killed by colliding with themselves or other snakes
# the user (food) can be powered up by becoming poison, and thus can kill the snakes by running into them. this will be the only way for a snake to die
# and as usual, the food can only be eaten by the snake's head
# food can collide with snake body, and cannot be moved past it, but will not die
# drip poison powerup !?!
# sprint/slow movement function for apple!
# sprint powerup?

import pygame
import os
import random

WIDTH, HEIGHT = 900, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cursed Snake Game")

BLOCK_WIDTH, BLOCK_HEIGHT = 30, 30

VEL = 2
STAMINA = 100
FPS = 60
REGENERATE_STAMINA = 1000 #regenerate stamina every second
USE_STAMINA = 20 # drain a percentage of stamina every 20ms == depletes full bar in 2 seconds
POISON_TIME = 5000 # poison booster lasts only 5 seconds

regen_stamina_event = pygame.USEREVENT + 1
use_stamina_event = pygame.USEREVENT + 2
poison_time_event = pygame.USEREVENT + 3
food_collided_head_event = pygame.USEREVENT + 4

BLACK = (0,0,0)
WHITE = (255,255,255)

FOOD_IMG = pygame.image.load(os.path.join('Assets', 'apple.png'))
FOOD = pygame.transform.scale(FOOD_IMG, (BLOCK_WIDTH, BLOCK_HEIGHT))
POISON_FOOD_IMG = pygame.image.load(os.path.join('Assets', 'poison_apple.png'))
POISON_FOOD = pygame.transform.scale(POISON_FOOD_IMG, (BLOCK_WIDTH, BLOCK_HEIGHT))

SNAKE_BODY_IMG = pygame.image.load(os.path.join('Assets', 'snake_body.png'))
SNAKE_BODY = pygame.transform.scale(SNAKE_BODY_IMG, (BLOCK_WIDTH, BLOCK_HEIGHT))
SNAKE_HEAD_IMG = pygame.image.load(os.path.join('Assets', 'snake_head.png'))


# function to spawn snake head with appropriate image orientation based on movement direction
def spawn_snake_head(direction):
    SNAKE_HEAD = pygame.transform.rotate(pygame.transform.scale(SNAKE_HEAD_IMG, (BLOCK_WIDTH, BLOCK_HEIGHT)), direction)
    return SNAKE_HEAD

def draw_window(food, poison, sprint_stamina, snakes, direction):
    WIN.fill(BLACK)
    sprint_bar = pygame.font.SysFont('comicsans', 40).render("Sprint: " + str(sprint_stamina), 1, WHITE)
    WIN.blit(sprint_bar, (10, 10))
    if poison == 1:
        WIN.blit(POISON_FOOD, (food.x, food.y))
    elif poison == 0:
            WIN.blit(FOOD, (food.x, food.y))

    #display snake
    for x in range(len(snakes)):
        for i in range(len(snakes[x])):
            if i == 0:
                WIN.blit(spawn_snake_head(direction[i]), (snakes[x][i].x, snakes[x][i].y))
            elif i > 0:
                WIN.blit(SNAKE_BODY, (snakes[x][i].x, snakes[x][i].y))
    pygame.display.update()

def draw_end_game():
    draw_text = pygame.font.SysFont('comicsans', 40).render("YOU LOST", 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def food_movement(keys_pressed, food, sprint_stamina):
        sprint = 0
        slow_movement = 0
        if keys_pressed[pygame.K_LSHIFT] and not keys_pressed[pygame.K_LCTRL]:
            sprint = VEL//2
        elif keys_pressed[pygame.K_LCTRL] and not keys_pressed[pygame.K_LSHIFT]:
            slow_movement = VEL//2      
        if sprint_stamina == 0:
            sprint = 0

        if keys_pressed[pygame.K_a] and food.x - VEL > 0: # LEFT
            food.x -= VEL + sprint - slow_movement
        if keys_pressed[pygame.K_d] and food.x + VEL + food.width < WIDTH: # RIGHT
            food.x += VEL + sprint - slow_movement
        if keys_pressed[pygame.K_w] and food.y - VEL > 0: # UP
            food.y -= VEL + sprint - slow_movement
        if keys_pressed[pygame.K_s] and food.y + VEL + food.height < HEIGHT: # DOWN
            food.y += VEL + sprint - slow_movement

def snake_ai(snakes, food):
    direction = []
    for i in range(len(snakes)):
        x_diff = food.x - snakes[i][0].x
        y_diff = food.y - snakes[i][0].y

        if abs(x_diff) > abs(y_diff):
            if x_diff >= 0:
                direction.append(270)        
            else:
                direction.append(90)
        else:
            if y_diff >= 0: 
                direction.append(180)
            else:    
                direction.append(0)

    return direction
 
def snake_movement(snakes, direction):
    for x in range(len(snakes)):
        for i in range(len(snakes[x]) - 1, 0, -1):
            snakes[x][i].x = snakes[x][i-1].x
            snakes[x][i].y = snakes[x][i-1].y       
        if direction[x] == 0:
            snakes[x][0].y -= BLOCK_WIDTH
        elif direction[x] == 180:
            snakes[x][0].y += BLOCK_WIDTH    
        elif direction[x] == 90:
            snakes[x][0].x -= BLOCK_WIDTH
        elif direction[x] == 270:
            snakes[x][0].x += BLOCK_WIDTH


def handle_food_snake_collision(food, snakes):
    for x in range(len(snakes)):
        for i in range(len(snakes[x])):
            if i == 0:
                if food.colliderect(snakes[x][i]):
                    pygame.event.post(pygame.event.Event(food_collided_head_event))
            elif i > 0:
                if food.colliderect(snakes[x][i]):
                    diff_x = snakes[x][i].x - food.x
                    diff_y = snakes[x][i].y - food.y
                    print(diff_x, diff_y)
                    if abs(diff_x) > abs(diff_y): # collided horizontally
                        if diff_x >= 0: # collided from left
                            print("left")
                            food.x -= 3
                        else: # collided from right
                            print("right")
                            food.x += 3
                    elif abs(diff_y) > abs(diff_x): # collided vertically
                        if diff_y >= 0:  #collided from top
                            print("top")
                            food.y -= 3
                        else:         #collided from bottom
                            print("bottom")
                            food.y += 3
                    # collided diagnaolly??
            

def create_snakes(number_of_snakes, snake_length):
    snakes = []
    snake_locations_x = [250, 500, 750, 250, 500, 750]
    snake_locations_y = [100, 100, 100, 700, 700, 700]
    for i in range(number_of_snakes):
        #snake_length = random.randit(0,5)
        for i in range(snake_length):
            snakes.append(pygame.Rect(snake_locations_x[i] - BLOCK_WIDTH - (30 * (i+1)), snake_locations_y[i], BLOCK_WIDTH, BLOCK_HEIGHT))



    return snakes

    
def main():
    pygame.init()
    food = pygame.Rect(450 - BLOCK_WIDTH//2, 450 - BLOCK_HEIGHT//2, BLOCK_WIDTH, BLOCK_HEIGHT)
    #snake_head = pygame.Rect(300 - BLOCK_WIDTH, 150, BLOCK_WIDTH, BLOCK_HEIGHT)
    clock = pygame.time.Clock()

    pygame.time.set_timer(regen_stamina_event, REGENERATE_STAMINA)
    pygame.time.set_timer(use_stamina_event, USE_STAMINA)
    pygame.time.set_timer(poison_time_event, POISON_TIME)

    move = 0

    sprint_stamina = STAMINA
    poison = 0

    end_game = 0

    snakes = [[pygame.Rect(300 - BLOCK_WIDTH, 150, BLOCK_WIDTH, BLOCK_HEIGHT), pygame.Rect(300 - BLOCK_WIDTH - 30, 150, BLOCK_WIDTH, BLOCK_HEIGHT), pygame.Rect(300 - BLOCK_WIDTH - 60, 150,         BLOCK_WIDTH, BLOCK_HEIGHT), pygame.Rect(300 - BLOCK_WIDTH - 90, 150, BLOCK_WIDTH, BLOCK_HEIGHT), pygame.Rect(300 - BLOCK_WIDTH - 120, 150, BLOCK_WIDTH, BLOCK_HEIGHT)], [pygame.Rect(600 - BLOCK_WIDTH, 150, BLOCK_WIDTH, BLOCK_HEIGHT), pygame.Rect(600 - BLOCK_WIDTH - 30, 150, BLOCK_WIDTH, BLOCK_HEIGHT), pygame.Rect(600 - BLOCK_WIDTH - 60, 150,         BLOCK_WIDTH, BLOCK_HEIGHT), pygame.Rect(600 - BLOCK_WIDTH - 90, 150, BLOCK_WIDTH, BLOCK_HEIGHT), pygame.Rect(600 - BLOCK_WIDTH - 120, 150, BLOCK_WIDTH, BLOCK_HEIGHT)]]


    run = True
    while run:
        clock.tick(FPS)
        keys_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    poison = 1

            if event.type == regen_stamina_event:
                if sprint_stamina < STAMINA:
                    sprint_stamina += 1

            if keys_pressed[pygame.K_LSHIFT]:
                if event.type == use_stamina_event:
                    if sprint_stamina > 0:
                        sprint_stamina -= 1

            if event.type == poison_time_event:
                if poison:
                    poison = 0

            if event.type == food_collided_head_event:
                end_game = 1

        food_movement(keys_pressed, food, sprint_stamina)

        if move % 40 == 0:
            direction = snake_ai(snakes, food)
            prev_direction = direction
            snake_movement(snakes, direction)

        if end_game == 1:
            draw_end_game()
            break
 
        handle_food_snake_collision(food, snakes)
        draw_window(food, poison, sprint_stamina, snakes, direction)
        move += 1
    main()


if __name__ == "__main__":
    main()