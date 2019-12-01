import contextlib
with contextlib.redirect_stdout(None):
    import pygame, random, os, sys, time, threading
    from pygame.locals import *

os.environ['SDL_VIDEO_CENTERED'] = '1'
##os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
width, height = 1600, 900
##width, height = 1920, 1080
pygame.init()
#print(pygame.font.get_fonts())
font20=pygame.font.SysFont("input", 20)
font60=pygame.font.SysFont("input", 60)
pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=4096)
bhover=pygame.mixer.Sound("button hover.wav")
bclick=pygame.mixer.Sound("button click.wav")


loop, is_looping = None, False
find, finding = None, False

grid=[]
bias=[0,1,1]
scale = 50
colours=[255,0,0]
speed = 5
minimap=False
RGBcycle=False


vertical,horizontal=0,0
moveup, movedown, moveleft, moveright=False, False, False, False

def initialise():
    global height, width, clock, g, font20, font60
    g=pygame.display.set_mode([width,height])
    pygame.display.set_caption("Path finder")
    clock=pygame.time.Clock()
    #print(pygame.display.get_driver())



def RGBshift():
    global colours, speed
    if colours[0] == 255 and colours[1] < 255 and colours[2] == 0:
        colours[1] += speed
    elif colours[0] > 0 and colours[1] == 255 and colours[2] == 0:
        colours[0] -= speed
    elif colours[0] == 0 and colours[1] == 255 and colours[2] < 255:
        colours[2] += speed
    elif colours[0] == 0 and colours[1] > 0 and colours[2] == 255:
        colours[1] -= speed
    elif colours[0] < 255 and colours[1] == 0 and colours[2] == 255:
        colours[0] += speed
    elif colours[0] == 255 and colours[1] == 0 and colours[2] > 0:
        colours[2] -= speed




def events():
    global click, mouseloc, menus, moveup, movedown, moveleft, moveright, loop, is_looping, find, finding, menus
    mouseloc=pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            if menus[-1] == program:
                menus.append(escmenu)
            elif menus[-1] == escmenu:
                menus = [program]
            elif len(menus)>1:
                menus.pop()
        if event.type == pygame.MOUSEBUTTONUP:
            click = True



        if menus[-1] == program:

            if event.type == pygame.KEYDOWN:
                if event.key == K_w or event.key == K_UP:
                    moveup = True
                if event.key == K_s or event.key == K_DOWN:
                    movedown = True
                if event.key == K_a or event.key == K_LEFT:
                    moveleft = True
                if event.key == K_d or event.key == K_RIGHT:
                    moveright = True
            if event.type == pygame.KEYUP:
                if event.key == K_w or event.key == K_UP:
                    moveup = False
                if event.key == K_s or event.key == K_DOWN:
                    movedown = False
                if event.key == K_a or event.key == K_LEFT:
                    moveleft = False
                if event.key == K_d or event.key == K_RIGHT:
                    moveright = False


##    global is_looping, loop, finding, find, moveup, movedown, moveleft, moveright, scale, width, height
##    for event in pygame.event.get():
##        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
##            if finding == True:
##                find.cancel()
##            if is_looping==True:
##                loop.cancel()
##            pygame.quit()
##            sys.exit()


        elif event.type == KEYDOWN and event.key == K_1:
            ##Re generate the grid
            return 1
        elif event.type == KEYDOWN and event.key == K_2:
            ##Place markers
            return 2
        elif event.type == KEYDOWN and event.key == K_3 and is_looping == False:
            pass
            ##Solve the map
##            is_looping = True
##            return 3
        elif event.type == KEYDOWN and event.key == K_4 and is_looping == True:
            pass
##            is_looping = False
##            loop.cancel()
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
        row.append([0,5,-1])
        grid.append(row)
    row=[]
    for i in range(int((width/20))+1):
        temp=[]
        temp.append(0)
        temp.append(5)
        temp.append(-1)
        row.append(temp)
    grid.append(row)


