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
        
    def execute_ai(self, snakes, food): # executes ai and returns a list of directions
        directions = [] 
        for i in range(len(snakes)):
            if i <= 4:
                directions.append(self.flanking_ai(snakes, food, i))
        
        
        return directions 
        
        
    def flanking_ai(self, snakes, food, i): # covers up to 4 snakes
        # note: HAVE TO CHECK TO MAKE SURE IT DOESN'T GO OFF SCREEN, IF IT DOES JUST HAVE THE AI MATCH X OR Y VALUES INSTEAD
        if i == 0:
            setup_position_x = food.x + (BLOCK_WIDTH * self.offset)
            setup_position_y = food.y + (BLOCK_HEIGHT * self.offset)
        if i == 1:
            setup_position_x = food.x + (BLOCK_WIDTH * self.offset)
            setup_position_y = food.y - (BLOCK_HEIGHT * self.offset)   
        if i == 2:
            setup_position_x = food.x - (BLOCK_WIDTH * self.offset)
            setup_position_y = food.y + (BLOCK_HEIGHT * self.offset) 
        if i == 3:
            setup_position_x = food.x - (BLOCK_WIDTH * self.offset)
            setup_position_y = food.y - (BLOCK_HEIGHT * self.offset)                                  
            
        setup_position_x_diff = setup_position_x - snakes[i][0].x
        setup_position_y_diff = setup_position_y - snakes[i][0].y
        x_diff = food.x - snakes[i][0].x
        y_diff = food.y - snakes[i][0].y
        if (i == 0 and self.s1_kill == 0) or (i == 1 and self.s2_kill == 0) or (i == 2 and self.s3_kill == 0) or (i == 3 and self.s4_kill == 0):
            if abs(setup_position_x_diff) > BLOCK_WIDTH :
                if setup_position_x_diff >= 0:
                    if snakes[i][0].x + BLOCK_WIDTH == snakes[i][1].x or snakes[i][0].x + BLOCK_WIDTH == WIDTH:
                        # make srue snakes doesn't go out of bounds
                        if snakes[i][0].y + BLOCK_HEIGHT > HEIGHT:
                            direction_to_append = 0
                        elif snakes[i][0].y + BLOCK_HEIGHT < 0:
                            direction_to_append = 180
                        elif snakes[i][0].y + BLOCK_HEIGHT <= HEIGHT and snakes[i][0].y + BLOCK_HEIGHT >= 0:
                            direction_to_append = random.choice([0,180])
                        #print("forced to go up or down")
                    else:
                        direction_to_append = 90
                else:
                    if snakes[i][0].x - BLOCK_WIDTH == snakes[i][1].x or snakes[i][0].x - BLOCK_WIDTH == 0:
                        # make sure snake doesn't go out of bounds
                        if snakes[i][0].y + BLOCK_HEIGHT > HEIGHT:
                            direction_to_append = 0
                        elif snakes[i][0].y + BLOCK_HEIGHT < 0:
                            direction_to_append = 180
                        elif snakes[i][0].y + BLOCK_HEIGHT <= HEIGHT and snakes[i][0].y + BLOCK_HEIGHT >= 0:
                            direction_to_append = random.choice([0,180])
                        #print("forced to go up or down")   
                    else:
                        direction_to_append = 270 
            else:
                if setup_position_y_diff >= 0: 
                    if snakes[i][0].y + BLOCK_HEIGHT == snakes[i][1].y or snakes[i][0].y + BLOCK_HEIGHT == HEIGHT:
                        if snakes[i][0].x + BLOCK_WIDTH > WIDTH:
                            direction_to_append = 90
                        elif snakes[i][0].x + BLOCK_WIDTH < 0:
                            direction_to_append = 270
                        elif snakes[i][0].x + BLOCK_WIDTH <= WIDTH and snakes[i][0].x + BLOCK_WIDTH >= 0:
                            direction_to_append = random.choice([90,270])
                        #print("forced to go left or right")    
                    else:   
                        direction_to_append = 180  
                else:    
                    if snakes[i][0].y - BLOCK_HEIGHT == snakes[i][1].y or snakes[i][0].y - BLOCK_HEIGHT == 0:
                        if snakes[i][0].x + BLOCK_WIDTH > WIDTH:
                            direction_to_append = 90
                        elif snakes[i][0].x + BLOCK_WIDTH < 0:
                            direction_to_append = 270
                        elif snakes[i][0].x + BLOCK_WIDTH <= WIDTH and snakes[i][0].x + BLOCK_WIDTH >= 0:
                            direction_to_append = random.choice([90,270])
                        #print("forced to go left or right")
                    else:
                        direction_to_append = 0  

        # check if snake is in position to attack        
            
        if (i == 0 and snakes[i][0].x >= setup_position_x - BLOCK_WIDTH and snakes[i][0].x <= setup_position_x + BLOCK_WIDTH and snakes[i][0].y >= setup_position_y - BLOCK_HEIGHT and snakes[i][0].y <= setup_position_y + BLOCK_HEIGHT and self.s1_kill == 0):
            self.s1_kill = 1
            print("snake " + str(i) + " in position!")
        if (i == 1 and snakes[i][0].x >= setup_position_x - BLOCK_WIDTH and snakes[i][0].x <= setup_position_x + BLOCK_WIDTH and snakes[i][0].y >= setup_position_y - BLOCK_HEIGHT and snakes[i][0].y <= setup_position_y + BLOCK_HEIGHT and self.s2_kill == 0):
            self.s2_kill = 1
            print("snake " + str(i) + " in position!")
        if (i == 2 and snakes[i][0].x >= setup_position_x - BLOCK_WIDTH and snakes[i][0].x <= setup_position_x + BLOCK_WIDTH and snakes[i][0].y >= setup_position_y - BLOCK_HEIGHT and snakes[i][0].y <= setup_position_y + BLOCK_HEIGHT and self.s3_kill == 0):
            self.s3_kill = 1
            print("snake " + str(i) + " in position!")
        if (i == 3 and snakes[i][0].x >= setup_position_x - BLOCK_WIDTH and snakes[i][0].x <= setup_position_x + BLOCK_WIDTH and snakes[i][0].y >= setup_position_y - BLOCK_HEIGHT and snakes[i][0].y <= setup_position_y + BLOCK_HEIGHT and self.s4_kill == 0):
            self.s4_kill = 1
            print("snake " + str(i) + " in position!")
            
            
        if (i == 0 and self.s1_kill == 1) or (i == 1 and self.s2_kill == 1) or (i == 2 and self.s3_kill == 1) or (i == 3 and self.s4_kill == 1):
            #print("killing")
            if abs(x_diff) > abs(y_diff):
                if x_diff >= 0:
                    direction_to_append = 90 # NEED TO MAKE SURE THIS DOESN'T GO OFF THE SCREEN TO THE RIGHT
                else:
                    direction_to_append = 270 # NEED TO MAKE SURE THIS DOESN'T GO OFF THE SCREEN TO THE LEFT
            else:
                if y_diff >= 0: 
                    direction_to_append = 180  
                else:    
                    direction_to_append = 0  
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
        
    def shortest_path_ai(self, food, snakes, i): # ai for shortest path to food
        x_diff = food.x - snakes[i][0].x
        y_diff = food.y - snakes[i][0].y     
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
    
    def line_up_ai(self): # ai where it either lines up vertically or horizontally before moving in beeline towards the food
        pass
    
    def patrolling_ai(self): # ai patrols certain sections of the window for a period before moving to the next, if food comes close enough it will pursue
        pass
    
    def circling_ai(self): # ai where snake will run circles around a certain radius in the map, no real intentions to kill the food. the snake must be long however! 
        pass