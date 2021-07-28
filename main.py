# implementation notes:
# multiple snakes (upwards of 8, user can choose how many to spawn in)
# user can choose what food he is 
# the food can be moved diagonally, while the snakes move like they originally do ## DONE##
# snakes, however cannot be killed by colliding with themselves or other snakes 
# the user (food) can be powered up by becoming poison, and thus can kill the snakes by running into them. this will be the only way for a snake to die ## DONE##
# and as usual, the food can only be eaten by the snake's head ## DONE##
# food can collide with snake body, and cannot be moved past it, but will not die ## DONE##
# drip poison powerup !?! ## DONE##
# sprint/slow movement function for apple! ## DONE##
# sprint powerup? ## DONE##
# perhaps implement ability to respawn a snake after it is dead 
# intelligent AI from snakes that will work together dynamically, game plan of snakes changes depending on how many

import pygame
import os
import random
import pygame_constants
pygame.font.init()
pygame.mixer.init()
from pygame.event import get
from snake_ai import SnakeAI


### global variables ###
snake_speed = 25
number_of_snakes = 8
food_name = "Apple"
speed_string = "normal"
### end global variables ###


WIDTH, HEIGHT = pygame_constants.WIDTH, pygame_constants.HEIGHT
ACTUAL_WINDOW_WIDTH = WIDTH + 280
BLOCK_WIDTH, BLOCK_HEIGHT = pygame_constants.BLOCK_WIDTH, pygame_constants.BLOCK_HEIGHT
FPS = pygame_constants.FPS
VEL = 2
FOOD_BULLET_VEL = 4
STAMINA = 100
REGENERATE_STAMINA = 1000 #regenerate stamina every second
USE_STAMINA = 20 # drain a percentage of stamina every 20ms == depletes full bar in 2 seconds
POISON_DURATION = 5000 # only get 5seconds to use the poison
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (112,128,144)
SILVER = (192,192,192)
RED = (255,0,0)
GREEN = (0,100,0)
SPAWN_POWER_UP_INTERVAL = 1800 # 2700/60 = 45 1800/60 = 30 seconds
POWER_UP_TIME = 10000 # powers ups are only active for 10 seconds 
MAX_SNAKES = 8

pygame.init()
WIN = pygame.display.set_mode((ACTUAL_WINDOW_WIDTH, HEIGHT))
pygame.display.set_caption("Cursed Snake Game")

FOOD_DEATH_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'food_death.mp3'))
SHOOT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'shoot.mp3'))
SNAKE_DEATH_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'snake_death.mp3'))
POISON_POWER_UP_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'poison_power_up.mp3'))
SHOOT_POWER_UP_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'shoot_power_up.mp3'))
SPRINT_POWER_UP_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'sprint_power_up.mp3'))


regen_stamina_event = pygame.USEREVENT + 1
use_stamina_event = pygame.USEREVENT + 2
poison_used_event = pygame.USEREVENT + 3
food_collided_head_event = pygame.USEREVENT + 4
activate_poison_event = pygame.USEREVENT + 5
activate_sprint_recharge_event = pygame.USEREVENT + 6
activate_shoot_food_event = pygame.USEREVENT + 7
disable_power_up_event = pygame.USEREVENT + 8

## global pygame var ##
POISON_FOOD_IMG = pygame.image.load(os.path.join('Assets', 'poison_apple.png'))
FOOD_IMG = pygame.image.load(os.path.join('Assets', 'apple.png'))
FOOD = pygame.transform.scale(FOOD_IMG, (BLOCK_WIDTH, BLOCK_HEIGHT))
POISON_FOOD = pygame.transform.scale(POISON_FOOD_IMG, (BLOCK_WIDTH, BLOCK_HEIGHT))
## end global pygame var ##

SNAKE_BODY_IMG = pygame.image.load(os.path.join('Assets', 'snake_body.png'))
SNAKE_BODY = pygame.transform.scale(SNAKE_BODY_IMG, (BLOCK_WIDTH, BLOCK_HEIGHT))
SNAKE_HEAD_IMG = pygame.image.load(os.path.join('Assets', 'snake_head.png'))