def startup():
    global screen_rect, height, width, mmvar, omvar, emvar, openmvar, RGBcycle, minimap, scale
    screen_rect=g.get_rect()
    title=font60.render('Path finder', True, pygame.Color('Cyan'))
    titleloc=title.get_rect()
    titleloc.center=screen_rect.center[0],(height/10)*1
    starttxt = font60.render('Start', True, pygame.Color('White'))
    starttxtalt = font60.render('Start', True, pygame.Color('Green'))
    starttxtloc=starttxt.get_rect()
    starttxtloc.center=screen_rect.center[0],(height/10)*2
    optionstxt = font60.render('Options', True, pygame.Color('White'))
    optionstxtalt = font60.render('Options', True, pygame.Color('Green'))
    optionstxtloc=optionstxt.get_rect()
    optionstxtloc.center=screen_rect.center[0],(height/10)*3
    exittxt = font60.render('Exit', True, pygame.Color('White'))
    exittxtalt = font60.render('Exit', True, pygame.Color('Green'))
    exittxtloc=exittxt.get_rect()
    exittxtloc.center=screen_rect.center[0],(height/10)*9

    mmvar=[[title, titleloc], [starttxt, starttxtalt, starttxtloc, start], [optionstxt, optionstxtalt, optionstxtloc, options_menu], [exittxt, exittxtalt, exittxtloc, exit_prog]]

    title=font60.render('Options', True, pygame.Color('Cyan'))
    titleloc=title.get_rect()
    titleloc.center=screen_rect.center[0],(height/10)*1
    t_RGBtxt = font60.render('RGB cycle: '+str(RGBcycle), True, pygame.Color('White'))
    t_RGBtxtalt = font60.render('RGB cycle: '+str(RGBcycle), True, pygame.Color('Green'))
    t_RGBtxtloc=t_RGBtxt.get_rect()
    t_RGBtxtloc.center=screen_rect.center[0],(height/10)*2
    t_minimaptxt = font60.render('Minimap: '+str(minimap), True, pygame.Color('White'))
    t_minimaptxtalt = font60.render('Minimap: '+str(minimap), True, pygame.Color('Green'))
    t_minimaptxtloc=t_minimaptxt.get_rect()
    t_minimaptxtloc.center=screen_rect.center[0],(height/10)*3


    t_sensitivitytxt = font60.render('Sensitivity: ', True, pygame.Color('White'))
    t_sensitivitytxtalt = font60.render('Sensitivity: ', True, pygame.Color('Green'))
    t_sensitivitytxtloc=t_sensitivitytxt.get_rect()
    t_sensitivitytxtloc.center=screen_rect.center[0],(height/10)*4


    t_scaletxt = font60.render('Scale: '+str(scale), True, pygame.Color('White'))
    t_scaletxtalt = font60.render('Scale: '+str(scale), True, pygame.Color('Green'))        ##Fix scaling: lines 373 & 382
    t_scaletxtloc=t_scaletxt.get_rect()
    t_scaletxtloc.center=screen_rect.center[0],(height/10)*5



    backtxt = font60.render('Back', True, pygame.Color('White'))
    backtxtalt = font60.render('Back', True, pygame.Color('Green'))
    backtxtloc=backtxt.get_rect()
    backtxtloc.center=screen_rect.center[0],(height/10)*9

    ## Overall movement sensitivity, UI scale, FPS cap/speed of path filling 

    omvar=[[title, titleloc], [t_RGBtxt, t_RGBtxtalt, t_RGBtxtloc, toggleRGB], [t_minimaptxt, t_minimaptxtalt, t_minimaptxtloc, toggleminimap], [t_sensitivitytxt, t_sensitivitytxtalt, t_sensitivitytxtloc, sensitivity], [t_scaletxt, t_scaletxtalt, t_scaletxtloc, changescale], [backtxt, backtxtalt, backtxtloc, back]]
    ##omvar.pop(4)

    title=font60.render('Options', True, pygame.Color('Cyan'))
    titleloc=title.get_rect()
    titleloc.center=screen_rect.center[0],(height/10)*1
    conttxt = font60.render('Continue', True, pygame.Color('White'))
    conttxtalt = font60.render('Continue', True, pygame.Color('Green'))
    conttxtloc=conttxt.get_rect()
    conttxtloc.center=screen_rect.center[0],(height/10)*2
    optionstxt = font60.render('Options', True, pygame.Color('White'))
    optionstxtalt = font60.render('Options', True, pygame.Color('Green'))
    optionstxtloc=optionstxt.get_rect()
    optionstxtloc.center=screen_rect.center[0],(height/10)*3    
    savetxt = font60.render('Save', True, pygame.Color('White'))
    savetxtalt = font60.render('Save', True, pygame.Color('Green'))
    savetxtloc=savetxt.get_rect()
    savetxtloc.center=screen_rect.center[0],(height/10)*4
    exittxt = font60.render('Exit to main menu', True, pygame.Color('White'))
    exittxtalt = font60.render('Exit to main menu', True, pygame.Color('Green'))
    exittxtloc=exittxt.get_rect()
    exittxtloc.center=screen_rect.center[0],(height/10)*9

    emvar=[[title, titleloc], [conttxt, conttxtalt, conttxtloc, back], [optionstxt, optionstxtalt, optionstxtloc, options_menu], [savetxt, savetxtalt, savetxtloc, save_map], [exittxt, exittxtalt, exittxtloc, exit_to_main]]

    title=font60.render('Saves', True, pygame.Color('Cyan'))
    titleloc=title.get_rect()
    titleloc.center=screen_rect.center[0],(height/10)*1
    newtxt = font60.render('New save', True, pygame.Color('White'))
    newtxtalt = font60.render('New save', True, pygame.Color('Green'))
    newtxtloc=newtxt.get_rect()
    newtxtloc.center=screen_rect.center[0],(height/10)*2
    backtxt = font60.render('Back', True, pygame.Color('White'))
    backtxtalt = font60.render('Back', True, pygame.Color('Green'))
    backtxtloc=backtxt.get_rect()
    backtxtloc.center=screen_rect.center[0],(height/10)*9

    openmvar=[[title, titleloc], [newtxt, newtxtalt, newtxtloc, start_prog], [backtxt, backtxtalt, backtxtloc, back]]

