import contextlib
with contextlib.redirect_stdout(None):
    import pygame, random, os, sys, time, threading
    from pygame.locals import *
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
g=pygame.display.set_mode([1280,720])
pygame.display.set_caption("Path Finder")
clock=pygame.time.Clock()
font=pygame.font.SysFont("Sans MS", 20)
loop, is_looping = None, False              #Defines the variable loop so it the function find_path can be started and stopped, is_looping stops the function fuind_path being called more than once
rerun, is_regen = None, False
grid=[]
bias=[0,1,1]

def events():
    global is_looping, is_regen
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            if is_looping==True:
                loop.cancel()
            if is_regen==True:
                rerun.cancel()
            pygame.quit()
            sys.exit()
        elif event.type == event.type == KEYDOWN and event.key == K_r:
            return 1
        elif event.type == event.type == KEYDOWN and event.key == K_SPACE:
            return 2
        elif event.type == event.type == KEYDOWN and event.key == K_f and is_regen == False:
            return 3
        elif event.type == event.type == KEYDOWN and event.key == K_v and is_regen == True:
            rerun.cancel()
            is_regen = False
        elif event.type == event.type == KEYDOWN and event.key == K_e and is_looping == True:
            is_looping = False                  #is_looping boolean set to false so it can be called again
            loop.cancel()

def genmap():           #GENERATE A PROPER MAP/MAZE THAT CAN BE COMPLETED.
    global grid, highest
    highest = 0
    grid=[]
    for rows in range(36):
        row=[]
        for values in range(65):
            temp=[]
            temp.append(random.choice(bias)*150)    #Choosing from a bias list so that more of the map is open
            temp.append(1)                          #index 1 is display colour
            temp.append(-1)                         #index 2 is for pathfinding only
            row.append(temp)
        row.append([0,1,-1])
        grid.append(row)
    grid[int(len(grid)/2)][int(len(grid[0])/2)][0] = 150
    row=[]
    for i in range(130):
        temp=[]
        temp.append(0)
        temp.append(1)
        temp.append(-1)
        row.append(temp)
    grid.append(row)
    
def find_mid():
    print(int(len(grid)/2))
    print(int(len(grid[0])/2))

def find_path():
    global grid, highest, loop, value
    try:
        grid[int(len(grid)/2)][int(len(grid[0])/2)][1]=0
        grid[int(len(grid)/2)][int(len(grid[0])/2)][2]=0
        highest+=1
        for row in range(len(grid)):
            for column in range(len(grid[0])):
                if grid[row][column][2] == highest-1 and grid[row][column][0] == 150:
                    if grid[row+1][column][0] == 150 and grid[row+1][column][2] == -1:
                        grid[row+1][column][2] = highest
                        grid[row+1][column][1]=0
                    if grid[row-1][column][0] == 150 and grid[row-1][column][2] == -1:
                        grid[row-1][column][2] = highest
                        grid[row-1][column][1]=0
                    if grid[row][column-1][0] == 150 and grid[row][column-1][2] == -1:
                        grid[row][column-1][2] = highest
                        grid[row][column-1][1]=0
                    if grid[row][column+1][0] == 150 and grid[row][column+1][2] == -1:
                        grid[row][column+1][2] = highest
                        grid[row][column+1][1]=0
    except:
        value=1
    loop = threading.Timer(0.00, find_path)      #Assigns is function to another thread so that it can run at a differnet "speed" to the rest of the code
    loop.start()

def helper():
    global rerun
    genmap()
    rerun = threading.Timer(0.2, helper)      #Assigns is function to another thread so that it can run at a differnet "speed" to the rest of the code
    rerun.start()


def draw():
    try:
        clock.tick()
        pygame.draw.rect(g, (150,150,150), [0,0,1920,1080],0)
        for row in range(len(grid)):
            for column in range(len(grid[0])):
                if grid[row][column][1] == 0:
                    pygame.draw.rect(g, (0,(grid[row][column][0]),0), [column*20, row*20, 20,20],0)
                elif grid[row][column][1] == 1:
                    pygame.draw.rect(g, (0,grid[row][column][0],grid[row][column][0]), [column*20, row*20, 20,20],0)
                if grid[row][column][2] != -1:
                    height = font.render(str(grid[row][column][2]), True, pygame.Color('gray'))
                    g.blit(height, (column*20, (row*20)+5))
        pygame.display.flip()
    except Exception as e:
        print(row, column, e)
##        pygame.quit()
##        sys.exit()
        pygame.draw.rect(g, (255,0,0), [column*20, row*20, 20,20],0)
        pygame.display.flip()
        print(grid[row][column])
        time.sleep(10)
genmap()
draw()
while True:
    value = events()
    draw()
    if value == 1:
        genmap()
    if value == 2 and is_looping == False:
        is_looping = True   #Sets the 'is_looping' boolean to True to reduce the chance of a crash when stopping the function
        find_path()         #When the user selects the option the function to find a path is called
    if value == 3 and is_regen == False:
        is_regen = True
        helper()
















