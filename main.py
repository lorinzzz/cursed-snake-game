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

def draw_window(food, poison, sprint_stamina, snake_head, snake_body, direction):
    WIN.fill(BLACK)
    sprint_bar = pygame.font.SysFont('comicsans', 40).render("Sprint: " + str(sprint_stamina), 1, WHITE)
    WIN.blit(sprint_bar, (10, 10))
    if poison == 1:
        WIN.blit(POISON_FOOD, (food.x, food.y))
    elif poison == 0:
            WIN.blit(FOOD, (food.x, food.y))

    #display snake
    WIN.blit(spawn_snake_head(direction), (snake_head.x, snake_head.y))
    for i in range(len(snake_body)):
        WIN.blit(SNAKE_BODY, (snake_body[i].x, snake_body[i].y))
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

def snake_ai(snake_head, food):
    x_diff = food.x - snake_head.x
    y_diff = food.y - snake_head.y

    if abs(x_diff) > abs(y_diff):
        if x_diff >= 0:
            direction = 270         
        else:
            direction = 90
    else:
        if y_diff >= 0: 
            direction = 180
        else:    
            direction = 0

    return direction
 
def snake_movement(snake_head, snake_body, direction):
    for i in range(len(snake_body) - 1, 0, -1):
        snake_body[i].x = snake_body[i-1].x
        snake_body[i].y = snake_body[i-1].y
    snake_body[0].x = snake_head.x
    snake_body[0].y = snake_head.y        
    if direction == 0:
        snake_head.y -= BLOCK_WIDTH
    elif direction == 180:
        snake_head.y += BLOCK_WIDTH    
    elif direction == 90:
        snake_head.x -= BLOCK_WIDTH
    elif direction == 270:
        snake_head.x += BLOCK_WIDTH


def handle_food_snake_collision(food, snake_head, snake_body):
    if food.colliderect(snake_head):
        pygame.event.post(pygame.event.Event(food_collided_head_event))


            



    
def main():
    pygame.init()
    food = pygame.Rect(450 - BLOCK_WIDTH//2, 450 - BLOCK_HEIGHT//2, BLOCK_WIDTH, BLOCK_HEIGHT)
    snake_head = pygame.Rect(300 - BLOCK_WIDTH, 150, BLOCK_WIDTH, BLOCK_HEIGHT)
    clock = pygame.time.Clock()

    pygame.time.set_timer(regen_stamina_event, REGENERATE_STAMINA)
    pygame.time.set_timer(use_stamina_event, USE_STAMINA)
    pygame.time.set_timer(poison_time_event, POISON_TIME)

    move = 0

    sprint_stamina = STAMINA
    poison = 0

    end_game = 0

    #x = [300 - BLOCK_WIDTH - 30, 300 - BLOCK_WIDTH - 60, 300 - BLOCK_WIDTH - 90, 300 - BLOCK_WIDTH - 120, 300 - BLOCK_WIDTH - 150]
    #y= [150, 150, 150, 150, 150]
    snake_body = [pygame.Rect(300 - BLOCK_WIDTH - 30, 150, BLOCK_WIDTH, BLOCK_HEIGHT), pygame.Rect(300 - BLOCK_WIDTH - 60, 150, BLOCK_WIDTH, BLOCK_HEIGHT),
                    pygame.Rect(300 - BLOCK_WIDTH - 90, 150, BLOCK_WIDTH, BLOCK_HEIGHT), pygame.Rect(300 - BLOCK_WIDTH - 120, 150, BLOCK_WIDTH, BLOCK_HEIGHT)]
    #snake_body.append(x)
    #snake_body.append(y)


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
            direction = snake_ai(snake_head, food)
            prev_direction = direction
            snake_movement(snake_head, snake_body, direction)

        if end_game == 1:
            draw_end_game()
            break
 
        handle_food_snake_collision(food, snake_head, snake_body)
        draw_window(food, poison, sprint_stamina, snake_head, snake_body, direction)
        move += 1
    main()


if __name__ == "__main__":
    main()