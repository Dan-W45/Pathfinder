import contextlib
with contextlib.redirect_stdout(None):
    import pygame, random, os, sys, time, threading
    from pygame.locals import *

width, height = 320, 180
#width, height = 1600, 900
pygame.init()

font20 = pygame.font.SysFont('input', 20)
font60 = pygame.font.SysFont('input', 20)   ##CHANGE BACK TO 60##

class Menu:
    def __init__(self, selected):
        #print(width, height)
        if selected == 1:
            self.menu = 'Main'
    def change_menu(self, selected=1):
        if selected == 1:
            self.menu = 'Main'
        elif selected == 2:
            self.menu = 'Options'
    def main_menu(self):
        self.menu = 'Main'

        screen_rect = g.get_rect()
        
        title=font60.render('Path finder', True, pygame.Color('Cyan'))
        titleloc=title.get_rect()
        titleloc.center=screen_rect.center[0],(height/10)*1

        g.blit(title, titleloc)



def __init__():
    global height, width, clock, g
    g=pygame.display.set_mode([width, height])
    clock=pygame.time.Clock()

def events():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

__init__()


show_menu = Menu(1)

show_menu.main_menu()
print(str(show_menu.menu))

##show_menu.change_menu(2)
##print(str(show_menu.menu))

show_menu.main_menu()



while True:
    events()
    clock.tick(60)
    g.fill(pygame.Color('grey20'))
    FPS = font20.render(str(int(clock.get_fps()))+" FPS", True, pygame.Color('Red'))
    g.blit(FPS, (0,0))
    show_menu.main_menu()
    pygame.display.flip()
