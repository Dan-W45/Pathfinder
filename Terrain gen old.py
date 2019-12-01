import contextlib
with contextlib.redirect_stdout(None):
    import pygame, random, os, sys, ast, time
    from pygame.locals import *

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
g=pygame.display.set_mode([1280,720])
pygame.display.set_caption("Terrain Generator")
clock=pygame.time.Clock()
font=pygame.font.SysFont("Sans MS", 30)
display_fps = True

grid=[]

def events():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_r:
            return 1

def genrow():
    row=[]
    for rows in range(16):
        row.append(random.randint(0,255))
    return row

for columns in range(9):
    column=genrow()
    grid.append(column)
print(grid)

while True:
    if events() == 1:
        grid=[]
        for columns in range(9):
            column=genrow()
            grid.append(column)
    clock.tick()
    pygame.draw.rect(g, (80,80,80), [0,0,1280,720],0)
    for row in range(len(grid)):
        for column in range(len(grid[0])):
            pygame.draw.rect(g, (0,grid[row][column],grid[row][column]), [column*50, row*50, 50,50],0)
            height = font.render(str(grid[row][column]), True, pygame.Color('gray'))
            g.blit(height, (column*50, (row*50)+30))
    if display_fps == True:
        text = font.render(str(int(clock.get_fps()))+" FPS", True, pygame.Color('green'))
        g.blit(text, (0,0))    
    pygame.display.flip()
