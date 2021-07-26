import pygame
import pygame_constants
import pygame
import random

# constants
WIDTH, HEIGHT = pygame_constants.WIDTH, pygame_constants.HEIGHT
BLOCK_WIDTH, BLOCK_HEIGHT = pygame_constants.BLOCK_WIDTH, pygame_constants.BLOCK_HEIGHT
LONG_OFFSET = [30, 60, 90, 120, 150, 180, 210]
SHORT_OFFSET = [240, 270, 300, 330, 360, 390]


class SnakeAI:
    def __init__(self):
        # kill state of snakes 
        self.s1_kill = 0
        self.s2_kill = 0
        self.s3_kill = 0
        self.s4_kill = 0
        
        # hold how many moves flanking AI can make when in kill mode
        self.s1_move = 0
        self.s2_move = 0
        self.s3_move = 0
        self.s4_move = 0
        self.offset = 5

        self.revolutions = [-1, -1]
        self.circular_offset = [0, 0]
        self.start_pos = [[0,0], [0,0]]
        self.circling_ai_initial_setup = 1
        self.circle_state = [0,0]
        self.moves = [0,0]
        self.total_revolutions = [0, 0]

        self.random_path_choice1 = random.choice([1,2,3])
        self.random_path_choice2 = random.choice([1,2,3])
        self.random_path_choice3 = random.choice([1,2,3])
        self.random_path_choice4 = random.choice([1,2,3])
        self.random_indices_for_path = [0,1,2,3]
        random.shuffle(self.random_indices_for_path) # for random paths in flanking ai
        self.random_indices_for_orientation = [0,1]
        random.shuffle(self.random_indices_for_orientation)

    def execute_ai(self, snakes, food): # executes ai and returns a list of directions
        directions = [] 
        for i in range(len(snakes)):
            directions.append(self.circling_ai(snakes, food, i, 1, self.circling_ai_initial_setup))  
        if self.circling_ai_initial_setup == 1:
            self.circling_ai_initial_setup = 0                      
        return directions 
            
    # the flanking ai goes to a "setup" position offset from the food before moving in to attack
    # it uses the shortest and line up path choices, hence we can just call those functions to use those pathfinding functions       
    def flanking_ai(self, snakes, food, i): # covers up to 4 snakes
        
        # assign random offset and path choices for each snake
        if i == self.random_indices_for_path[0]:
            setup_position_x = food.x + (BLOCK_WIDTH * self.offset)
            setup_position_y = food.y + (BLOCK_HEIGHT * self.offset)
            path_choice = self.random_path_choice1
        if i == self.random_indices_for_path[1]:
            setup_position_x = food.x + (BLOCK_WIDTH * self.offset)
            setup_position_y = food.y - (BLOCK_HEIGHT * self.offset)   
            path_choice = self.random_path_choice2
        if i == self.random_indices_for_path[2]:
            setup_position_x = food.x - (BLOCK_WIDTH * self.offset)
            setup_position_y = food.y + (BLOCK_HEIGHT * self.offset) 
            path_choice = self.random_path_choice3
        if i == self.random_indices_for_path[3]:
            setup_position_x = food.x - (BLOCK_WIDTH * self.offset)
            setup_position_y = food.y - (BLOCK_HEIGHT * self.offset)     
            path_choice = self.random_path_choice4                             
        
        # move towards set up region
        if (i == 0 and self.s1_kill == 0) or (i == 1 and self.s2_kill == 0) or (i == 2 and self.s3_kill == 0) or (i == 3 and self.s4_kill == 0):
            if path_choice == 1:
                direction_to_append = self.line_up_ai(snakes, food, i, 0, setup_position_x, setup_position_y)
            if path_choice == 2:
                direction_to_append = self.shortest_path_ai(snakes, food, i, setup_position_x, setup_position_y)
            if path_choice == 3:
                direction_to_append = self.line_up_ai(snakes, food, i, 1, setup_position_x, setup_position_y)
                
        # check if snake is in set up region, if so it is in position to attack, set kill status         
        if (i == 0 and snakes[i][0].x >= setup_position_x - BLOCK_WIDTH and snakes[i][0].x <= setup_position_x + BLOCK_WIDTH and snakes[i][0].y >= setup_position_y - BLOCK_HEIGHT and snakes[i][0].y <= setup_position_y + BLOCK_HEIGHT and self.s1_kill == 0):
            self.s1_kill = 1
            print("snake " + str(i) + " in position!")
            print("path choice: ", str(path_choice))
        if (i == 1 and snakes[i][0].x >= setup_position_x - BLOCK_WIDTH and snakes[i][0].x <= setup_position_x + BLOCK_WIDTH and snakes[i][0].y >= setup_position_y - BLOCK_HEIGHT and snakes[i][0].y <= setup_position_y + BLOCK_HEIGHT and self.s2_kill == 0):
            self.s2_kill = 1
            print("snake " + str(i) + " in position!")
        if (i == 2 and snakes[i][0].x >= setup_position_x - BLOCK_WIDTH and snakes[i][0].x <= setup_position_x + BLOCK_WIDTH and snakes[i][0].y >= setup_position_y - BLOCK_HEIGHT and snakes[i][0].y <= setup_position_y + BLOCK_HEIGHT and self.s3_kill == 0):
            self.s3_kill = 1
            print("snake " + str(i) + " in position!")
        if (i == 3 and snakes[i][0].x >= setup_position_x - BLOCK_WIDTH and snakes[i][0].x <= setup_position_x + BLOCK_WIDTH and snakes[i][0].y >= setup_position_y - BLOCK_HEIGHT and snakes[i][0].y <= setup_position_y + BLOCK_HEIGHT and self.s4_kill == 0):
            self.s4_kill = 1
            print("snake " + str(i) + " in position!")
            
        # kil mode: moves to eat the food
        if (i == 0 and self.s1_kill == 1) or (i == 1 and self.s2_kill == 1) or (i == 2 and self.s3_kill == 1) or (i == 3 and self.s4_kill == 1):
            if path_choice == 1: # shortest path 
                direction_to_append = self.shortest_path_ai(snakes, food, i)
            elif path_choice == 2: # vertical line up
                direction_to_append = self.line_up_ai(snakes, food, i, 0)
            elif path_choice == 3: # horizontal line up
                direction_to_append = self.line_up_ai(snakes, food, i, 1)
            if i == 0:
                if self.s1_move == 25:                   
                    self.s1_kill = 0
                    self.s1_move = 0
                    print("snake " + str(i) + " in set up mode") 
                self.s1_move += 1
            if i == 1:
                if self.s2_move == 25:                   
                    self.s2_kill = 0
                    self.s2_move = 0
                    print("snake " + str(i) + " in set up mode") 
                self.s2_move += 1
            if i == 2:
                if self.s3_move == 25:                   
                    self.s3_kill = 0
                    self.s3_move = 0
                    print("snake " + str(i) + " in set up mode") 
                self.s3_move += 1
            if i == 3:
                if self.s4_move == 25:                   
                    self.s4_kill = 0
                    self.s4_move = 0
                    print("snake " + str(i) + " in set up mode") 
                self.s4_move += 1                   
                   
        return direction_to_append
        
    def shortest_path_ai(self, snakes, food, i, setup_position_x = -1, setup_position_y = -1): # ai for shortest path to a point (x,y)
        # determine if we are moving towards food or setup position of coord are provided 
        if setup_position_x == -1 and setup_position_y == -1:
            x_diff = food.x - snakes[i][0].x
            y_diff = food.y - snakes[i][0].y
        else:
            x_diff = setup_position_x - snakes[i][0].x
            y_diff = setup_position_y - snakes[i][0].y                
        if abs(x_diff) > abs(y_diff):
            if x_diff >= 0:
                direction_to_append = 90 
            else:
                direction_to_append = 270
        else:
            if y_diff >= 0: 
                direction_to_append = 180
            else:    
                direction_to_append = 0
                
        return direction_to_append
    
    def line_up_ai(self, snakes, food, i, orientation, setup_position_x = -1, setup_position_y = -1): # ai where it either lines up vertically or horizontally before moving in beeline towards the food, orientation  parameter determines whether to line it up horizontaly or vertically
        # determine if the snakes are going towards the food or the setup position
        # if so we need the appropirate x and y diff, and we need the code to prevent the snake from being cornered
        if setup_position_x == -1 and setup_position_y == -1:
            x_diff = food.x - snakes[i][0].x
            y_diff = food.y - snakes[i][0].y
            set_up_flag = 0
        else:
            x_diff = setup_position_x - snakes[i][0].x
            y_diff = setup_position_y - snakes[i][0].y  
            set_up_flag = 1   
            if setup_position_x > WIDTH or setup_position_y > HEIGHT or setup_position_x < 0 or setup_position_y < 0:
                out_of_bounds = 1
                print('outs of bounds')
            else:
                out_of_bounds = 0     
        if orientation == 1: 
            if abs(x_diff) > BLOCK_WIDTH: 
                if x_diff >= 0: # go right
                    # make sure snake doesn't commit a full 180 turn into its own body
                    if snakes[i][0].x + BLOCK_WIDTH == snakes[i][1].x or snakes[i][0].x + BLOCK_WIDTH == WIDTH:
                        # make sure snakes doesn't go out of bounds
                        if snakes[i][0].y + BLOCK_HEIGHT == HEIGHT: # go up
                            direction_to_append = 0
                        elif snakes[i][0].y == 0: # go down
                            direction_to_append = 180
                        elif snakes[i][0].y > 0 and snakes[i][0].y + BLOCK_HEIGHT < HEIGHT:
                            direction_to_append = random.choice([0,180])
                        print("forced to go up or down")                       
                    else:
                        direction_to_append = 90
                    # if the snake is going to the setup region but it is out of map force it to just hunt the food
                    # that way the snake won't get cornered and have nowhere to go
                    if set_up_flag == 1 and out_of_bounds == 1:
                        direction_to_append = self.shortest_path_ai(snakes, food, i)    
                        print("forced to hunt")   
                # the rest of the code follows the above, just a matter of going left, up, and or down                                 
                else: # go left
                    if snakes[i][0].x - BLOCK_WIDTH == snakes[i][1].x or snakes[i][0].x <= 0:
                        if snakes[i][0].y + BLOCK_HEIGHT == HEIGHT: # go up
                            direction_to_append = 0
                        elif snakes[i][0].y == 0: # go down
                            direction_to_append = 180
                        elif snakes[i][0].y > 0 and snakes[i][0].y + BLOCK_HEIGHT < HEIGHT:
                            direction_to_append = random.choice([0,180])
                        print("forced to go up or down")                          
                    else:
                        direction_to_append = 270  
                    if set_up_flag == 1 and out_of_bounds == 1:
                        direction_to_append = self.shortest_path_ai(snakes, food, i)    
                        print("forced to hunt")                                            
            else:
                if y_diff >= 0: # go down
                    if snakes[i][0].y + BLOCK_HEIGHT == snakes[i][1].y or snakes[i][0].y + BLOCK_HEIGHT == HEIGHT:
                        if snakes[i][0].x == WIDTH: # go left
                            direction_to_append = 270
                        elif snakes[i][0].x == 0: # go right
                            direction_to_append = 90
                        elif snakes[i][0].x > 0 and snakes[i][0].x + BLOCK_WIDTH < WIDTH:
                            direction_to_append = random.choice([90,270])
                        print("forced to go left or right")                            
                    else:   
                        direction_to_append = 180  
                    if set_up_flag == 1 and out_of_bounds == 1:
                        direction_to_append = self.shortest_path_ai(snakes, food, i)    
                        print("forced to hunt")                          
                else:   # go up
                    if snakes[i][0].y - BLOCK_HEIGHT == snakes[i][1].y or snakes[i][0].y <= 0:
                        if snakes[i][0].x == WIDTH: # go left
                            direction_to_append = 270
                        elif snakes[i][0].x == 0:
                            direction_to_append = 90 # go right
                        elif snakes[i][0].x > 0 and snakes[i][0].x + BLOCK_WIDTH < WIDTH:
                            direction_to_append = random.choice([90,270])
                        print("forced to go left or right")                        
                    else:
                        direction_to_append = 0  
                    if set_up_flag == 1 and out_of_bounds == 1:
                        direction_to_append = self.shortest_path_ai(snakes, food, i)    
                        print("forced to hunt")                          
        # vertical                                     
        elif orientation == 0:
            if abs(y_diff) > BLOCK_WIDTH: 
                if y_diff >= 0: # go down
                    if snakes[i][0].y + BLOCK_HEIGHT == snakes[i][1].y or snakes[i][0].y + BLOCK_HEIGHT == HEIGHT:
                        if snakes[i][0].x == WIDTH: # go left
                            direction_to_append = 270
                        elif snakes[i][0].x == 0: # go right
                            direction_to_append = 90
                        elif snakes[i][0].x > 0 and snakes[i][0].x + BLOCK_WIDTH < WIDTH:
                            direction_to_append = random.choice([90,270])
                        print("forced to go left or right")                              
                    else:   
                        direction_to_append = 180 
                    if set_up_flag == 1 and out_of_bounds == 1:
                        direction_to_append = self.shortest_path_ai(snakes, food, i)    
                        print("forced to hunt")                          
                else:    # go up
                    if snakes[i][0].y - BLOCK_HEIGHT == snakes[i][1].y or snakes[i][0].y <= 0:
                        if snakes[i][0].x == WIDTH: # go left
                            direction_to_append = 270
                        elif snakes[i][0].x == 0:
                            direction_to_append = 90 # go right
                        elif snakes[i][0].x > 0 and snakes[i][0].x + BLOCK_WIDTH < WIDTH:
                            direction_to_append = random.choice([90,270])
                        print("forced to go left or right")                    
                    else:
                        direction_to_append = 0 
                    if set_up_flag == 1 and out_of_bounds == 1:
                        direction_to_append = self.shortest_path_ai(snakes, food, i)    
                        print("forced to hunt")                                             
            else:
                if x_diff >= 0:
                    # make sure snake doesn't commit a full 180 turn into its own body
                    if snakes[i][0].x + BLOCK_WIDTH == snakes[i][1].x or snakes[i][0].x + BLOCK_WIDTH == WIDTH:
                        # make sure snakes doesn't go out of bounds
                        if snakes[i][0].y + BLOCK_HEIGHT == HEIGHT: # go up
                            direction_to_append = 0
                        elif snakes[i][0].y == 0: # go down
                            direction_to_append = 180
                        elif snakes[i][0].y > 0 and snakes[i][0].y + BLOCK_HEIGHT < HEIGHT:
                            direction_to_append = random.choice([0,180])
                        print("forced to go up or down")                         
                    else:
                        direction_to_append = 90
                    if set_up_flag == 1 and out_of_bounds == 1:
                        direction_to_append = self.shortest_path_ai(snakes, food, i)    
                        print("forced to hunt")                         
                else:
                    if snakes[i][0].x - BLOCK_WIDTH == snakes[i][1].x or snakes[i][0].x <= 0:
                        if snakes[i][0].y + BLOCK_HEIGHT == HEIGHT: # go up
                            direction_to_append = 0
                        elif snakes[i][0].y == 0: # go down
                            direction_to_append = 180
                        elif snakes[i][0].y > 0 and snakes[i][0].y + BLOCK_HEIGHT < HEIGHT:
                            direction_to_append = random.choice([0,180])
                        print("forced to go up or down")                               
                    else:
                        direction_to_append = 270  
                    if set_up_flag == 1 and out_of_bounds == 1:
                        direction_to_append = self.shortest_path_ai(snakes, food, i)    
                        print("forced to hunt")                                                    
                
        return direction_to_append
    def patrolling_ai(self): # ai patrols certain sections of the window for a period before moving to the next, if food comes close enough it will pursue
        pass
    
    def circling_ai(self, snakes, food, i, mode, setup_flag): # ai where snake will run circles around a certain radius in the map, no real intentions to kill the food. the snake must be long for outer edges, and shorter for circles towards the center! 
        # this function will be called with a snake and its index if it is the longest or shortest snake, or both! 
        # no need to worry about figuring out length here
        # mode parameter decides if its an ai for short or long snake length, 0 = short snake, 1 = long snake
        # supports up to two snakes 
        # the radius of the circle will just be an offset from the width or height
        if i == 0:
            index = 0
        elif i == 1:
            index = 1

        if setup_flag == 1 or self.revolutions[index] == self.total_revolutions[index]: # get new offset and start position for snake
            self.revolutions[index] = -1
            self.circle_state[index] = 0           
            if mode == 0: # short snake
                self.circular_offset[index] = random.choice(SHORT_OFFSET)
                self.total_revolutions[index] =  random.randint(7, 15)    # 7-15 laps for short snake 
            elif mode == 1: # long snake
                self.circular_offset[index] = random.choice(LONG_OFFSET)
                self.total_revolutions[index] =  random.randint(2, 7)    # 2-6 laps for long snake 
            print(self.total_revolutions[index], " revolutions")
            print(snakes[i][0].x, snakes[i][0].y)
            x_y_cord = []
            # create x cord on offset closest to snake 
            if abs(self.circular_offset[index] - snakes[i][0].x) < abs(WIDTH - self.circular_offset[index] - snakes[i][0].x):
                x_y_cord.append(self.circular_offset[index])
            else:
                x_y_cord.append(WIDTH - self.circular_offset[index])
            # create y cord on offset closest to snake 
            if abs(self.circular_offset[index] - snakes[i][0].y) < abs(HEIGHT - self.circular_offset[index] - snakes[i][0].y):
                x_y_cord.append(self.circular_offset[index])
            else:
                x_y_cord.append(WIDTH - self.circular_offset[index])
            print(x_y_cord)
            # the above will get us a corner closest to the snake on the offset square, now we need to figure out whether to slide the x or y value to get closer to the snake
            if abs(x_y_cord[0] - snakes[i][0].x) < abs(x_y_cord[1] - snakes[i][0].y): # if x value closer slide x value to snake and keep y value
                if snakes[i][0].x >= self.circular_offset[index] and snakes[i][0].x <= WIDTH - self.circular_offset[index]: # only slide if snake is within offset lines
                    x_y_cord[0] = snakes[i][0].x
                # else it stays in corner 
                print("slid x val")
            else: # if y value closer slide y value to snake and keep x value
                if snakes[i][0].y >= self.circular_offset[index] and snakes[i][0].y <= WIDTH - self.circular_offset[index]: # only slide if snake is within offset lines
                    x_y_cord[1] = snakes[i][0].y                
                print("slid y val")
            
            self.start_pos[index] = x_y_cord
            print("starting pos:" , x_y_cord)
            print("offset: ", self.circular_offset[index])

        # go to starting position
        if (snakes[i][0].x != self.start_pos[index][0] or snakes[i][0].y != self.start_pos[index][1]) and self.circle_state[index] == 0:
            print(snakes[i][0].x, snakes[i][0].y)
            direction_to_append = self.shortest_path_ai(snakes, food, i, self.start_pos[index][0], self.start_pos[index][1])
        elif (snakes[i][0].x == self.start_pos[index][0] and snakes[i][0].y == self.start_pos[index][1]) and self.circle_state[index] == 0:
            print("in circle state")
            self.circle_state[index] = 1

        # check if snake head in proximity with food, (within 4 blocks away)
        if food.x >= snakes[i][0].x - 120 and food.x <= snakes[i][0].x + 150 and food.y >= snakes[i][0].y - 120 and food.y <= snakes[i][0].y + 150:
            self.circle_state[index] = 3 # kill mode
            print("circling snake in kill mode!")
        
        if self.circle_state[index] == 3: # kill food
            direction_to_append = self.shortest_path_ai(snakes, food, i)
            self.moves[index] += 1
        
        if self.moves[index] == 25:
            self.moves[index] = 0
            self.circle_state[index] = 0
            self.revolutions[index] == self.total_revolutions[index]
        

        # check if snakes is at corner before deciding whether to go up down left or right
        # check if snake is not in corner and on vertical or horizontal offset border line
        if self.circle_state[index] == 1:

            ccw = 0
            if ccw == 1:
                direction = [180, 0, 270, 90]
                corner_direction = [180, 270, 90, 0]
            else:
                direction = [0, 180, 90, 270]
                corner_direction = [90, 180, 0, 270]

            print(snakes[i][0].x, snakes[i][0].y)
            if snakes[i][0].x != self.circular_offset[index] and snakes[i][0].x != WIDTH - self.circular_offset[index]: # this means snake is right on horizontal border of offset so must go left or right 
                # GOING CW for now
                # check which horizontal border it is on before deciding left or right
                if snakes[i][0].y == self.circular_offset[index]: # top border
                    direction_to_append = direction[2]
                elif snakes[i][0].y == HEIGHT - self.circular_offset[index]: # bottom border
                    direction_to_append = direction[3]
            elif snakes[i][0].y != self.circular_offset[index] and snakes[i][0].y != HEIGHT - self.circular_offset[index]: # else snake is right on vertical border of offset so must go up or down
                if snakes[i][0].x == self.circular_offset[index]: # left border
                    direction_to_append = direction[0]
                elif snakes[i][0].x == WIDTH - self.circular_offset[index]: # right border
                    direction_to_append = direction[1] 
            else: # snake is at a corner
                if snakes[i][0].y == self.circular_offset[index]: # snake is at top border
                    if snakes[i][0].x == self.circular_offset[index]: # at top left corner
                        direction_to_append = corner_direction[0]
                    elif snakes[i][0].x == WIDTH - self.circular_offset[index]: # top right corner
                        direction_to_append = corner_direction[1]
                elif snakes[i][0].y == HEIGHT - self.circular_offset[index]:
                    if snakes[i][0].x == self.circular_offset[index]: # at bottom left corner
                        direction_to_append = corner_direction[2]
                    elif snakes[i][0].x == WIDTH - self.circular_offset[index]: # bottom right corner                
                        direction_to_append = corner_direction[3]

            # when snake head returns to starting pos, increase revolutions 
            if snakes[i][0].x == self.start_pos[index][0] and snakes[i][0].y == self.start_pos[index][1]:
                self.revolutions[index] += 1
                print(self.revolutions[index])
        return direction_to_append

    #7/22/21 1:30am - note: consider adding "coin" pickups on the window to increase score, gives player an incentive to move around to specific locatins and take risks