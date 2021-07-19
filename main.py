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
FOOD_BULLET_VEL = 3
STAMINA = 100
FPS = 60
REGENERATE_STAMINA = 1000 #regenerate stamina every second
USE_STAMINA = 20 # drain a percentage of stamina every 20ms == depletes full bar in 2 seconds
POISON_TIME = 3000 # poison booster lasts only 3 seconds

regen_stamina_event = pygame.USEREVENT + 1
use_stamina_event = pygame.USEREVENT + 2
poison_time_event = pygame.USEREVENT + 3
food_collided_head_event = pygame.USEREVENT + 4
activate_poison_event = pygame.USEREVENT + 5
activate_sprint_recharge_event = pygame.USEREVENT + 6
activate_shoot_food_event = pygame.USEREVENT + 7

BLACK = (0,0,0)
WHITE = (255,255,255)


FORTY_FIVE_SECONDS = 500


FOOD_IMG = pygame.image.load(os.path.join('Assets', 'apple.png'))
FOOD = pygame.transform.scale(FOOD_IMG, (BLOCK_WIDTH, BLOCK_HEIGHT))
POISON_FOOD_IMG = pygame.image.load(os.path.join('Assets', 'poison_apple.png'))
POISON_FOOD = pygame.transform.scale(POISON_FOOD_IMG, (BLOCK_WIDTH, BLOCK_HEIGHT))

SNAKE_BODY_IMG = pygame.image.load(os.path.join('Assets', 'snake_body.png'))
SNAKE_BODY = pygame.transform.scale(SNAKE_BODY_IMG, (BLOCK_WIDTH, BLOCK_HEIGHT))
SNAKE_HEAD_IMG = pygame.image.load(os.path.join('Assets', 'snake_head.png'))

SPRINT_PWR_UP_IMG = pygame.image.load(os.path.join('Assets', 'sprint_power_up.png'))
SPRINT_PWR_UP = pygame.transform.scale(SPRINT_PWR_UP_IMG, (BLOCK_WIDTH, BLOCK_HEIGHT))

DROP_POISON_PWR_UP_IMG = pygame.image.load(os.path.join('Assets', 'drop_poison_power_up.png'))
DROP_POISON_PWR_UP = pygame.transform.scale(DROP_POISON_PWR_UP_IMG, (BLOCK_WIDTH, BLOCK_HEIGHT))

POISON_PWR_UP_IMG = pygame.image.load(os.path.join('Assets', 'poison_power_up.png'))
POISON_PWR_UP = pygame.transform.scale(POISON_PWR_UP_IMG, (BLOCK_WIDTH, BLOCK_HEIGHT))

# function to spawn snake head with appropriate image orientation based on movement direction
def spawn_snake_head(direction):
    SNAKE_HEAD = pygame.transform.rotate(pygame.transform.scale(SNAKE_HEAD_IMG, (BLOCK_WIDTH, BLOCK_HEIGHT)), direction)
    return SNAKE_HEAD

def draw_window(food, poison, power_up, power_up_status, food_bullets, sprint_stamina, snakes, direction, time, snakes_killed):
    WIN.fill(BLACK)
    sprint_bar = pygame.font.SysFont('comicsans', 40).render("Sprint: " + str(sprint_stamina), 1, WHITE)
    WIN.blit(sprint_bar, (10, 10))
    time_disp = pygame.font.SysFont('comicsans', 40).render("Time: " + str(time), 1, WHITE)
    WIN.blit(time_disp, (WIDTH - time_disp.get_width() - 10, 10))
    snakes_killed_disp = pygame.font.SysFont('comicsans', 40).render("Snakes Killed: " + str(snakes_killed), 1, WHITE)
    WIN.blit(snakes_killed_disp, (WIDTH - snakes_killed_disp.get_width() - 10, 40))
    if poison == 1:
        WIN.blit(POISON_FOOD, (food.x, food.y))
    elif poison == 0:
            WIN.blit(FOOD, (food.x, food.y))

    if power_up_status[1] == 1:
        if power_up_status[0] == 1:
            WIN.blit(SPRINT_PWR_UP, (power_up.x, power_up.y))
        elif power_up_status[0] == 2:
            WIN.blit(DROP_POISON_PWR_UP, (power_up.x, power_up.y))
        elif power_up_status[0] == 3:
            WIN.blit(POISON_PWR_UP, (power_up.x, power_up.y))

    #display snake
    for x in range(len(snakes)):
        for i in range(len(snakes[x])):
            if i == 0:
                WIN.blit(spawn_snake_head(direction[i]), (snakes[x][i].x, snakes[x][i].y))
            elif i > 0:
                WIN.blit(SNAKE_BODY, (snakes[x][i].x, snakes[x][i].y))

    for bullet in food_bullets:
        pygame.draw.rect(WIN, (255,0,0), bullet)

    pygame.display.update()


