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
from pymunk.vec2d import Vec2d
import pymunk.pygame_util 

import os

current_path = os.path.dirname(__file__)
moves = [0,0,0,0] #left, rght, up, down
directions = list(itertools.product([-1,0,1], repeat=2))
PLAYER_VELOCITY = 10
def flipy(y):
    return -y+height

def cpfclamp(f, min_, max_):
    """Clamp f between min and max"""
    return min(max(f, min_), max_)

def cpflerpconst(f1, f2, d):
    """Linearly interpolate from f1 to f2 by no more than d."""
    return f1 + cpfclamp(f2 - f1, -d, d)

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

width, height = 690,400
fps = 60
dt = 1./fps
PLAYER_VELOCITY = 20



def main():

    ### PyGame init
    pygame.init()
    screen = pygame.display.set_mode((width,height)) 

    clock = pygame.time.Clock()
    running = True
    font = pygame.font.SysFont("Arial", 16)
    
    ### Physics stuff
    space = pymunk.Space()   
    space.gravity = 0, 0
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    # box walls 
    static = [pymunk.Segment(space.static_body, (10, 50), (300, 50), 10)
                , pymunk.Segment(space.static_body, (300, 50), (325, 50), 10)
                , pymunk.Segment(space.static_body, (325, 50), (350, 50), 10)
                , pymunk.Segment(space.static_body, (350, 50), (375, 50), 10)
                , pymunk.Segment(space.static_body, (375, 50), (680, 50), 10)
                , pymunk.Segment(space.static_body, (680, 50), (680, 370), 10)
                , pymunk.Segment(space.static_body, (680, 370), (10, 370), 10)
                , pymunk.Segment(space.static_body, (10, 370), (10, 50), 10)
                ]  
    
    # rounded shape
    rounded = [pymunk.Segment(space.static_body, (500, 50), (520, 60), 3)
                , pymunk.Segment(space.static_body, (520, 60), (540, 80), 3)
                , pymunk.Segment(space.static_body, (540, 80), (550, 100), 3)
                , pymunk.Segment(space.static_body, (550, 100), (550, 150), 3)
                ]
                
    # static platforms
    platforms = [pymunk.Segment(space.static_body, (170, 50), (270, 150), 3)
                , pymunk.Segment(space.static_body, (270, 100), (300, 100), 5)
                , pymunk.Segment(space.static_body, (400, 150), (450, 150), 3)
                , pymunk.Segment(space.static_body, (400, 200), (450, 200), 3)
                , pymunk.Segment(space.static_body, (220, 200), (300, 200), 3)
                , pymunk.Segment(space.static_body, (50, 250), (200, 250), 3)
                , pymunk.Segment(space.static_body, (10, 370), (50, 250), 3)
                ]
    
    for s in static + platforms+rounded:
        s.friction = 1.
        s.group = 1
    space.add(static, platforms+rounded)
    
    # player
    body_radius = 10
    body = pymunk.Body(1, pymunk.inf)
    body.position = 100,100
    feet = pymunk.Circle(body, body_radius, (0, 0))
    space.add(body, feet)

    def draw_ray(start, radius, thickness):
         ### Clear screen
        screen.fill(pygame.color.THECOLORS["black"])
        
        ### Draw stuff
        space.debug_draw(draw_options)

        for direction in directions:
            line_end = start + (direction[0]*(width/2), direction[1]*(height/2))
            line_start = start + (direction[0]*(radius + 0.5), direction[1]*(radius + 0.5))
            segment_q = space.segment_query_first(line_start, line_end, thickness, pymunk.ShapeFilter())
            if segment_q:
                contact_point = segment_q.point
                line = pymunk.Segment(space.static_body, line_start, contact_point, thickness)
                line.sensor = True
                line.body.position = 0,0
                line_length = math.sqrt((contact_point[0] - line_start[0])**2 + 
                                        (contact_point[1] - line_start[1])**2)
                print(line_length)

                p1 = line_start.x, flipy(line_start.y)
                p2 = contact_point.x, flipy(contact_point.y)
                pygame.draw.lines(screen, THECOLORS["green"], False, [p1, p2])


    frame_number = 0
    while running:
            
        for event in pygame.event.get():
            if event.type == QUIT or \
                event.type == KEYDOWN and (event.key in [K_ESCAPE, K_q]):  
                running = False
            elif event.type == KEYDOWN and event.key == K_p:
                pygame.image.save(screen, "platformer.png")

        
        draw_ray(body.position, 10, 0.2)

        moves = np.random.randint(0,2,(4,1))
        
        move(moves, body)
        
        target_vx = 0
        target_vy = 0

        keys = pygame.key.get_pressed()
        if (keys[K_LEFT]):
            target_vx -= PLAYER_VELOCITY
        if (keys[K_RIGHT]):
            target_vx += PLAYER_VELOCITY
        if (keys[K_DOWN]):
            target_vy -= PLAYER_VELOCITY
        if (keys[K_UP]):
            target_vy += PLAYER_VELOCITY

        body.velocity = target_vx, target_vy
        
        # Info and flip screen
        screen.blit(font.render("fps: " + str(clock.get_fps()), 1, THECOLORS["white"]), (0,0))
        pygame.display.flip()
        frame_number += 1
        ### Update physics
        
        space.step(dt)
        
        clock.tick(fps)


if __name__ == '__main__':
    sys.exit(main())