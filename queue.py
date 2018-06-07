"""
The idea is to teach neural network to form a queue in order to exit 
the room in the fastest manner. Hope is that instead of all rushing towards the exit,
bots will form a line and exit in an orderly manner.
"""

__docformat__ = "reStructuredText"

import sys,math
import itertools
import pygame
from pygame.locals import *
from pygame.color import *
import numpy as np
import pymunk
from PIL import Image
from pymunk.vec2d import Vec2d
import pymunk.pygame_util 
import os
import skimage as sk
from skimage import color as skcolor

current_path = os.path.dirname(__file__)
moves = [0,0,0,0] #left, rght, up, down
directions = list(itertools.product([-1,0,1], repeat=2))
PLAYER_VELOCITY = 20
width, height = 28, 28
hole_width = 8
fps = 120
dt = 1./fps

def flipy(y):
    return -y+height

def move(moves, body):

        target_vx = 0
        target_vy = 0

        if (moves[0] == 1):
            target_vx -= PLAYER_VELOCITY
        if (moves[1] == 1):
            target_vx += PLAYER_VELOCITY
        if (moves[2] == 1):
            target_vy -= PLAYER_VELOCITY
        if (moves[3] == 1):
            target_vy += PLAYER_VELOCITY

        body.velocity = target_vx, target_vy

def main():

    ### PyGame init
    pygame.init()
    screen = pygame.display.set_mode((width,height)) 
    frame_number = 0
    clock = pygame.time.Clock()
    running = True
    
    ### Physics stuff
    space = pymunk.Space()   
    space.gravity = 0, 0
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    hole_location = np.random.random_integers(1,18)
    # box walls 
    static = [pymunk.Segment(space.static_body, (0, 0), (width, 0), 2),
              pymunk.Segment(space.static_body, (0, 0), (0, height), 1),
              pymunk.Segment(space.static_body, (width, 0), (width, height), 2),
              pymunk.Segment(space.static_body, (0, height), (hole_location, height), 1),
              pymunk.Segment(space.static_body, (hole_location+hole_width, height), (width, height), 1)
                ]  
    
    for s in static:
        s.friction = 1.
        s.group = 1
    space.add(static)

    # player
    body_radius = 2
    body = pymunk.Body(1, pymunk.inf)
    body.position = np.random.random_integers(2, 16, (2, 1))
    feet = pymunk.Circle(body, body_radius, (0, 0))
    space.add(body, feet)

    while running:
            
        for event in pygame.event.get():
            if event.type == QUIT or \
                event.type == KEYDOWN and (event.key in [K_ESCAPE, K_q]):  
                running = False
            elif event.type == KEYDOWN and event.key == K_p:
                img = pygame.image.tostring(screen, 'RGB')
                img = Image.frombytes('RGB', (width, height), img)
                original = sk.img_as_float(img)
                original = skcolor.rgb2gray(original)
                original = original.flatten()
                print(original.shape)
                
        ### Clear screen
        screen.fill(pygame.color.THECOLORS["black"])
            
        ### Draw stuff
        space.debug_draw(draw_options)

        ### Move
        moves = np.random.randint(0,2,(4,1))
        move(moves, body)
        
        # Info and flip screen
        pygame.display.flip()
        frame_number += 1

        ### Update physics
        space.step(dt)
        clock.tick(fps)

        #if body.position[1] > height/4:
        #    return frame_number


if __name__ == '__main__':
    sys.exit(main())