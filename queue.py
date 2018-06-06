"""Showcase of a very basic 2d platformer
The red girl sprite is taken from Sithjester's RMXP Resources:
http://untamed.wild-refuge.net/rmxpresources.php?characters
.. note:: The code of this example is a bit messy. If you adapt this to your 
    own code you might want to structure it a bit differently.
"""

__docformat__ = "reStructuredText"

import sys,math

import pygame
from pygame.locals import *
from pygame.color import *
    
import pymunk
from pymunk.vec2d import Vec2d
import pymunk.pygame_util 

import os

current_path = os.path.dirname(__file__)

def cpfclamp(f, min_, max_):
    """Clamp f between min and max"""
    return min(max(f, min_), max_)

def cpflerpconst(f1, f2, d):
    """Linearly interpolate from f1 to f2 by no more than d."""
    return f1 + cpfclamp(f2 - f1, -d, d)



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
    img = pygame.image.load(current_path + "/xmasgirl1.png")
    
    ### Physics stuff
    space = pymunk.Space()   
    space.gravity = 0, 0
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    # box walls 
    static = [pymunk.Segment(space.static_body, (10, 50), (300, 50), 30)
                , pymunk.Segment(space.static_body, (300, 50), (325, 50), 30)
                , pymunk.Segment(space.static_body, (325, 50), (350, 50), 30)
                , pymunk.Segment(space.static_body, (350, 50), (375, 50), 30)
                , pymunk.Segment(space.static_body, (375, 50), (680, 50), 30)
                , pymunk.Segment(space.static_body, (680, 50), (680, 370), 30)
                , pymunk.Segment(space.static_body, (680, 370), (10, 370), 30)
                , pymunk.Segment(space.static_body, (10, 370), (10, 50), 30)
                ]  
    static[1].color = pygame.color.THECOLORS['red']
    static[2].color = pygame.color.THECOLORS['green']
    static[3].color = pygame.color.THECOLORS['red']
    
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
    
    frame_number = 0
    
    
    # player
    body = pymunk.Body(1, pymunk.inf)
    body.position = 100,100
    
    
    feet = pymunk.Circle(body, 10, (0, 0))
    # Since we use the debug draw we need to hide these circles. To make it 
    # easy we just set their color to black.
    
    space.add(body, feet)


    
    while running:
            
        for event in pygame.event.get():
            if event.type == QUIT or \
                event.type == KEYDOWN and (event.key in [K_ESCAPE, K_q]):  
                running = False
            elif event.type == KEYDOWN and event.key == K_p:
                pygame.image.save(screen, "platformer.png")
                
        # Target horizontal velocity of player
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
        
        
        ### Clear screen
        screen.fill(pygame.color.THECOLORS["black"])
        
        
        ### Draw stuff
        space.debug_draw(draw_options)
        

        
        # Info and flip screen
        screen.blit(font.render("fps: " + str(clock.get_fps()), 1, THECOLORS["white"]), (0,0))
        screen.blit(font.render("Move with Left/Right, jump with Up, press again to double jump", 1, THECOLORS["darkgrey"]), (5,height - 35))
        screen.blit(font.render("Press ESC or Q to quit", 1, THECOLORS["darkgrey"]), (5,height - 20))
        
       
        pygame.display.flip()
        frame_number += 1
        
        ### Update physics
        
        space.step(dt)
        
        clock.tick(fps)

if __name__ == '__main__':
    sys.exit(main())