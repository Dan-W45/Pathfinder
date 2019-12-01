import pygame,sys
from pygame.locals import *
screen=pygame.display.set_mode((1000,700))
pygame.init()
clock = pygame.time.Clock()
tx,ty=250,250
while True :
    for event in pygame.event.get():
        if event.type==QUIT :
                    pygame.quit()
                    sys.exit()
        if event.type== pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse=pygame.mouse.get_pos()
            if mouse[0]in range ( tx,tx+130) and  mouse[1]in range ( ty,ty+20):
                print (" you press the text ")
    pygame.draw.rect(screen,(0,0,255),[tx,ty,130,20])
    myfont = pygame.font.SysFont("Marlett",35)
    textsurface = myfont.render(("Start game"), True, (230,230,230))
    screen.blit(textsurface,(tx,ty))
    pygame.display.update()
    clock.tick(60)
