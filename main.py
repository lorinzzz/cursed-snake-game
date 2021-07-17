# implementation notes:
# multiple snakes (upwards of 8, user can choose how many to spawn in)
# user can choose what food he is 
# the food can be moved diagonally, while the snakes move like they originally do
# snakes, however cannot be killed by colliding with themselves or other snakes
# the user (food) can be powered up by becoming poison, and thus can kill the snakes by running into them. this will be the only way for a snake to die
# and as usual, the food can only be eaten by the snake's head
# drip poison powerup !?!
# sprint/slow movement function for apple!
# sprint powerup?

import pygame
import os

WIDTH, HEIGHT = 900, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cursed Snake Game")

BLOCK_WIDTH, BLOCK_HEIGHT = 25, 25

VEL = 2
STAMINA = 100
FPS = 60
REGENERATE_STAMINA = 1000 #regenerate stamina every second
USE_STAMINA = 20 # drain a percentage of stamina every 20ms == depletes full bar in 2 seconds
POISON_TIME = 5000 # poison booster lasts only 5 seconds

regen_stamina_event = pygame.USEREVENT + 1
use_stamina_event = pygame.USEREVENT + 2
poison_time_event = pygame.USEREVENT + 3


BLACK = (0,0,0)
WHITE = (255,255,255)

FOOD_IMG = pygame.image.load(os.path.join('Assets', 'apple.png'))
FOOD = pygame.transform.scale(FOOD_IMG, (BLOCK_WIDTH, BLOCK_HEIGHT))
POISON_FOOD_IMG = pygame.image.load(os.path.join('Assets', 'poison_apple.png'))
POISON_FOOD = pygame.transform.scale(POISON_FOOD_IMG, (BLOCK_WIDTH, BLOCK_HEIGHT))

SNAKE_BODY_IMG = pygame.image.load(os.path.join('Assets', 'snake_body.png'))
SNAKE_BODY = pygame.transform.scale(SNAKE_BODY_IMG, (BLOCK_WIDTH, BLOCK_HEIGHT))
SNAKE_HEAD_IMG = pygame.image.load(os.path.join('Assets', 'snake_head.png'))


# function to rotate snake head based on its movement direction
def rot_head(direction = 0):
    SNAKE_HEAD = pygame.transform.scale(SNAKE_HEAD_IMG, (BLOCK_WIDTH, BLOCK_HEIGHT), direction)

def draw_window(food, poison, sprint_stamina):
    WIN.fill(BLACK)
    sprint_bar = pygame.font.SysFont('comicsans', 40).render("Sprint: " + str(sprint_stamina), 1, WHITE)
    WIN.blit(sprint_bar, (10, 10))
    if poison == 1:
        WIN.blit(POISON_FOOD, (food.x, food.y))
    elif poison == 0:
        WIN.blit(FOOD, (food.x, food.y))
    pygame.display.update()

def food_movement(keys_pressed, food, sprint_stamina):
        sprint = 0
        slow_movement = 0
        if keys_pressed[pygame.K_LSHIFT] and not keys_pressed[pygame.K_LALT]:
            sprint = VEL//2
        elif keys_pressed[pygame.K_LALT] and not keys_pressed[pygame.K_LSHIFT]:
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

 
def main():
    pygame.init()
    food = pygame.Rect(350, 250 - BLOCK_HEIGHT//2, BLOCK_WIDTH, BLOCK_HEIGHT)
    clock = pygame.time.Clock()

    pygame.time.set_timer(regen_stamina_event, REGENERATE_STAMINA)
    pygame.time.set_timer(use_stamina_event, USE_STAMINA)
    pygame.time.set_timer(poison_time_event, POISON_TIME)

    sprint_stamina = STAMINA
    poison = 0

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

        food_movement(keys_pressed, food, sprint_stamina)


        draw_window(food, poison, sprint_stamina)
    main()


if __name__ == "__main__":
    main()