import contextlib
with contextlib.redirect_stdout(None):
    import pygame, random, os, sys, time, threading
    from pygame.locals import *

pygame.init()
font20=pygame.font.SysFont("Sans MS", 20)
g=pygame.display.set_mode([1280,720])
clock = pygame.time.Clock()

def events():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

def draw():
    clock.tick()
    fps = font20.render(str(int(clock.get_fps()))+" FPS", True, pygame.Color('Red'))
    g.blit(fps, [0,0])
    pygame.display.flip()


while True:
    g.fill([80,80,80])
    pygame.draw.line(g,[0,255,0],[50,50],[250,250],5)
    events()
    draw()
