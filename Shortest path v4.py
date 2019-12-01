import contextlib
with contextlib.redirect_stdout(None):
    import pygame, random, os, sys, time, threading
    from pygame.locals import *

width, height = 1600, 900

pause = False
startmenu = True
optionmenuenabled = False
hover = False


def initialise():
    global width, height, g, clock, font20, font60, grid, bias, scale, loop, looping, find, finding, pause, startmenu, optionmenuenabled, bclick, bhover
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    g=pygame.display.set_mode([width,height])
    screen_rect=g.get_rect()
    pycenter = screen_rect.center

    res=pygame.display.list_modes()
    center=[res[0][0]/2,res[0][1]/2]

##    print(res[0],res[1])
##    print('Window location:',(center[0]-pycenter[0]), (center[1]-pycenter[1]))
##    print(str(int(center[0]-pycenter[0]))+", "+str(int(center[1]-pycenter[1])))
    g=pygame.display.set_mode([width,height-1])
    os.environ['SDL_VIDEO_WINDOW_POS'] = str(int(center[0]-pycenter[0]))+", "+str(int(center[1]-pycenter[1]))
    g=pygame.display.set_mode([width,height])


    pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=4096)
    bclick = pygame.mixer.Sound("button click.wav")
    bhover = pygame.mixer.Sound("button hover.wav")


##    pygame.mouse.set_cursor((8, 8), (4, 4), (24, 24, 24, 231, 231, 24, 24, 24), (0, 0, 0, 0, 0, 0, 0, 0))
##    pygame.mouse.set_cursor((16, 19), (0, 0), (128, 0, 192, 0, 160, 0, 144, 0, 136, 0, 132, 0, 130, 0, 129, 0, 128, 128, 128, 64, 128, 32, 128, 16, 129, 240, 137, 0, 148, 128, 164, 128, 194, 64, 2, 64, 1, 128), (128, 0, 192, 0, 224, 0, 240, 0, 248, 0, 252, 0, 254, 0, 255, 0, 255, 128, 255, 192, 255, 224, 255, 240, 255, 240, 255, 0, 247, 128, 231, 128, 195, 192, 3, 192, 1, 128))

    if fullscreen:
        width,height=res[0][0],res[0][1]
##    g=pygame.display.set_mode([width,height])
    pygame.display.set_caption("Path finder")
    clock=pygame.time.Clock()
    font20=pygame.font.SysFont("SansMS", 20)
    font60=pygame.font.SysFont("SansMS", 60)

    grid=[]
    bias=[0,1,1]
    scale=50
    loop, looping = None, False
    find, finding = None, False

vertical, horizontal = 0, 0
moveup, movedown, moveleft, moveright = False, False, False, False
fullscreen = False

resx=[640,800,1280,1280,1600,1600,1920,1920]
resy=[480,600,1024,720,900,1200,1080,1200]

def startup():
    global mmvar, emvar, omvar, height, width, screen_rect
    screen_rect=g.get_rect()
    title = font60.render('Path finder', True, pygame.Color('cyan'))
    titleloc=title.get_rect()
    titleloc.center=screen_rect.center[0],(height/10)*1
    starttxt = font60.render('Start', True, pygame.Color('White'))
    starttxtloc=starttxt.get_rect()
    starttxtloc.center=screen_rect.center[0],(height/10)*2
    optionstxt = font60.render('Options', True, pygame.Color('White'))
    opttxtloc=optionstxt.get_rect()
    opttxtloc.center=screen_rect.center[0],(height/10)*3
    exittxt = font60.render('Exit', True, pygame.Color('White'))
    exittxtloc=exittxt.get_rect()
    exittxtloc.center=screen_rect.center[0],(height/10)*9
    mmvar=[title, titleloc, starttxtloc, opttxtloc, exittxtloc]

    title = font60.render('Pause', True, pygame.Color('cyan'))
    titleloc=title.get_rect()
    titleloc.center=screen_rect.center[0],(height/10)*1
    continuetxt = font60.render('Continue', True, pygame.Color('White'))
    conttxtloc=continuetxt.get_rect()
    conttxtloc.center=screen_rect.center[0],(height/10)*2
    optionstxt = font60.render('Options', True, pygame.Color('White'))
    opttxtloc=optionstxt.get_rect()
    opttxtloc.center=screen_rect.center[0],(height/10)*3
    savetxt = font60.render('Save', True, pygame.Color('White'))
    savetxtloc=savetxt.get_rect()
    savetxtloc.center=screen_rect.center[0],(height/10)*4
    exittxt = font60.render('Exit to main menu', True, pygame.Color('White'))
    exittxtloc=exittxt.get_rect()
    exittxtloc.center=screen_rect.center[0],(height/10)*9
    emvar=[title, titleloc, conttxtloc, opttxtloc, savetxtloc, exittxtloc]

    optionstxt = font60.render('Options', True, pygame.Color('cyan'))
    opttxtloc=optionstxt.get_rect()
    opttxtloc.center=screen_rect.center[0],(height/10)*1
    backtxt = font60.render('Back', True, pygame.Color('White'))
    backtxtloc=backtxt.get_rect()
    backtxtloc.center=screen_rect.center[0],(height/10)*9
    restxt = font60.render("Resolution: "+str(int(width))+"x"+str(int(height)), True, pygame.Color('white'))
    restxtloc=restxt.get_rect()
    restxtloc.center=screen_rect.center[0],(height/10)*2
    omvar=[optionstxt, opttxtloc, backtxtloc, restxtloc]