def draw_power_up_hud():
    pass
def draw_end_game(end_game, time, snakes_killed):
    if end_game == 1:
        draw_text = pygame.font.SysFont('comicsans', 34).render("YOU LOST, YOU SURVIVED " + str(time) + " SECONDS AND YOU KILLED " + str(snakes_killed) + " SNAKES", 1, WHITE)
        WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    if end_game == 2:
        draw_text = pygame.font.SysFont('comicsans', 34).render("YOU WON, YOU SURVIVED " + str(time) + " SECONDS AND KILLED ALL " + str(snakes_killed) + " SNAKES", 1, WHITE)
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

# handles the movement of the snake head
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

# handles collision of food, snake, and poison objects in window
# returns 1 if snake head collided with poison food or flying food, else 0 
def handle_food_snake_collision(food, snakes, poison, food_bullets):
    del_flag = 0
    del_idx = -2
    for x in range(len(snakes)):
        for i in range(len(snakes[x])):
            if i == 0:
                for j in range(len(food_bullets)):
                    if food_bullets[j].colliderect(snakes[x][i]):
                        del_flag = 1
                        del_idx = x
                        del food_bullets[j]
                if food.colliderect(snakes[x][i]):
                    if poison == 0:
                        pygame.event.post(pygame.event.Event(food_collided_head_event))
                    elif poison == 1:
                        del_flag = 1
                        del_idx = x
            elif i > 0:
                for j in range(len(food_bullets)):
                    if food_bullets[j].colliderect(snakes[x][i]):
                        del food_bullets[j]
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
    if del_flag == 1:
        del snakes[del_idx]
        return 1
    else: 
        return 0
            
# max of 8 snakes
def create_snakes(number_of_snakes, snake_length):
    snakes = []
    for x in range(number_of_snakes):
        snakes.append([])
    snake_locations_x = [250, 500, 750, 250, 500, 750, 250, 750]
    snake_locations_y = [100, 100, 100, 700, 700, 700, 450, 450]
    for j in range(number_of_snakes):
        #snake_length = random.randit(0,5)
        for i in range(snake_length):
            snakes[j].append(pygame.Rect(snake_locations_x[j] - BLOCK_WIDTH - (30 * (i+1)), snake_locations_y[j], BLOCK_WIDTH, BLOCK_HEIGHT))

    return snakes

def handle_food_power_up_collision(food, power_up, power_up_status):
    if power_up_status[1] == 1: # only check if on 
        if food.colliderect(power_up):
            if power_up_status[0] == 1: # sprint
                pygame.event.post(pygame.event.Event(activate_sprint_recharge_event))
            elif power_up_status[0] == 2: # shoot food
                pygame.event.post(pygame.event.Event(activate_shoot_food_event))
            elif power_up_status[0] == 3: # poison
                pygame.event.post(pygame.event.Event(activate_poison_event))
            return 0 # power picked up, so disable it
        else:
            return 1


def handle_bullets(bullet_direction, food_bullets): # handles direction, velocity of bullets and if it goes off screen
    for i in range(len(food_bullets)):
        if bullet_direction == 270: 
            food_bullets[i].x -= FOOD_BULLET_VEL
        if bullet_direction == 90: 
            food_bullets[i].x += FOOD_BULLET_VEL
        if bullet_direction == 0: 
            food_bullets[i].y -= FOOD_BULLET_VEL
        if bullet_direction == 180:     
            food_bullets[i].y += FOOD_BULLET_VEL   