SPRINT_PWR_UP_IMG = pygame.image.load(os.path.join('Assets', 'sprint_power_up.png'))
SPRINT_PWR_UP = pygame.transform.scale(SPRINT_PWR_UP_IMG, (BLOCK_WIDTH, BLOCK_HEIGHT))

DROP_POISON_PWR_UP_IMG = pygame.image.load(os.path.join('Assets', 'shoot_food_power_up.png'))
DROP_POISON_PWR_UP = pygame.transform.scale(DROP_POISON_PWR_UP_IMG, (BLOCK_WIDTH, BLOCK_HEIGHT))

POISON_PWR_UP_IMG = pygame.image.load(os.path.join('Assets', 'poison_power_up.png'))
POISON_PWR_UP = pygame.transform.scale(POISON_PWR_UP_IMG, (BLOCK_WIDTH, BLOCK_HEIGHT))

BORDER = pygame.Rect(WIDTH, 0, 2, HEIGHT)

SNAKE_GRAVE_BORDER = pygame.Rect(WIDTH, 440, 280, 2)

MAIN_MENU_BUTTON = pygame.Rect(WIDTH + 50, 200, 200, 50)
RESET_BUTTON = pygame.Rect(WIDTH + 50, 275, 200, 50)
QUIT_BUTTON = pygame.Rect(WIDTH + 50, 350, 200, 50)