def events():
    global moveup, movedown, moveleft, moveright, startmenu, mouseloc
    mouseloc=pygame.mouse.get_pos()
##    if pygame.mouse.get_pressed()[0]:
##        print('CLICK')
##        return "click"
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            print('Escape')
            return "esc"
##        if event.type == pygame.MOUSEBUTTONDOWN:
##            print('Click')
##            return "click"

def mainmenu():
    global pause, startmenu, optionmenuenabled, mmvar, mouseloc, click, bclick, bhover, hover
    clock.tick(60)
    g.fill([0,0,0])
    text = font20.render(str(int(clock.get_fps()))+" FPS", True, pygame.Color('red'))
    g.blit(text, (0,0))
    g.blit(mmvar[0],mmvar[1])

    event = pygame.event.poll()
    if mouseloc[0] in range (mmvar[4][0],mmvar[4][0]+mmvar[4][2]) and mouseloc[1] in range (mmvar[4][1],mmvar[4][1]+mmvar[4][3]):
        exittxt = font60.render('Exit', True, pygame.Color('Green'))
        g.blit(exittxt, mmvar[4])
        if click:
            bclick.play()
            print('Exit')
            pygame.quit()
            sys.exit()
    else:
        exittxt = font60.render('Exit', True, pygame.Color('White'))
        g.blit(exittxt, mmvar[4])


    if mouseloc[0] in range (mmvar[2][0],mmvar[2][0]+mmvar[2][2]) and mouseloc[1] in range (mmvar[2][1],mmvar[2][1]+mmvar[2][3]):
        starttxt = font60.render('Start', True, pygame.Color('Green'))
        g.blit(starttxt, mmvar[2])
        if click:
            bclick.play()
            print('Start')
            pause = False
            startmenu = False
            optionmenuenabled = False
    else:
        starttxt = font60.render('Start', True, pygame.Color('White'))
        g.blit(starttxt, mmvar[2])


    if mouseloc[0] in range (mmvar[3][0],mmvar[3][0]+mmvar[3][2]) and mouseloc[1] in range (mmvar[3][1],mmvar[3][1]+mmvar[3][3]):
        optionstxt = font60.render('Options', True, pygame.Color('Green'))
        g.blit(optionstxt, mmvar[3])
        if click:
            bclick.play()
            print('Options')
            optionmenuenabled = True
            pause = False
    else:
        optionstxt = font60.render('Options', True, pygame.Color('White'))
        g.blit(optionstxt, mmvar[3])

    pygame.display.flip()


