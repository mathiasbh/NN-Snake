#!/usr/bin/env bash

import itertools
import numpy as np
from time import sleep

from snake import Snake
from boundary import Boundary
from point import Point
from random import choice, randrange


pxsize = 20
off = 15


class SnakeGame(object):
    """docstring for main"""
    def __init__(self, player=False, render=False, width=400, height=400, FPS=30, distance_option="simple"):
        super(SnakeGame, self).__init__()
        
        self.width = width
        self.height = height

        # Initialize objects
        self.snake = Snake((self.width - pxsize)/2 - off, (self.height - pxsize)/2 - off, pxsize, off)
        self.point = Point(randrange(off + pxsize, self.width - off, pxsize), randrange(off + pxsize, self.height - off, pxsize), pxsize)
        self.board = np.zeros([int((self.height-off)/pxsize), int((self.width-off)/pxsize)])

        self.walls = []
        self.walls.append(Boundary(off, off, off, self.height-off))
        self.walls.append(Boundary(off, off, self.width-off, off))
        self.walls.append(Boundary(self.width-off, off, self.width-off, self.height-off))
        self.walls.append(Boundary(off, self.height-off, self.width-off, self.height-off))

        self.minsteps = 100 # if this reaches 0, the snake dies. 
        self.score = 0
        self.steps = 0
        self.fitness = 0

        self.running = True
        self.render = render
        self.player = player
        self.FPS = FPS
        self.distance_option = distance_option
        
  
        if self.render:
            import pyglet
            self.win = pyglet.window.Window(width=self.width, height=self.height, fullscreen = False)
            self.win.set_caption('Snake neural network')
            self.win.set_location(400,400)
            self.key = pyglet.window.key
            self.on_key_press = self.win.event(self.on_key_press)
            self.label = pyglet.text.Label('Score: 0', x=self.width//2, y=self.height*3//4, font_size=12, anchor_x="center")


    def reset(self):
        self.__init__(player=self.player, render=self.render, width=self.width, height=self.height, FPS=self.FPS, distance_option=self.distance_option)

    def set_fitness(self, new_fitness):
        self.fitness = new_fitness
        
    def set_score(self, new_score):
        self.score = new_score
        
    def set_steps(self, new_steps):
        self.steps = new_steps

    def on_key_press(self, symbol, modifiers):
        if symbol == self.key.ESCAPE:
            self.running = False
        if (symbol == self.key.LEFT) and self.player:
            self.snake.update_dir('lt')
        if (symbol == self.key.RIGHT) and self.player:
            self.snake.update_dir('rt')


    def model_turn(self, direction):
        if direction == 0:
            self.snake.update_dir('lt')
        if direction == 2:
            self.snake.update_dir('rt')


    def draw_game(self):
        self.win.clear()
        self.snake.show()
        self.point.show()
        
        self.label.text = 'Score: ' + str(self.score)
        self.label.draw()
        
        
        for wall in self.walls:
            wall.show()

        self.win.flip()


    def generate_point(self):      
        exclude = []
        exclude.append((self.snake.x, self.snake.y))
        for segment in self.snake.segments:
            exclude.append((segment.x, segment.y))

        x = range(off + pxsize, self.width - off, pxsize)
        y = range(off + pxsize, self.height - off, pxsize)
        
        # Find all open spaces for point
        openspace = [i for i in list(itertools.product(x, y)) if i not in exclude]
        
        if openspace:
            loc = choice(openspace)
            self.point.update_pos(loc[0], loc[1])
        else:
            print("You win!")


    def collision(self):
        if self.snake.collision_snake():
            self.minsteps = -1
            if self.player:
                self.steps = 0
                self.score = 0
            self.snake = Snake((self.width - pxsize)/2 - off, (self.height - pxsize)/2 - off, pxsize, off)

        if self.snake.collision_point(self.point):
            self.score += 1
            if self.minsteps > 400:
                self.minsteps = 500
            else:
                self.minsteps += 100
            self.generate_point()
            self.snake.add_segment(self.snake.x, self.snake.y, self.snake.len)

        for wall in self.walls:
            if self.snake.collision_wall(wall, off, self.width, self.height):
                self.minsteps = -1
                if self.player:
                    self.steps = 0
                    self.score = 0
                self.snake = Snake((self.width - pxsize)/2 - off, (self.height - pxsize)/2 - off, pxsize, off)



    def vision(self):
        return(self.snake.snake_vision(self.walls, self.point, self.width, self.height, pxsize, distance_option=self.distance_option))


    def calculate_fitness(self, ):
        if self.score < 10:
            self.fitness = self.steps * self.steps * (2**(self.score)) / 10000 + 2*self.score
        else:
            self.fitness = self.steps * self.steps * (2**(10)) * (self.score - 9) / 10000 + 2*self.score
        


    def run(self, direction=None):
        self.snake.update_pos()
        self.collision()
        self.steps += 1
        self.minsteps -= 1

        if not self.player:
            self.model_turn(direction)
        
        if self.render:
            self.win.dispatch_events()
            self.draw_game()
            sleep(1./self.FPS)


                
if (__name__ == "__main__"):
    # execute only if run as a script
    x = SnakeGame(player=True, render=True, FPS=10)

 
    while x.running:
        x.run()
        print(x.vision())
        

