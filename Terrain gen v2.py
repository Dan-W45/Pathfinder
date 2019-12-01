import contextlib
with contextlib.redirect_stdout(None):
    import pygame, random, os, sys, ast, time
    from pygame.locals import *
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
g=pygame.display.set_mode([1250,700])
pygame.display.set_caption("Path finding")
clock=pygame.time.Clock()
font=pygame.font.SysFont("Sans MS", 30)
##display_fps = True
grid=[]
currentxy=[0,0]


def events():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == event.type == KEYDOWN and event.key == K_r:
            return 1
        elif event.type == event.type == KEYDOWN and event.key == K_c:
            return 2

def check(currentxy):
    #Start at [0,0], then move towards bottom right checking for the highest value tile below and
    #to the right of the current tile.
##    print('current '+str(grid[currentxy[0]][currentxy[1]][0]))
##    print('to the right '+str(grid[currentxy[0]][currentxy[1]+1][0]))
##    print('below '+str(grid[currentxy[0]+1][currentxy[1]][0]))
    try:
        grid[currentxy[0]][currentxy[1]][1]=1
        grid[currentxy[0]][currentxy[1]+1][1]=2
        grid[currentxy[0]+1][currentxy[1]][1]=2
        draw(grid)
        time.sleep(0.5)
        if grid[currentxy[0]][currentxy[1]+1][0] > grid[currentxy[0]+1][currentxy[1]][0]:
            grid[currentxy[0]][currentxy[1]+1][1]=0
            grid[currentxy[0]+1][currentxy[1]][1]=0
            currentxy[1]+=1
        else:
            grid[currentxy[0]][currentxy[1]+1][1]=0
            grid[currentxy[0]+1][currentxy[1]][1]=0
            currentxy[0]+=1
    except:
        print('end')
        time.sleep(2)
        return 5
    return currentxy
    



def genrow():
    row=[]
    for values in range(25):
        temp=[]
        temp.append(random.randint(100,255))
        temp.append(0)
        row.append(temp)
    return row

for columns in range(14):
    column=genrow()
    grid.append(column)


def draw(grid):
##    pygame.draw.rect(g, (80,80,80), [0,0,1280,720],0)
    for row in range(len(grid)):
        for column in range(len(grid[0])):
            if grid[row][column][1] == 0:
                pygame.draw.rect(g, (0,grid[row][column][0],0), [column*50, row*50, 50,50],0)
            elif grid[row][column][1] == 1:
                pygame.draw.rect(g, (0,grid[row][column][0],grid[row][column][0]), [column*50, row*50, 50,50],0)
            elif grid[row][column][1] == 2:
                pygame.draw.rect(g, (grid[row][column][0],grid[row][column][0],0), [column*50, row*50, 50,50],0)
            height = font.render(str(grid[row][column][0]), True, pygame.Color('black'))
            g.blit(height, (column*50, (row*50)+30))
##    text = font.render(str(int(clock.get_fps()))+" FPS", True, pygame.Color('red'))
##    g.blit(text, (0,0)) 
    pygame.display.flip()

while True:
    choice = events()
    value = check(currentxy)
    if value == 5:
        choice = 1
    if choice == 1:
        grid=[]
        currentxy=[0,0]
        for columns in range(14):
            column=genrow()
            grid.append(column)
    elif choice == 2 and grid[0][0][1]==0:
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                grid[x][y][1]=1
    elif choice == 2 and grid[0][0][1]==1:
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                grid[x][y][1]=0
    clock.tick()