def escmenu():
    global pause, optionmenuenabled, startmenu, emvar, mouseloc, click, bclick, bhover
    clock.tick(60)
    g.fill([0,0,0])
    screen_rect=g.get_rect()
    text = font20.render(str(int(clock.get_fps()))+" FPS", True, pygame.Color('red'))
    g.blit(text, (0,0))
    g.blit(emvar[0],emvar[1])

    mouseloc=pygame.mouse.get_pos()
    event = pygame.event.poll()
    if event.type == KEYDOWN and event.key == K_ESCAPE:
        pause = False
    if mouseloc[0] in range (emvar[2][0],emvar[2][0]+emvar[2][2]) and mouseloc[1] in range (emvar[2][1],emvar[2][1]+emvar[2][3]):
        continuetxt = font60.render('Continue', True, pygame.Color('Green'))
        g.blit(continuetxt, emvar[2])
        if click:
            bclick.play()
            print('Continue')
            pause = False
    else:
        continuetxt = font60.render('Continue', True, pygame.Color('White'))
        g.blit(continuetxt, emvar[2])


    if mouseloc[0] in range (emvar[3][0],emvar[3][0]+emvar[3][2]) and mouseloc[1] in range (emvar[3][1],emvar[3][1]+emvar[3][3]):
        optionstxt = font60.render('Options', True, pygame.Color('Green'))
        g.blit(optionstxt, emvar[3])
        if click:
            bclick.play()
            print('Options')
            optionmenuenabled = True
    else:
        optionstxt = font60.render('Options', True, pygame.Color('White'))
        g.blit(optionstxt, emvar[3])

    if mouseloc[0] in range (emvar[4][0],emvar[4][0]+emvar[4][2]) and mouseloc[1] in range (emvar[4][1],emvar[4][1]+emvar[4][3]):
        savetxt = font60.render('Save', True, pygame.Color('Green'))
        g.blit(savetxt, emvar[4])
        if click:
            bclick.play()
            print('Save')
    else:
        savetxt = font60.render('Save', True, pygame.Color('White'))
        g.blit(savetxt, emvar[4])


    if mouseloc[0] in range (emvar[5][0],emvar[5][0]+emvar[5][2]) and mouseloc[1] in range (emvar[5][1],emvar[5][1]+emvar[5][3]):
        exittxt = font60.render('Exit to main menu', True, pygame.Color('Green'))
        g.blit(exittxt, emvar[5])
        if click:
            bclick.play()
            print('Exit to main menu')
            pause = False
            startmenu = True
    else:
        exittxt = font60.render('Exit to main menu', True, pygame.Color('White'))
        g.blit(exittxt, emvar[5])

    pygame.display.flip()

def optionmenu():
    global pause, optionmenuenabled, mouseloc, click, omvar, width, height,resx, resy, res, bclick, bhover
    clock.tick(60)
    g.fill([0,0,0])
    screen_rect=g.get_rect()
    text = font20.render(str(int(clock.get_fps()))+" FPS", True, pygame.Color('red'))
    g.blit(text, (0,0))

    g.blit(omvar[0], omvar[1])

    mouseloc=pygame.mouse.get_pos()
    event = pygame.event.poll()
    if mouseloc[0] in range (omvar[2][0],omvar[2][0]+omvar[2][2]) and mouseloc[1] in range (omvar[2][1],omvar[2][1]+omvar[2][3]):
        backtxt = font60.render('Back', True, pygame.Color('Green'))
        g.blit(backtxt, omvar[2])
        if click:
            bclick.play()
            print('Back')
            optionmenuenabled = False
    else:
        backtxt = font60.render('Back', True, pygame.Color('White'))
        g.blit(backtxt, omvar[2])

    if mouseloc[0] in range(omvar[3][0],omvar[3][0]+omvar[3][2]) and mouseloc[1] in range (omvar[3][1],omvar[3][1]+omvar[3][3]):
        restxt = font60.render("Resolution: "+str(int(width))+"x"+str(int(height)), True, pygame.Color('Green'))
        g.blit(restxt, omvar[3])
        if click:
            bclick.play()
            print('Change resolution')
            res+=1
            if res >= 8:
                res = 0
            width, height = resx[res],resy[res]
            initialise()
            startup()
    else:
        restxt = font60.render("Resolution: "+str(int(width))+"x"+str(int(height)), True, pygame.Color('White'))
        g.blit(restxt, omvar[3])

    pygame.display.flip()

def draw():
    clock.tick(60)
    g.fill([80,80,80])
    text = font20.render(str(int(clock.get_fps()))+" FPS", True, pygame.Color('red'))
    g.blit(text, (0,0))
    pygame.display.flip()


initialise()
screen_rect=g.get_rect()
startup()
delay = 0
res=4
while True:
    delay += 1
    click = False
    mouseloc=pygame.mouse.get_pos()
    keypress = events()
    if pygame.mouse.get_pressed()[0] == 1 and delay > 20:
        delay = 0
        click = True
    if keypress == "esc" and pause == False:
        pause = True
        optionmenuenabled = False
    elif keypress == "esc" and pause == True:
        pause = False
    elif keypress == "click":
        click = True
    if optionmenuenabled == True:
        optionmenu()
    elif startmenu == True:
        mainmenu()
    elif pause == True:
        escmenu()
    else:
##        pygame.mouse.set_pos([screen_rect.center[0],screen_rect.center[1]])
        draw()
