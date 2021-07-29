# Cursed Snake Game

Snake game where you are now the food and there are multiple snakes out there to eat you! A twist to the original Snake game.

As a food, you have the ability to move unrestricted with diagonal directions along with a sprint ability. The snakes however retain their block by block movements, and mostly 
have the same behavior as the original snake game. However, snakes cannot accidentally kill themselves by running into their own body or another snake's body. If snakes are so
flexible and can roll up like a hose, they can do that in this game! The food can roam around and pickup power-ups that randomly spawn. (note that their is a time limit before 
they disappear) There are three power-ups as follow: sprint boost, poison food, food ejecter. Sprint boost is exactly what it means. Poison food turns your food into poison, so 
if a snake eats you, they'll die instead. Food ejecter is a one-time ability for your food to eject a projectile that will kill a snake granted it hits their head. 

## Menu 
Ability to choose how many snakes appear, their speed, and your choice of food.

<img src="https://i.imgur.com/NFsUFVx.jpg" width="600" />

## Gameplay & Snake AI
Each snake has a different AI powering its movement. The combination of all AI's allow snakes to essentially area deny, block, and attack the food from all directions.
There are five types of AI as follows:
1) Aggressive Attacker - takes the shortest path to eat the food
2) Flanker - moves into a random position away from the food before going in for the kill
3) Cut-Off - always matches either the food's x or y values before moving in a beeline towards the food 
4) Patroller - patrols a random region for a set amount of moves before moving to the next, if the food gets close enough to the snake, the snake will forfeit its patrol to 
pursue the snake
5) Circler - give to the shortest and longest snake to circle around the center or outer edges of the window. This essentially serves as a wall for the food. Like the patroller,
if the food comes into distance with the head of the snake, it will forfeit its run to pursue the snake.
<img src="https://i.imgur.com/HlM2DDf.jpg" width="600" />
<img src="https://i.imgur.com/KvMhrbt.jpg" width="600" />
