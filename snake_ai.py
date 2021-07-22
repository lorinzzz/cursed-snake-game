import pygame
import pygame_constants
import pygame
import random

# constants
WIDTH, HEIGHT = pygame_constants.WIDTH, pygame_constants.HEIGHT
BLOCK_WIDTH, BLOCK_HEIGHT = pygame_constants.BLOCK_WIDTH, pygame_constants.BLOCK_HEIGHT

class SnakeAI:
    def __init__(self):
        self.s1_kill = 0
        self.s2_kill = 0
        self.s3_kill = 0
        self.s4_kill = 0
        
        self.s1_move = 0
        self.s2_move = 0
        self.s3_move = 0
        self.s4_move = 0
        self.offset = 7
        
        self.random_path_choice1 = random.choice([1,2,3])
        self.random_path_choice2 = random.choice([1,2,3])
        self.random_path_choice3 = random.choice([1,2,3])
        self.random_path_choice4 = random.choice([1,2,3])
        self.random_indices = [0,1,2,3]
        random.shuffle(self.random_indices)
        
    def execute_ai(self, snakes, food): # executes ai and returns a list of directions
        directions = [] 
        for i in range(len(snakes)):
            if i < 4:
                directions.append(self.flanking_ai(snakes, food, i))               
        return directions 
        
        
    def flanking_ai(self, snakes, food, i): # covers up to 4 snakes
        
        
        if i == self.random_indices[0]:
            setup_position_x = food.x + (BLOCK_WIDTH * self.offset)
            setup_position_y = food.y + (BLOCK_HEIGHT * self.offset)
            path_choice = self.random_path_choice1
        if i == self.random_indices[1]:
            setup_position_x = food.x + (BLOCK_WIDTH * self.offset)
            setup_position_y = food.y - (BLOCK_HEIGHT * self.offset)   
            path_choice = self.random_path_choice2
        if i == self.random_indices[2]:
            setup_position_x = food.x - (BLOCK_WIDTH * self.offset)
            setup_position_y = food.y + (BLOCK_HEIGHT * self.offset) 
            path_choice = self.random_path_choice3
        if i == self.random_indices[3]:
            setup_position_x = food.x - (BLOCK_WIDTH * self.offset)
            setup_position_y = food.y - (BLOCK_HEIGHT * self.offset)     
            path_choice = self.random_path_choice4                             
            
        setup_position_x_diff = setup_position_x - snakes[i][0].x
        setup_position_y_diff = setup_position_y - snakes[i][0].y
        x_diff = food.x - snakes[i][0].x
        y_diff = food.y - snakes[i][0].y
        
        
        if (i == 0 and self.s1_kill == 0) or (i == 1 and self.s2_kill == 0) or (i == 2 and self.s3_kill == 0) or (i == 3 and self.s4_kill == 0):
            if path_choice == 1:
                direction_to_append = self.line_up_ai(snakes, food, i, 0, setup_position_x, setup_position_y)
            if path_choice == 2:
                direction_to_append = self.shortest_path_ai(snakes, food, i, setup_position_x, setup_position_y)
            if path_choice == 3:
                direction_to_append = self.line_up_ai(snakes, food, i, 1, setup_position_x, setup_position_y)
        # check if snake is in position to attack        
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
        
    def shortest_path_ai(self, snakes, food, i, setup_position_x = -1, setup_position_y = -1): # ai for shortest path to food
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
        if orientation == 1: # horizontal
            print("here10")
            if abs(x_diff) > BLOCK_WIDTH: 
                print("here11")
                if x_diff >= 0:
                    # make sure snake doesn't commit a full 180 turn into its own body
                    if snakes[i][0].x + BLOCK_WIDTH == snakes[i][1].x or snakes[i][0].x + BLOCK_WIDTH == WIDTH:
                        # make srue snakes doesn't go out of bounds
                        if snakes[i][0].y + BLOCK_HEIGHT > HEIGHT:
                            direction_to_append = 0
                        elif snakes[i][0].y - BLOCK_HEIGHT < 0:
                            direction_to_append = 180
                        elif snakes[i][0].y + BLOCK_HEIGHT <= HEIGHT and snakes[i][0].y - BLOCK_HEIGHT >= 0:
                            direction_to_append = random.choice([0,180])
                        print("forced to go up or down")                       
                    else:
                        direction_to_append = 90
                    if set_up_flag == 1:
                        print("here22")
                        if snakes[i][0].x + BLOCK_WIDTH == WIDTH:
                            direction_to_append = self.shortest_path_ai(snakes, food, i)    
                            print("forced to hunt")                         
                else:
                    if snakes[i][0].x - BLOCK_WIDTH == snakes[i][1].x or snakes[i][0].x - BLOCK_HEIGHT == 0:
                        # make sure snake doesn't go out of bounds
                        if snakes[i][0].y + BLOCK_HEIGHT > HEIGHT:
                            direction_to_append = 0
                        elif snakes[i][0].y - BLOCK_HEIGHT < 0:
                            direction_to_append = 180
                        elif snakes[i][0].y + BLOCK_HEIGHT <= HEIGHT and snakes[i][0].y - BLOCK_HEIGHT >= 0:
                            direction_to_append = random.choice([0,180])
                        print("forced to go up or down")                          
                    else:
                        direction_to_append = 270  
                    if set_up_flag == 1:
                        if snakes[i][0].x - BLOCK_WIDTH == 0:
                            direction_to_append = self.shortest_path_ai(snakes, food, i)   
                            print("forced to hunt")                                           
            else:
                print("here12")
                if y_diff >= 0: 
                    if snakes[i][0].y + BLOCK_HEIGHT == snakes[i][1].y or snakes[i][0].y + BLOCK_HEIGHT == HEIGHT:
                        if snakes[i][0].x + BLOCK_WIDTH > WIDTH:
                            direction_to_append = 90
                        elif snakes[i][0].x - BLOCK_WIDTH < 0:
                            direction_to_append = 270
                        elif snakes[i][0].x + BLOCK_WIDTH <= WIDTH and snakes[i][0].x - BLOCK_WIDTH >= 0:
                            direction_to_append = random.choice([90,270])
                        print("forced to go left or right")                            
                    else:   
                        direction_to_append = 180  
                    if set_up_flag == 1:
                        if snakes[i][0].y + BLOCK_HEIGHT == HEIGHT:
                            direction_to_append = self.shortest_path_ai(snakes, food, i)      
                            print("forced to hunt")                         
                else:    
                    if snakes[i][0].y - BLOCK_HEIGHT == snakes[i][1].y or snakes[i][0].y - BLOCK_HEIGHT == 0:
                        if snakes[i][0].x + BLOCK_WIDTH > WIDTH:
                            direction_to_append = 90
                        elif snakes[i][0].x - BLOCK_WIDTH < 0:
                            direction_to_append = 270
                        elif snakes[i][0].x + BLOCK_WIDTH <= WIDTH and snakes[i][0].x - BLOCK_WIDTH >= 0:
                            direction_to_append = random.choice([90,270])
                        print("forced to go left or right")                        
                    else:
                        direction_to_append = 0  
                    if set_up_flag == 1:
                        if snakes[i][0].y - BLOCK_HEIGHT == 0:
                            direction_to_append = self.shortest_path_ai(snakes, food, i)
                            print("forced to hunt")                         
                        
                        
        elif orientation == 0: # vertical
            print("here")
            if abs(y_diff) > BLOCK_WIDTH: 
                print("here1")
                if y_diff >= 0:
                    print("here3")
                    if snakes[i][0].y + BLOCK_HEIGHT == snakes[i][1].y or snakes[i][0].y + BLOCK_HEIGHT == HEIGHT:
                        if snakes[i][0].x + BLOCK_WIDTH > WIDTH:
                            direction_to_append = 90
                        elif snakes[i][0].x - BLOCK_WIDTH < 0:
                            direction_to_append = 270
                        elif snakes[i][0].x + BLOCK_WIDTH <= WIDTH and snakes[i][0].x - BLOCK_WIDTH >= 0:
                            direction_to_append = random.choice([90,270])
                        print("forced to go left or right")                              
                    else:   
                        direction_to_append = 180 
                    if set_up_flag == 1:
                        print("here21")
                        if snakes[i][0].y + BLOCK_HEIGHT == HEIGHT:
                            direction_to_append = self.shortest_path_ai(snakes, food, i)      
                            print("forced to hunt")                          
                else:    
                    print("here4")
                    if snakes[i][0].y - BLOCK_HEIGHT == snakes[i][1].y or snakes[i][0].y - BLOCK_HEIGHT == 0:
                        print("here5")
                        if snakes[i][0].x + BLOCK_WIDTH > WIDTH:
                            direction_to_append = 90
                        elif snakes[i][0].x - BLOCK_WIDTH < 0:
                            direction_to_append = 270
                        elif snakes[i][0].x + BLOCK_WIDTH <= WIDTH and snakes[i][0].x - BLOCK_WIDTH >= 0:
                            direction_to_append = random.choice([90,270])
                        print("forced to go left or right")                       
                    else:
                        print("here7")
                        direction_to_append = 0 
                    if set_up_flag == 1:
                        print("here6")
                        if snakes[i][0].y - BLOCK_HEIGHT == 0:
                            print("here8")
                            direction_to_append = self.shortest_path_ai(snakes, food, i)
                            print("forced to hunt")                                           
            else:
                print("here2")
                if x_diff >= 0:
                    # make sure snake doesn't commit a full 180 turn into its own body
                    if snakes[i][0].x + BLOCK_WIDTH == snakes[i][1].x or snakes[i][0].x + BLOCK_WIDTH == WIDTH:
                        # make srue snakes doesn't go out of bounds
                        if snakes[i][0].y + BLOCK_HEIGHT > HEIGHT:
                            direction_to_append = 0
                        elif snakes[i][0].y - BLOCK_HEIGHT < 0:
                            direction_to_append = 180
                        elif snakes[i][0].y + BLOCK_HEIGHT <= HEIGHT and snakes[i][0].y - BLOCK_HEIGHT >= 0:
                            direction_to_append = random.choice([0,180])
                        print("forced to go up or down")                        
                    else:
                        direction_to_append = 90
                    if set_up_flag == 1:
                        if snakes[i][0].x + BLOCK_WIDTH == WIDTH:
                            direction_to_append = self.shortest_path_ai(snakes, food, i)    
                            print("forced to hunt")                         
                else:
                    if snakes[i][0].x - BLOCK_WIDTH == snakes[i][1].x or snakes[i][0].x - BLOCK_HEIGHT == 0:
                        # make sure snake doesn't go out of bounds
                        if snakes[i][0].y + BLOCK_HEIGHT > HEIGHT:
                            direction_to_append = 0
                        elif snakes[i][0].y - BLOCK_HEIGHT < 0:
                            direction_to_append = 180
                        elif snakes[i][0].y + BLOCK_HEIGHT <= HEIGHT and snakes[i][0].y - BLOCK_HEIGHT >= 0:
                            direction_to_append = random.choice([0,180])
                        print("forced to go up or down")                             
                    else:
                        direction_to_append = 270  
                    if set_up_flag == 1:
                        if snakes[i][0].x - BLOCK_WIDTH == 0:
                            direction_to_append = self.shortest_path_ai(snakes, food, i)   
                            print("forced to hunt")                                                    
                
        return direction_to_append
    def patrolling_ai(self): # ai patrols certain sections of the window for a period before moving to the next, if food comes close enough it will pursue
        pass
    
    def circling_ai(self): # ai where snake will run circles around a certain radius in the map, no real intentions to kill the food. the snake must be long however! 
        pass