def exit_prog():
    pygame.quit()
    sys.exit()

def options_menu():
    global menus
    menus.append(optionsmenu)
##    print('Options')

def start():
    global menus
    menus.append(openmenu)
##    print('Start')

def start_prog():
    global menus
    menus=[program]

def save_map():
    print('Save')

def back():
    global menus
    menus.pop()
    pass

def exit_to_main():
    global menus, vertical, horizontal
    menus=[mainmenu]
    vertical,horizontal=0,0


def toggleRGB():
    global RGBcycle, colours
    if RGBcycle:
        RGBcycle = False
    else:
        RGBcycle = True
        colours=[255,0,0]
    startup()

def toggleminimap():
    global minimap
    if minimap:
        minimap = False
    else:
        minimap = True
    startup()

def sensitivity():
    None
    pass

def changescale():
    global scale
    scale += 10
    if scale >= 70:
        scale = 40
    startup()


def mainmenu():
    global mmvar, mouseloc, click, colours
    g.fill(colours)
    g.blit(mmvar[0][0],mmvar[0][1])
    for i in range(len(mmvar)-1):
        i+=1
        g.blit(mmvar[i][0],mmvar[i][2])
        if mouseloc[0] in range (mmvar[i][2][0],mmvar[i][2][0]+mmvar[i][2][2]) and mouseloc[1] in range (mmvar[i][2][1],mmvar[i][2][1]+mmvar[i][2][3]):
            g.blit(mmvar[i][1],mmvar[i][2])
            if click:
                call=mmvar[i][3]
                call()

def openmenu():
    global openmvar, mouseloc, click, colours
    g.fill(colours)
    g.blit(openmvar[0][0],openmvar[0][1])
    for i in range(len(openmvar)-1):
        i+=1
        g.blit(openmvar[i][0],openmvar[i][2])
        if mouseloc[0] in range (openmvar[i][2][0],openmvar[i][2][0]+openmvar[i][2][2]) and mouseloc[1] in range (openmvar[i][2][1],openmvar[i][2][1]+openmvar[i][2][3]):
            g.blit(openmvar[i][1],openmvar[i][2])
            if click:
                call=openmvar[i][3]
                call()

    


def escmenu():
    global emvar, mouseloc, click, colours
    g.fill(colours)
    g.blit(emvar[0][0],emvar[0][1])
    for i in range(len(emvar)-1):
        i+=1
        g.blit(emvar[i][0],emvar[i][2])
        if mouseloc[0] in range (emvar[i][2][0],emvar[i][2][0]+emvar[i][2][2]) and mouseloc[1] in range (emvar[i][2][1],emvar[i][2][1]+emvar[i][2][3]):
            g.blit(emvar[i][1],emvar[i][2])
            if click:
                call=emvar[i][3]
                call()