# start button for main menu 
START_GAME_BUTTON = pygame.Rect(WIDTH//2, HEIGHT//2 - 30, 250, 70)
# snake count options
FOUR_SNAKES = pygame.Rect( 400,  HEIGHT//2 + 390, 50, 50)
FIVE_SNAKES = pygame.Rect( 500,  HEIGHT//2 + 390, 50, 50)
SIX_SNAKES = pygame.Rect( 600,  HEIGHT//2 + 390, 50, 50)
SEVEN_SNAKES = pygame.Rect( 700,  HEIGHT//2 + 390, 50, 50)
EIGHT_SNAKES = pygame.Rect( 800,  HEIGHT//2 + 390, 50, 50)
# # snake speed options
FAST_SPEED = pygame.Rect( 250,  HEIGHT//2 + 290, 150, 50)
NORMAL_SPEED = pygame.Rect( 450,  HEIGHT//2 + 290, 150, 50)
SLOW_SPEED = pygame.Rect( 650,  HEIGHT//2 + 290, 150, 50)
# snake food options
TACO_OPTION = pygame.Rect( 250,  HEIGHT//2 + 190, 150, 50)
BURGER_OPTION = pygame.Rect( 450, HEIGHT//2 + 190, 150,  50)
APPLE_OPTION = pygame.Rect( 650, HEIGHT//2 + 190,  150,  50)


# function to spawn snake head with appropriate image orientation based on movement direction
def spawn_snake_head(direction):
    #pygame has these flipped
    if direction == 270:
        direction = 90
    elif direction == 90:
        direction = 270
    SNAKE_HEAD = pygame.transform.rotate(pygame.transform.scale(SNAKE_HEAD_IMG, (BLOCK_WIDTH, BLOCK_HEIGHT)), direction)
    return SNAKE_HEAD

def draw_window(food, poison, power_up, power_up_status, food_bullets, sprint_stamina, snakes, direction, time, snakes_killed):
    WIN.fill(BLACK)
    pygame.draw.rect(WIN, WHITE, BORDER)
    pygame.draw.rect(WIN, WHITE, SNAKE_GRAVE_BORDER)
    sprint = pygame.font.SysFont('comicsans', 35).render("Sprint:", 1, WHITE)
    sprint_value = pygame.font.SysFont('comicsans', 40).render(str(sprint_stamina), 1, RED)
    WIN.blit(sprint, (WIDTH + 80, 110))
    WIN.blit(sprint_value, (WIDTH + 170, 110))
    time_disp = pygame.font.SysFont('comicsans', 60).render("Time: " + str(time), 1, WHITE)
    WIN.blit(time_disp, (WIDTH + 65, 15))
    snakes_killed_disp = pygame.font.SysFont('comicsans', 35).render("Snakes Killed: " + str(snakes_killed), 1, WHITE)
    WIN.blit(snakes_killed_disp, (WIDTH + 55, 450))
    if poison == 1:
        WIN.blit(POISON_FOOD, (food.x, food.y))
    elif poison == 0:
            WIN.blit(FOOD, (food.x, food.y))

    # display power up pickups
    if power_up_status[1] == 1:
        if power_up_status[0] == 1:
            WIN.blit(SPRINT_PWR_UP, (power_up.x, power_up.y))
        elif power_up_status[0] == 2:
            WIN.blit(DROP_POISON_PWR_UP, (power_up.x, power_up.y))
        elif power_up_status[0] == 3:
            WIN.blit(POISON_PWR_UP, (power_up.x, power_up.y))

    #display snake body
    for x in range(len(snakes)):
        for i in range(len(snakes[x])):
            if i == 0:
                WIN.blit(spawn_snake_head(direction[i]), (snakes[x][i].x, snakes[x][i].y))
            if i > 0:
                WIN.blit(SNAKE_BODY, (snakes[x][i].x, snakes[x][i].y))
    # display projectiles from using the shoot power up
    for bullet in food_bullets:
        pygame.draw.rect(WIN, (255,0,0), bullet)

    reset = pygame.font.SysFont('comicsans', 40).render("Reset", 1, BLACK)
    main_menu = pygame.font.SysFont('comicsans', 40).render("Main Menu", 1, BLACK)
    quit = pygame.font.SysFont('comicsans', 40).render("Exit", 1, BLACK)

    mx, my = pygame.mouse.get_pos()
    pygame.draw.rect(WIN, WHITE, MAIN_MENU_BUTTON)
    pygame.draw.rect(WIN, WHITE, RESET_BUTTON)
    pygame.draw.rect(WIN, WHITE, QUIT_BUTTON)
    if MAIN_MENU_BUTTON.collidepoint((mx,my)):
        pygame.draw.rect(WIN, GREY, MAIN_MENU_BUTTON)
        if pygame.mouse.get_pressed()[0] == 1:
            pygame.draw.rect(WIN, SILVER, MAIN_MENU_BUTTON)
            main(reset = 0)
    if RESET_BUTTON.collidepoint((mx,my)):
        pygame.draw.rect(WIN, GREY, RESET_BUTTON)
        if pygame.mouse.get_pressed()[0] == 1:
            pygame.draw.rect(WIN, SILVER, RESET_BUTTON)
            main(reset = 1)
    if QUIT_BUTTON.collidepoint((mx,my)):
        pygame.draw.rect(WIN, GREY, QUIT_BUTTON)
        if pygame.mouse.get_pressed()[0] == 1:
            pygame.draw.rect(WIN, SILVER, QUIT_BUTTON)
            quit()        
    WIN.blit(main_menu, (980, 215))
    WIN.blit(reset, (1010, 290))
    WIN.blit(quit, (1020, 365))
    pygame.display.update()

def draw_end_game(end_game, time, snakes_killed):
    if end_game == 1:
        draw_text = pygame.font.SysFont('comicsans', 38).render("YOU LOST, YOU SURVIVED " + str(time) + " SECONDS AND KILLED " + str(snakes_killed) + " SNAKES", 1, WHITE)
        WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    if end_game == 2:
        draw_text = pygame.font.SysFont('comicsans', 38).render("YOU WON, YOU SURVIVED " + str(time) + " SECONDS AND KILLED ALL " + str(snakes_killed) + " SNAKES", 1, WHITE)
        WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

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
# make sure none of these movements result in a snake going out of bounds, or running into itself 
# maybe consider if snakes collide, their movement speeds are slowed? 
# would be much easier to code rather than checking if every move will result in a collision with antother snake and having to figure out another move
# not coding for snake vs another snake collision is much easier
# check if snake does not collide itself ORRRR
# snake cannot make full 180 degree turns but can be allowed to have at MAX one collision 
#def snake_ai(snakes, food):
#    return ai.execute_ai(snakes,food)
 
def snake_movement(snakes, direction, ignore_list):
    for x in range(len(snakes)):
        if x not in ignore_list:
            for i in range(len(snakes[x]) - 1, 0, -1):
                snakes[x][i].x = snakes[x][i-1].x
                snakes[x][i].y = snakes[x][i-1].y       
            if direction[x] == 0:
                snakes[x][0].y -= BLOCK_WIDTH
            elif direction[x] == 180:
                snakes[x][0].y += BLOCK_WIDTH    
            elif direction[x] == 270:
                snakes[x][0].x -= BLOCK_WIDTH
            elif direction[x] == 90:
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
                        FOOD_DEATH_SOUND.play()
                        pygame.event.post(pygame.event.Event(food_collided_head_event))
                    elif poison == 1:
                        del_flag = 1
                        del_idx = x
                        pygame.event.post(pygame.event.Event(poison_used_event))
            elif i > 0:
                for j in range(len(food_bullets)):
                    if food_bullets[j].colliderect(snakes[x][i]):
                        del food_bullets[j]
                if food.colliderect(snakes[x][i]):
                    if poison == 1:
                        pygame.event.post(pygame.event.Event(poison_used_event)) # take away poison if collided with body
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
        SNAKE_DEATH_SOUND.play()
        return del_idx
    else: 
        return -1

def update_ignore_list(del_idx, ignore_list):
    ignore_list.append(del_idx)

def to_graveyard(snakes, del_idx, snakes_killed):
    for i in range(len(snakes[del_idx])):
        snakes[del_idx][i].x = WIDTH + (35 * snakes_killed)
        snakes[del_idx][i].y = 500 + i*30

# max of 8 snakes, maybe?
def create_snakes(number_of_snakes):
    snakes = []
    snake_locations_x = []
    snake_locations_y = []

    # for later on when randomizing snake lengths 
    # note: need to do this in main and pass it in!
    random_snake_lengths = [] 

    x_coord, y_coord = 0, 0
    for x in range(number_of_snakes):
        snakes.append([])
        random_snake_lengths.append(random.randint(2,15))
    
    print("Snake lengths: ", random_snake_lengths)
    for k in range(MAX_SNAKES):
       #generate random coordinate to spawn snakehead in each coord
        if k == 0: # octant 1 
            x_coord = 30 * random.randint(1, 9) # [30,270]
            y_coord = 30 * random.randint(0, 9) # [0,270]
        elif k == 1: # octant 2
            x_coord = 30 * random.randint(10, 20) # [300,600]
            y_coord = 30 * random.randint(0, 9) # [0,270]           
        elif k == 2: # octant 3
            x_coord = 30 * random.randint(21, 29) # [630,870]
            y_coord = 30 * random.randint(0, 9) # [0,270]              
        elif k == 3: # octant 4
            x_coord = 30 * random.randint(21, 29) # [630,870]
            y_coord = 30 * random.randint(10, 20) # [300,600]             
        elif k == 4: # octant 5
            x_coord = 30 * random.randint(21, 29) # [630,870]
            y_coord = 30 * random.randint(21, 29) # [630,870]             
        elif k == 5: # octant 6
            x_coord = 30 * random.randint(10, 20) # [300,600]     
            y_coord = 30 * random.randint(21, 29) # [630,870]             
        elif k == 6: # octant 7
            x_coord = 30 * random.randint(1, 9) # [30,270]    
            y_coord = 30 * random.randint(21, 29) # [630,870]             
        elif k == 7: # octant 8
            x_coord = 30 * random.randint(1, 9) # [30,270]    
            y_coord = 30 * random.randint(10, 20) # [300,600]               
        snake_locations_x.append(x_coord)
        snake_locations_y.append(y_coord)   
    
    # shuffle x and y coord lists so in case we have less than 8 snakes, they can spawn at random octants
    # Using zip() + shuffle() + * operator to maintain list order consistency between the two
    temp = list(zip(snake_locations_x, snake_locations_y))
    random.shuffle(temp)
    snake_locations_x, snake_locations_y = zip(*temp)

    # snakes can spawn over other snakes, and their body can be out of screen
    # but their heads will always be inthe window
    for j in range(number_of_snakes):
        # get a random direction for orientation of body 
        body_spawn_direction = random.randint(1,4) # 1 = top, 2 = bottom, 3 = left, 4 = right
        print("snake " + str(j) + " spawned " + str(body_spawn_direction))
        for i in range(0, random_snake_lengths[j]):
            if body_spawn_direction == 1:
                snakes[j].append(pygame.Rect(snake_locations_x[j] - BLOCK_WIDTH - (30 * i), snake_locations_y[j], BLOCK_WIDTH, BLOCK_HEIGHT)) #note: this spawns them horizontally and to the left of the head
            if body_spawn_direction == 2:
                snakes[j].append(pygame.Rect(snake_locations_x[j] - BLOCK_WIDTH + (30 * i), snake_locations_y[j], BLOCK_WIDTH, BLOCK_HEIGHT)) # spawns to right
            if body_spawn_direction == 3:  
                snakes[j].append(pygame.Rect(snake_locations_x[j] - BLOCK_WIDTH, snake_locations_y[j] + (30 * i), BLOCK_WIDTH, BLOCK_HEIGHT)) # spawns to bottom  
            if body_spawn_direction == 4:    
                snakes[j].append(pygame.Rect(snake_locations_x[j] - BLOCK_WIDTH, snake_locations_y[j] - (30 * i), BLOCK_WIDTH, BLOCK_HEIGHT)) # spawns to top

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
            return 0 # power up picked up, so disable it
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
        if food_bullets[i].x > WIDTH or food_bullets[i].x < 0 or food_bullets[i].y > HEIGHT or food_bullets[i].y < 0:
            del food_bullets[i]
        
def get_bullet_direction(keys_pressed):
    if keys_pressed[pygame.K_a]: 
        bullet_direction = 270
    elif keys_pressed[pygame.K_d]: 
        bullet_direction = 90
    elif keys_pressed[pygame.K_w]: 
        bullet_direction = 0
    elif keys_pressed[pygame.K_s]:     
        bullet_direction = 180  
    else:
        bullet_direction = random.choice([0,90,180,270])  
    return bullet_direction

# player can customize snake speed, number of snakes, whether to have all snakes the same length, or to randomize the snake lengths
# when randomizing snake lengths, perhaps have an interval of lenghts to randomize from or no constraints
# In the future maybe add ability for snakes to respawn and have it toggleable 

def game(snake_speed, number_of_snakes):
    snake_ai = SnakeAI()
    
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

    food_bullets = []
    activate_bullet = 0
    bullet_direction = 0

    power_up_status = [-1, -1] #power up type (1-3), power up active or not (0 or 1)
    drop_power_up = random.randint(0, 1200) # 0 to 45 seconds, 750 is adjusted for the framerate (45*60 = 2700)
    number_of_power_ups_dropped = 0

    snakes = create_snakes(number_of_snakes)
    snakes_killed = 0

    ignore_list = []

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
                pygame.time.set_timer(poison_used_event, POISON_DURATION)
                POISON_POWER_UP_SOUND.play()

            if event.type == activate_sprint_recharge_event:
                sprint_stamina = STAMINA * 2 # get double staminas
                SPRINT_POWER_UP_SOUND.play()

            if event.type == activate_shoot_food_event:
                activate_bullet = 1
                SHOOT_POWER_UP_SOUND.play()
            if event.type == pygame.KEYDOWN and activate_bullet == 1:
                if event.key == pygame.K_SPACE:
                   bullet = pygame.Rect(food.x + food.width//2, food.y + food.height//2, 5, 5)
                   food_bullets.append(bullet)
                   activate_bullet = 0
                   bullet_direction = get_bullet_direction(keys_pressed)
                   SHOOT_SOUND.play()

            if event.type == regen_stamina_event:
                if sprint_stamina < STAMINA:
                    sprint_stamina += 1

            if keys_pressed[pygame.K_LSHIFT]:
                if event.type == use_stamina_event:
                    if sprint_stamina > 0:
                        sprint_stamina -= 1

            if event.type == poison_used_event:
                pygame.time.set_timer(poison_used_event, 0)
                if poison == 1:
                    poison = 0

            if event.type == food_collided_head_event:
                end_game = 1

            if event.type == disable_power_up_event:
                if power_up_status[1] == 1:
                    power_up_status[1] = 0
                    print("power-up disabled!")
            
        food_movement(keys_pressed, food, sprint_stamina)
        # generate random location for power up spawn at a random time within intervals of n seconds
        if time_control > drop_power_up + number_of_power_ups_dropped*SPAWN_POWER_UP_INTERVAL:
            #pygame.time.set_timer(disable_power_up_event, 0) # disable timer
            power_up = pygame.Rect(30 * random.randint(0, 29), 30 * random.randint(0, 29), BLOCK_WIDTH, BLOCK_HEIGHT)
            power_up_status[0] = random.randint(1, 3)
            power_up_status[1] = 1 # can only be turned back to zero if food collides with power_up in another function
            drop_power_up = random.randint(0, 1200)
            number_of_power_ups_dropped += 1
            pygame.time.set_timer(disable_power_up_event, POWER_UP_TIME) # set timer
        power_up_status[1] = handle_food_power_up_collision(food, power_up, power_up_status)

        if time_control % snake_speed == 0: # controls how fast the snake can move
            direction = snake_ai.execute_ai(snakes,food, ignore_list) # returns a list of directions for snakes
            snake_movement(snakes, direction, ignore_list)

        if time_control % 60 == 0: # add score every second
            time += 1

        del_idx = handle_food_snake_collision(food, snakes, poison, food_bullets)
        if del_idx != -1:
            snakes_killed += 1
            update_ignore_list(del_idx, ignore_list)
            to_graveyard(snakes, del_idx, snakes_killed)
        if snakes_killed == number_of_snakes:
            end_game = 2

        if end_game != 0:
            draw_end_game(end_game, time, snakes_killed)
            break

        handle_bullets(bullet_direction, food_bullets)
        draw_window(food, poison, power_up, power_up_status, food_bullets, sprint_stamina, snakes, direction, time, snakes_killed)
        time_control += 1
    game(snake_speed, number_of_snakes)

def draw_main_menu():
    global snake_speed
    global number_of_snakes
    global FOOD_IMG
    global POISON_FOOD_IMG
    global FOOD
    global POISON_FOOD
    WIN.fill(GREEN)
    
    global food_name
    global speed_string
    
    pygame.draw.rect(WIN, RED, START_GAME_BUTTON)
    pygame.draw.rect(WIN, WHITE, TACO_OPTION)
    pygame.draw.rect(WIN, WHITE, BURGER_OPTION)
    pygame.draw.rect(WIN, WHITE, APPLE_OPTION)
    
    pygame.draw.rect(WIN, WHITE, FAST_SPEED)
    pygame.draw.rect(WIN, WHITE, NORMAL_SPEED)
    pygame.draw.rect(WIN, WHITE, SLOW_SPEED)   
    
    pygame.draw.rect(WIN, WHITE, FOUR_SNAKES)
    pygame.draw.rect(WIN, WHITE, FIVE_SNAKES)
    pygame.draw.rect(WIN, WHITE, SIX_SNAKES)
    pygame.draw.rect(WIN, WHITE, SEVEN_SNAKES)
    pygame.draw.rect(WIN, WHITE, EIGHT_SNAKES)
  
    mx, my = pygame.mouse.get_pos()
    if START_GAME_BUTTON.collidepoint((mx,my)):
        pygame.draw.rect(WIN, WHITE, START_GAME_BUTTON)
        if pygame.mouse.get_pressed()[0] == 1:
            pygame.draw.rect(WIN, RED, START_GAME_BUTTON)
            FOOD = pygame.transform.scale(FOOD_IMG, (BLOCK_WIDTH, BLOCK_HEIGHT))
            POISON_FOOD = pygame.transform.scale(POISON_FOOD_IMG, (BLOCK_WIDTH, BLOCK_HEIGHT))
            game(snake_speed, number_of_snakes)
            
    if TACO_OPTION.collidepoint((mx,my)):
        pygame.draw.rect(WIN, GREY, TACO_OPTION)
        if pygame.mouse.get_pressed()[0] == 1:
            pygame.draw.rect(WIN, SILVER, TACO_OPTION)
            POISON_FOOD_IMG = pygame.image.load(os.path.join('Assets', 'poison_taco.png'))
            FOOD_IMG = pygame.image.load(os.path.join('Assets', 'taco.png'))
            food_name = "Taco"
    if BURGER_OPTION.collidepoint((mx,my)):
        pygame.draw.rect(WIN, GREY, BURGER_OPTION)
        if pygame.mouse.get_pressed()[0] == 1:
            pygame.draw.rect(WIN, SILVER, BURGER_OPTION)
            POISON_FOOD_IMG = pygame.image.load(os.path.join('Assets', 'poison_burger.png'))
            FOOD_IMG = pygame.image.load(os.path.join('Assets', 'burger.png')) 
            food_name = "Burger"
    if APPLE_OPTION.collidepoint((mx,my)):
        pygame.draw.rect(WIN, GREY, APPLE_OPTION)
        if pygame.mouse.get_pressed()[0] == 1:
            pygame.draw.rect(WIN, SILVER, APPLE_OPTION)
            POISON_FOOD_IMG = pygame.image.load(os.path.join('Assets', 'poison_apple.png'))
            FOOD_IMG = pygame.image.load(os.path.join('Assets', 'apple.png')) 
            food_name = "Apple"
    if FAST_SPEED.collidepoint((mx,my)):
        pygame.draw.rect(WIN, GREY, FAST_SPEED)
        if pygame.mouse.get_pressed()[0] == 1:
            pygame.draw.rect(WIN, SILVER, FAST_SPEED)
            snake_speed = 15
            speed_string = "fast"
    if NORMAL_SPEED.collidepoint((mx,my)):
        pygame.draw.rect(WIN, GREY, NORMAL_SPEED)
        if pygame.mouse.get_pressed()[0] == 1:
            pygame.draw.rect(WIN, SILVER, NORMAL_SPEED)
            snake_speed = 20 
            speed_string = "normal"                        
    if SLOW_SPEED.collidepoint((mx,my)):
        pygame.draw.rect(WIN, GREY, SLOW_SPEED)
        if pygame.mouse.get_pressed()[0] == 1:
            pygame.draw.rect(WIN, SILVER, SLOW_SPEED)
            snake_speed = 30
            speed_string = "slow"

    if FOUR_SNAKES.collidepoint((mx,my)):
        pygame.draw.rect(WIN, GREY, FOUR_SNAKES)
        if pygame.mouse.get_pressed()[0] == 1:
            pygame.draw.rect(WIN, SILVER, FOUR_SNAKES)
            number_of_snakes = 4
    if FIVE_SNAKES.collidepoint((mx,my)):
        pygame.draw.rect(WIN, GREY, FIVE_SNAKES)
        if pygame.mouse.get_pressed()[0] == 1:
            pygame.draw.rect(WIN, SILVER, FIVE_SNAKES)
            number_of_snakes = 5                        
    if SIX_SNAKES.collidepoint((mx,my)):
        pygame.draw.rect(WIN, GREY, SIX_SNAKES)
        if pygame.mouse.get_pressed()[0] == 1:
            pygame.draw.rect(WIN, SILVER, SIX_SNAKES)
            number_of_snakes = 6              
    if SEVEN_SNAKES.collidepoint((mx,my)):
        pygame.draw.rect(WIN, GREY, SEVEN_SNAKES)
        if pygame.mouse.get_pressed()[0] == 1:
            pygame.draw.rect(WIN, SILVER, SEVEN_SNAKES)
            number_of_snakes = 7
    if EIGHT_SNAKES.collidepoint((mx,my)):
        pygame.draw.rect(WIN, GREY, EIGHT_SNAKES)
        if pygame.mouse.get_pressed()[0] == 1:
            pygame.draw.rect(WIN, SILVER, EIGHT_SNAKES)
            number_of_snakes = 8      
                             
    speed_text = pygame.font.SysFont('comicsans', 50).render("Speed:", 1, WHITE)
    snake_text = pygame.font.SysFont('comicsans', 50).render("Snake Amount:", 1, WHITE)
    food_text = pygame.font.SysFont('comicsans', 50).render("Food:", 1, WHITE)
    start_text = pygame.font.SysFont('comicsans', 80).render("START", 1, BLACK)
    
    apple_text = pygame.font.SysFont('comicsans', 50).render("Apple", 1, BLACK)
    taco_text = pygame.font.SysFont('comicsans', 50).render("Taco", 1, BLACK)
    burger_text = pygame.font.SysFont('comicsans', 50).render("Burger", 1, BLACK)
    
    four_text = pygame.font.SysFont('comicsans', 50).render("4", 1, BLACK)
    five_text = pygame.font.SysFont('comicsans', 50).render("5", 1, BLACK)
    six_text = pygame.font.SysFont('comicsans', 50).render("6", 1, BLACK)
    seven_text = pygame.font.SysFont('comicsans', 50).render("7", 1, BLACK)
    eight_text = pygame.font.SysFont('comicsans', 50).render("8", 1, BLACK)
    
    slow_text = pygame.font.SysFont('comicsans', 50).render("Slow", 1, BLACK)
    normal_text = pygame.font.SysFont('comicsans', 50).render("Normal", 1, BLACK)
    fast_text = pygame.font.SysFont('comicsans', 50).render("Fast", 1, BLACK)
    
    game_name_text = pygame.font.SysFont('lucidahandwriting', 100).render("Cursed Snake Game", 1, BLACK)
    author_name_text = pygame.font.SysFont('comicsans', 40).render("by Lorin Zhang", 1, BLACK)
    date_text = pygame.font.SysFont('comicsans', 40).render("July 2021", 1, BLACK)

    
    summary_text = pygame.font.SysFont('comicsans', 50).render("You are a(n) " + food_name + " against " + str(number_of_snakes) + " snakes with " + speed_string + " speed.", 1, BLACK)
                  
    WIN.blit(game_name_text, (30, 75))
    WIN.blit(author_name_text, (450, 250))
    WIN.blit(date_text, (450, 300))  
    WIN.blit(summary_text, (130, 550))           
                            
    WIN.blit(start_text, (WIDTH//2 + 40, HEIGHT//2 - 20)) 
    WIN.blit(food_text, (100, HEIGHT//2 + 200))  
    WIN.blit(speed_text, (100, HEIGHT//2 + 300))  
    WIN.blit(snake_text, (100, HEIGHT//2 + 400))  
    
    WIN.blit(apple_text, (670, HEIGHT//2 + 200))
    WIN.blit(taco_text, (270, HEIGHT//2 + 200))
    WIN.blit(burger_text, (470, HEIGHT//2 + 200)) 
    
    WIN.blit(fast_text, (270, HEIGHT//2 + 300))
    WIN.blit(normal_text, (470, HEIGHT//2 + 300))
    WIN.blit(slow_text, (670, HEIGHT//2 + 300)) 
    
    WIN.blit(four_text, (415, HEIGHT//2 + 400))
    WIN.blit(five_text, (515, HEIGHT//2 + 400))
    WIN.blit(six_text, (615, HEIGHT//2 + 400)) 
    WIN.blit(seven_text, (715, HEIGHT//2 + 400))
    WIN.blit(eight_text, (815, HEIGHT//2 + 400))
    
    pygame.display.update()

def main(reset = 0):
    if reset == 1:
        game(snake_speed, number_of_snakes)
    else:
        clock = pygame.time.Clock()
        run = True
        while(run):
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
            draw_main_menu()

if __name__ == "__main__":
    main(reset = 0)