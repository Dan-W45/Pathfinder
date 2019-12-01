import contextlib
with contextlib.redirect_stdout(None):
    import pygame, random, os, sys, time, threading
    from pygame.locals import *

##os.environ['SDL_VIDEO_CENTERED'] = '1'
os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
pygame.init()

width, height = 1920, 1080
loop, is_looping = None, False
find, finding = None, False
print(width,height)
##res=pygame.display.list_modes()
##width,height=res[0][0],res[0][1]
##print(width,height)



g=pygame.display.set_mode([width,height])##,pygame.FULLSCREEN)
pygame.display.set_caption("Path Finder")
clock=pygame.time.Clock()
font=pygame.font.SysFont("Sans MS", 20)
grid=[]
bias=[0,1,1]

print(len(grid))

def events():
    global is_looping, loop, finding, find
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            if finding == True:
                find.cancel()
            if is_looping==True:
                loop.cancel()
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_1:
            ##Re generate the grid
            return 1
        elif event.type == KEYDOWN and event.key == K_2:
            ##Place markers
            return 2
        elif event.type == KEYDOWN and event.key == K_3 and is_looping == False:
            ##Solve the map
            is_looping = True
            return 3
        elif event.type == KEYDOWN and event.key == K_4 and is_looping == True:
            is_looping = False
            loop.cancel()
        elif event.type == KEYDOWN and event.key == K_SPACE and finding == False:
            return 4

def genmap():
    global grid, highest
    highest = 0
    grid=[]
    for rows in range(int((height/20)+1)):
        row=[]
        for columns in range(int((width/20))):
            column=[]
            column.append(random.choice(bias)*150)  #Height
            column.append(1)                        #Colour
            column.append(-1)                       #Discovered/distance from start
            row.append(column)
        row.append([0,1,-1])
        grid.append(row)
    grid[int(len(grid)/2)][int(len(grid[0])/2)][0] = 150
    row=[]
    for i in range(int((width/20))+1):
        temp=[]
        temp.append(0)
        temp.append(1)
        temp.append(-1)
        row.append(temp)
    grid.append(row)

def genpos():
    ## Generate the start and end pos for the algorithm to solve
    global grid, startx, starty, endx, endy
    startx = random.randint(0,int(height/20)-1)
    starty = random.randint(0,int(width/20)-1)
    endx = random.randint(0,int(height/20)-1)
    endy = random.randint(0,int(width/20)-1)
    print(startx, starty, endx, endy)
    grid[startx][starty][0] = 150
    grid[startx][starty][1] = 2
    grid[startx][starty][2]=0
    grid[endx][endy][0] = 150
    grid[endx][endy][1] = 4


def explore():
    global grid, startx, starty, endx, endy, highest, loop, is_looping
    loop = threading.Timer(0.02, explore)      #Assigns is function to another thread so that it can run at a differnet "speed" to the rest of the code
    grid[startx][starty][1]=2
    grid[startx][starty][2]=0
    grid[endx][endy][1] = 4
    highest += 1
    for row in range(len(grid)-1):
        for column in range(len(grid[0])-1):
            if grid[row][column][2] == highest-1 and grid[row][column][0] == 150:
                if grid[row+1][column][0] == 150 and grid[row+1][column][2] == -1:
                    grid[row+1][column][2] = highest
                    grid[row+1][column][1] = 0
                if grid[row-1][column][0] == 150 and grid[row-1][column][2] == -1:
                    grid[row-1][column][2] = highest
                    grid[row-1][column][1] = 0
                if grid[row][column-1][0] == 150 and grid[row][column-1][2] == -1:
                    grid[row][column-1][2] = highest
                    grid[row][column-1][1] = 0
                if grid[row][column+1][0] == 150 and grid[row][column+1][2] == -1:
                    grid[row][column+1][2] = highest
                    grid[row][column+1][1] = 0
                if grid[row][column][1]==4:
                    print('End found')
                    is_looping = False
                    loop.cancel()
    loop.start()


def findpath():
    global highest, grid, find, finding
    find = threading.Timer(0.02, findpath)      #Assigns is function to another thread so that it can run at a differnet "speed" to the rest of the code
    highest-=1
    for row in range(len(grid)-1):
        for column in range(len(grid[0])-1):
            if grid[row][column][2] == highest+1 and grid[row][column][0] == 150:
                if grid[row+1][column][0] == 150 and grid[row+1][column][2] == highest and (grid[row+1][column][1] == 4 or grid[row-1][column][1] == 4 or grid[row][column+1][1] == 4 or grid[row][column-1][1] == 4):
                    grid[row][column][1] = 4
                if grid[row-1][column][0] == 150 and grid[row-1][column][2] == highest and (grid[row+1][column][1] == 4 or grid[row-1][column][1] == 4 or grid[row][column+1][1] == 4 or grid[row][column-1][1] == 4):
                    grid[row][column][1] = 4
                if grid[row][column-1][0] == 150 and grid[row][column-1][2] == highest and (grid[row+1][column][1] == 4 or grid[row-1][column][1] == 4 or grid[row][column+1][1] == 4 or grid[row][column-1][1] == 4):
                    grid[row][column][1] = 4
                if grid[row][column+1][0] == 150 and grid[row][column+1][2] == highest and (grid[row+1][column][1] == 4 or grid[row-1][column][1] == 4 or grid[row][column+1][1] == 4 or grid[row][column-1][1] == 4):
                    grid[row][column][1] = 4
    if highest <= 0:
        finding = False
        find.cancel()
    find.start()


def draw():
    global grid
    clock.tick()
##    pygame.draw.rect(g,(80,80,80), [0,0,width,height],0)
    for row in range(len(grid)):
        for column in range(len(grid[0])):
            if grid[row][column][1] == 0:
                pygame.draw.rect(g, (0,(grid[row][column][0]),0), [column*20, row*20, 20,20],0)
            elif grid[row][column][1] == 1:
                pygame.draw.rect(g, (0,grid[row][column][0],grid[row][column][0]), [column*20, row*20, 20,20],0)
            elif grid[row][column][1] == 2:
                pygame.draw.rect(g, (grid[row][column][0],0,grid[row][column][0]), [column*20, row*20, 20,20],0)
            elif grid[row][column][1] == 3:
                pygame.draw.rect(g, (grid[row][column][0],0,0), [column*20, row*20, 20,20],0)
            elif grid[row][column][1] == 4:
                pygame.draw.rect(g, (grid[row][column][0],grid[row][column][0],0), [column*20, row*20, 20,20],0)
##            if grid[row][column][2] != -1:
##                height = font.render(str(grid[row][column][2]), True, pygame.Color('gray'))
##                g.blit(height, (column*20, (row*20)+5))
    text = font.render(str(int(clock.get_fps()))+" FPS", True, pygame.Color('red'))
    g.blit(text, (0,0))
    pygame.display.flip()

genmap()
while True:
    value = events()
    if value == 1:
        genmap()
    elif value == 2:
        genpos()
    elif value == 3:
        is_looping = True
        explore()
    elif value == 4:
        finding = True
        findpath()
    draw()