def optionsmenu():
    global omvar, mouseloc, click, colours
    g.fill(colours)
    g.blit(omvar[0][0],omvar[0][1])
    for i in range(len(omvar)-1):
        i+=1
        g.blit(omvar[i][0],omvar[i][2])
        if mouseloc[0] in range (omvar[i][2][0],omvar[i][2][0]+omvar[i][2][2]) and mouseloc[1] in range (omvar[i][2][1],omvar[i][2][1]+omvar[i][2][3]):
            g.blit(omvar[i][1],omvar[i][2])
            if click:
                call=omvar[i][3]
                call()



def draw():
    global click
    clock.tick(60)
    fps = font20.render(str(int(clock.get_fps()))+" FPS", True, pygame.Color('Red'))
    g.blit(fps, [0,0])
    pygame.display.flip()

def program():
    global grid, vertical, horizontal, width, height, scale, minimap
    clock.tick(75)
    text = font20.render(str(int(clock.get_fps()))+" FPS", True, pygame.Color('red'))
    pygame.draw.rect(g,(80,80,80), [0,0,width,height],0)
    column2 = int((len(grid[0])-52)-horizontal/scale)
    if column2 > len(grid[0]):
        column2 = len(grid[0])
    column1 = (int(0-(horizontal/scale)))
    if column1 <= 0:
        column1 = 0
    row1 = (int(0-(vertical/scale)))
    if row1 <= 0:
        row1 = 0
    row2 = int((len(grid)-28)-vertical/scale)
    if row2 > len(grid):
        row2 = len(grid)
    for row in range(row1, row2):
        for column in range(column1,column2):
            if grid[row][column][1] == 0:
                pygame.draw.rect(g, (0,(grid[row][column][0]),0), [column*scale+horizontal, row*scale+vertical, scale,scale],0)
            elif grid[row][column][1] == 1:
                pygame.draw.rect(g, (0,grid[row][column][0],grid[row][column][0]), [column*scale+horizontal, row*scale+vertical, scale,scale],0)
            elif grid[row][column][1] == 2:
                pygame.draw.rect(g, (grid[row][column][0],0,grid[row][column][0]), [column*scale+horizontal, row*scale+vertical, scale,scale],0)
            elif grid[row][column][1] == 3:
                pygame.draw.rect(g, (grid[row][column][0],0,0), [column*scale+horizontal, row*scale+vertical, scale,scale],0)
            elif grid[row][column][1] == 4:
                pygame.draw.rect(g, (grid[row][column][0],grid[row][column][0],0), [column*scale+horizontal, row*scale+vertical, scale,scale],0)
##            if grid[row][column][2] != -1:
##                height = font.render(str(grid[row][column][2]), True, pygame.Color('gray'))
##                g.blit(height, (column*scale, (row*scale)+5))
    if minimap:
        for row in range(len(grid)):
            for column in range(len(grid[0])):
                if grid[row][column][1] == 0:
                    pygame.draw.rect(g, (0,(grid[row][column][0]),0), [column*2, row*2, 2,2],0)
                elif grid[row][column][1] == 1:
                    pygame.draw.rect(g, (0,grid[row][column][0],grid[row][column][0]), [column*2, row*2, 2,2],0)
                elif grid[row][column][1] == 2:
                    pygame.draw.rect(g, (grid[row][column][0],0,grid[row][column][0]), [column*2, row*2, 2,2],0)
                elif grid[row][column][1] == 3:
                    pygame.draw.rect(g, (grid[row][column][0],0,0), [column*2, row*2, 2,2],0)
                elif grid[row][column][1] == 4:
                    pygame.draw.rect(g, (grid[row][column][0],grid[row][column][0],0), [column*2, row*2, 2,2],0)
                elif grid[row][column][1] == 5:
                    pygame.draw.rect(g, (255,255,255), [column*2, row*2, 5,5],0)
        pygame.draw.rect(g,(255,255,255),[horizontal/-25, vertical/-25,64,36],1)
        g.blit(text, (0,len(grid)*2+5))
    else:
        g.blit(text, (0,0))

    pygame.draw.rect(g, (50,50,50), [width-200,0, 200, height], 0)        #Quick access to settings whilst program is running go here



    pygame.display.flip()



menus=[mainmenu]
initialise()
startup()
genmap()
RGBcycle=False
while True:
    if moveup == True:
        vertical+=20
    if movedown == True:
        vertical-=20
    if moveleft == True:
        horizontal+=20
    if moveright == True:
        horizontal-=20
    if RGBcycle:
        RGBshift()
    else:
        colours=[0,0,0]
    click = False
    value = events()
    if value == 1:
        genmap()
    call=menus[-1]
    call()
    if call != program:
        draw()

     













