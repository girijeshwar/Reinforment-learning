import numpy as np
import pygame
from enum import Enum
import random
from collections import namedtuple

pygame.init()


font= pygame.font.SysFont("arial", 25)

class Direction(Enum):
    RIGHT=1
    LEFT=2
    UP=3
    DOWN=4


Point= namedtuple("Point","x, y")
WHITE = (255,255,255)
RED =(200,0,0)
BLUE1 =(0,0,255)
BLUE2 =(0,100,255)
BLACK =(0,0,0)

Block_size =20
speed =40
class SnakeGamesAI:

    def __init__(self,w=640, h=480):
        self.w=w
        self.h=h

        self.display= pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake Game")
        self.clock=pygame.time.Clock()
        self.reset()
        
    def reset(self):
        self.direction=Direction.RIGHT

        self.head= Point(self.w/2, self.h/2)
        self.snake= [self.head, 
                    Point(self.head.x-Block_size, self.head.y),
                    Point(self.head.x-(2*Block_size), self.head.y)]   

        self.score=0
        self.food=None
        self._place_food()
        self.frame_iteration = 0


    def _place_food(self):
        x=random.randint(0, (self.w-Block_size) //Block_size )*Block_size
        y=random.randint(0, (self.h-Block_size) //Block_size )*Block_size
        self.food=Point(x,y)
        if self.food in self.snake:
            self._place_food()
    


    def play_step(self, action):
        self.frame_iteration += 1

        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                pygame.quit()
                quit()
           

        self._move(action)
        self.snake.insert(0, self.head)


        reward = 0
        game_over=False
        if self.is_collison() or self.frame_iteration > 100 * len(self.snake):
            game_over=True
            reward = -10
            return reward, game_over, self.score

        if self.head==self.food:
            self.score +=1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        #5 uI
        self._update_ui()
        self.clock.tick(speed)

        # game_over=False
        return reward, game_over, self.score
        
    def is_collison(self, pt=None):
        if pt is None:
            pt= self.head
        if pt.x > self.w - Block_size or pt.x < 0 or pt.y > self.h -Block_size or pt.y < 0:
            return True
        if pt in self.snake[1:]:
            return True
        
        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, Block_size, Block_size))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12,12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, Block_size, Block_size))

        text= font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0,0])
        pygame.display.flip()


    def _move(self, action):
        #[ straight, right, left]
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx= clock_wise.index(self.direction)
        if np.array_equal(action, [1,0,0]):
            new_dir = clock_wise[idx] #straight
        elif np.array_equal(action, [0,1,0]):# right direction
            next_idx= (idx + 1)% 4
            new_dir = clock_wise[next_idx]
        else:
            next_idx= (idx - 1)% 4 
            new_dir = clock_wise[next_idx]

        self.direction = new_dir

        x= self.head.x
        y=self.head.y

        if self.direction ==Direction.RIGHT:
            x += Block_size
        elif self.direction == Direction.LEFT:
            x -= Block_size
        elif self.direction == Direction.DOWN:
            y += Block_size
        elif self.direction == Direction.UP:
            y -= Block_size
        
        
        
        self.head= Point(x, y)