def main():
    pygame.init()
    food = pygame.Rect(450 - BLOCK_WIDTH//2, 450 - BLOCK_HEIGHT//2, BLOCK_WIDTH, BLOCK_HEIGHT)
    power_up = pygame.Rect(30 * random.randint(0, 29), 30 * random.randint(0, 29), BLOCK_WIDTH, BLOCK_HEIGHT)
    clock = pygame.time.Clock()

    pygame.time.set_timer(regen_stamina_event, REGENERATE_STAMINA)
    pygame.time.set_timer(use_stamina_event, USE_STAMINA)

    time_control = 0
    time = 0

    sprint_stamina = STAMINA
    poison = 0

    end_game = 0

    #sprint_activated = 0
    food_bullets = []
    activate_bullet = 0
    bullet_direction = 0

    power_up_status = [-1, -1] #power up type (1-3), power up active or not (0 or 1)
    drop_power_up = random.randint(0, FORTY_FIVE_SECONDS) # 0 to 45 seconds, 750 is adjusted for the framerate (45*60 = 2700)
    number_of_power_ups_dropped = 0

    number_of_snakes = 8
    snake_length = 2
    snakes = create_snakes(number_of_snakes, snake_length)
    snakes_killed = 0
    run = True
    while run:
        clock.tick(FPS)
        keys_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == activate_poison_event:
                poison = 1
                pygame.time.set_timer(poison_time_event, POISON_TIME, True) # set timer 

            if event.type == activate_sprint_recharge_event:
                sprint_stamina = STAMINA

            if event.type == activate_shoot_food_event:
                activate_bullet = 1
            if event.type == pygame.KEYDOWN and activate_bullet == 1:
                if event.key == pygame.K_SPACE:
                   bullet = pygame.Rect(food.x + food.width//2, food.y + food.height//2, 10, 5)
                   food_bullets.append(bullet)
                   activate_bullet = 0
                if keys_pressed[pygame.K_a]: 
                    bullet_direction = 270
                elif keys_pressed[pygame.K_d]: 
                    bullet_direction = 90
                elif keys_pressed[pygame.K_w]: 
                    bullet_direction = 0
                elif keys_pressed[pygame.K_s]:     
                    bullet_direction = 180

            if event.type == regen_stamina_event:
                if sprint_stamina < STAMINA:
                    sprint_stamina += 1

            if keys_pressed[pygame.K_LSHIFT]:
                if event.type == use_stamina_event:
                    if sprint_stamina > 0:
                        sprint_stamina -= 1

            if event.type == poison_time_event:
                if poison == 1:
                    poison = 0

            if event.type == food_collided_head_event:
                end_game = 1

        food_movement(keys_pressed, food, sprint_stamina)
        # generate random location for power up spawn at a random time within intervals of 45 seconds
        if time_control > drop_power_up + number_of_power_ups_dropped*FORTY_FIVE_SECONDS:
            power_up = pygame.Rect(30 * random.randint(0, 29), 30 * random.randint(0, 29), BLOCK_WIDTH, BLOCK_HEIGHT)
            power_up_status[0] = random.randint(1, 3)
            power_up_status[1] = 1 # can only be turned back to zero if food collides with power_up in another function
            drop_power_up = random.randint(0, FORTY_FIVE_SECONDS)
            number_of_power_ups_dropped += 1

        power_up_status[1] = handle_food_power_up_collision(food, power_up, power_up_status)

        if time_control % 40 == 0: # controls how fast the snake can move
            direction = snake_ai(snakes, food)
            prev_direction = direction
            #snake_movement(snakes, direction)

        if time_control % 60 == 0: # add score every second
            time += 1

        snakes_killed += handle_food_snake_collision(food, snakes, poison, food_bullets)
        if snakes_killed == number_of_snakes:
            end_game = 2


        if end_game != 0:
            draw_end_game(end_game, time, snakes_killed)
            break

        handle_bullets(bullet_direction, food_bullets)
        draw_window(food, poison, power_up, power_up_status, food_bullets, sprint_stamina, snakes, direction, time, snakes_killed)
        draw_power_up_hud()
        time_control += 1
    main()


if __name__ == "__main__":
    main()