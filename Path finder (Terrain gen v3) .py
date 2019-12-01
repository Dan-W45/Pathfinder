import contextlib
with contextlib.redirect_stdout(None):      #Stops pyagame from displaying version number
    import pygame, random, os, sys, time, threading
    from pygame.locals import *
os.environ['SDL_VIDEO_CENTERED'] = '1'      #Opens pygame window in the center of the screen
pygame.init()                               #initialises the pygame window
g=pygame.display.set_mode([1250,700])       #sets the resolution to be 1250 x 700 pixels
pygame.display.set_caption("Path Finding")  #gives the pygame window the title "Path Finding"
clock=pygame.time.Clock()                   #allows for clock.tick() to be called later instead of pygame.time.Clock()
font=pygame.font.SysFont("Sans MS", 30)     #Sets the pygame default font size and style
display_fps = True                          #Can be set to true or false for displaying pygame window fps in the top right __Insert line number__
grid=[]                                     #Defines the array for later use
currentxy=[0,0]                             #Defines the array for later use
loop, is_looping = None, False              #Defines the variable loop so it the function find_path can be started and stopped, is_looping stops the function fuind_path being called more than once
re_gen = 0

def events():
    global is_looping
    for event in pygame.event.get():            ##Checking which keys have been pressed
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            if is_looping == True:
                loop.cancel()
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_r:
            return 1                            ##Force generates another map
        elif event.type == KEYDOWN and event.key == K_SPACE:
            return 2                            ##Runs the pathfinding algorithm
        elif event.type == KEYDOWN and event.key == K_e and is_looping == True:
            is_looping = False                  #is_looping boolean set to false so it can be called again
            loop.cancel()                       ##Stops pathfinding for debugging reasons

def gen_map():
    grid=[]
    for rows in range(14):          #14 is the height of the map in tiles
        row=[]                      #the array row is defined and cleared before appending to it
        for values in range(25):        #25 is the width of the map in tiles
            temp=[]                     #last array in the grid has to be cleared after it is stored in the array "row"
            temp.append(random.randint(100,255))        #appends a value to the 0 position of the temp array, this is the "height" value
            temp.append(0)                              #appends tha value 0 to the 1 position of the array, this is the colour value
            row.append(temp)                            #The temp array is appended to the row
        grid.append(row)                                #All rows are appended to the array grid
    return grid                         #returns the array so that it can be displayed

def find_path():
    global loop, re_gen
    try:
        grid[currentxy[0]][currentxy[1]][1]=1               #Sets colour of current square to blue
        grid[currentxy[0]][currentxy[1]+1][1]=2             #Sets colour of the square to the right to indicate checking
        grid[currentxy[0]+1][currentxy[1]][1]=2             #Sets colour of the square below to yellow to indicate checking
        if grid[currentxy[0]][currentxy[1]+1][0] > grid[currentxy[0]+1][currentxy[1]][0]:   #Compares the values of the squares below and to the right picking the highest value
            grid[currentxy[0]-1][currentxy[1]+1][1]=0
            grid[currentxy[0]+1][currentxy[1]-1][1]=0           #Reverts both of the previously yellow squares to green
            currentxy[1]+=1
        else:
            grid[currentxy[0]-1][currentxy[1]+1][1]=0
            grid[currentxy[0]+1][currentxy[1]-1][1]=0
            currentxy[0]+=1
    except:
        re_gen = 1                              #Once the end of the grid has been reached it will generate another grid and start again
    loop = threading.Timer(0.2, find_path)      #Assigns is function to another thread so that it can run at a differnet "speed" to the rest of the code
    loop.start()


def draw():
    pygame.draw.rect(g, (80,80,80), [0,0,1280,720],0)       #No longer necessary but sets the background colour (behind the tiles) to be grey
    for row in range(len(grid)):
        for column in range(len(grid[0])):                  #For loops generate numbers to check every value in the array grid for displaying
            if grid[row][column][1] == 0:                   #If the colour identifier value is 0, it should be displayed as green
                pygame.draw.rect(g, (0,grid[row][column][0],0), [column*50, row*50, 50,50],0)
            elif grid[row][column][1] == 1:                 #1 is for a blue ish color for the path
                pygame.draw.rect(g, (0,grid[row][column][0],grid[row][column][0]), [column*50, row*50, 50,50],0)
            elif grid[row][column][1] == 2:                 #and 2 is for yellow which is the squares it is compring
                pygame.draw.rect(g, (grid[row][column][0],grid[row][column][0],0), [column*50, row*50, 50,50],0)
            height = font.render(str(grid[row][column][0]), True, pygame.Color('black'))        #variable 'height' is set to the value of the square
            g.blit(height, (column*50, (row*50)+30))                                            #The 'height' value of the square is displayed inside the appropriate square
    if display_fps == True:
        text = font.render(str(int(clock.get_fps()))+" FPS", True, pygame.Color('red'))         #displayes the frames per second or simulation speed
        g.blit(text, (0,0))
    pygame.display.flip()       #Draws everything on the canvas so the user can see

grid = gen_map()        #Generates the first map so that the user does not have to

while True:     ##Main loop of the program, everything is called from within
    clock.tick()   
    choice = events()       #sets variable 'choice' to be what fuinction 'events()' returns (users inputs) 
    if re_gen == 1:
        currentxy=[0,0]     #resets the start position back to the top right, [0,0]
        grid = gen_map()    #sets the 'grid' boolean to be the new generated map
        re_gen = 0          #resets variable 're_gen' to 0 so it can be reused and does not cause an infinite loop
    if choice == 1:
        currentxy=[0,0]     #resets the start position back to the top right, [0,0]
        grid = gen_map()    #sets the 'grid' boolean to be the new generated map
    elif choice == 2 and is_looping == False:   #'is_looping' has to be false so that the function cannot be run multiple times
        is_looping = True   #Sets the 'is_looping' boolean to True to reduce the chance of a crash when stopping the function
        find_path()         #When the user selects the option the function to find a path is called
    draw()                  #Calls the 'draw()' function which displays the grid to the user
















