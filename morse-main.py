try:
    import pygame
    from pygame.locals import *
    from time import time,sleep
    from morse_lookup import *
    from sys import exit
    from config import *
    import tkinter as tk
    from array import array
    from layout import *
    from math import floor,sqrt
    from random import randint

#if a library is missing
except ImportError as e:
    try:
        #check it's the right python version
        from platform import python_version
        ver = python_version()
        if str(ver[0]) != "3":
            print("NOTE - This program will not work on python 2.")
            print("Please ensure that it is running on python 3.")
            print()
            print("Your current version of Python is " + ver)
    except:
        pass
    print()
    print("Missing required file/library:")
    print(e)
    from time import sleep
    from sys import exit
    sleep(10)
    exit()

#make it so things don't break if I'm coding on my pc and not the Pi
try:
    import RPi.GPIO as GPIO
    onapi = True
except ImportError:
    print("Not running on Raspberry Pi, Disabling GPIO Usage")
    onapi = False

def main():

    #get the screen resolution
    root = tk.Tk()
    root.withdraw()

    xres = int(root.winfo_screenwidth()/1)
    #this next line is here because my screen isn't 16:9, but the final result probably will be
    #yres = int(xres*9.0/16.0)
    yres = int(root.winfo_screenheight()/1)

    if onapi:
        #set up the GPIO for the physical morse code key
        GPIO.setmode(GPIO.BCM)
        #GPIO.setwarnings(False)
        GPIO.setup(gpiokey,GPIO.IN)

    #set it all up
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    window = pygame.display.set_mode((xres,yres),FULLSCREEN)
    window.fill(backgroundcol)
    pygame.display.set_caption("Morse Code")

    #get the position results from the layout file
    keyboardposresults = keyboardpos(xres,yres)
    mckeyposresults = mckeypos(xres,yres)
    keysposresults = keyspos((keyboardposresults[0]+yres/64,keyboardposresults[1]+yres/64,keyboardposresults[2]-yres/32,keyboardposresults[3]-yres/32))
    charstreamresults = charstreampos(xres,yres)
    morsestreamresults = morsestreampos(xres,yres)
    morsestreamarea = morsestreamresults[2]
    dashwidth = morsestreamarea[2]/30
    dashstart = morsestreamarea[0]+dashwidth * 16
    dashradius = morsestreamarea[3]/2
    mckeycomponents = mckeyinnards(mckeyposresults)

    #draw the various components
    pygame.draw.rect(window, keyboardcol, keyboardposresults)
    pygame.draw.rect(window, keyboardcol, mckeyposresults)
    pygame.draw.rect(window, charstreamoutlinecol, charstreamresults[0])
    pygame.draw.rect(window, charstreambackgroundcol, charstreamresults[1])
    pygame.draw.rect(window, charstreamoutlinecol, morsestreamresults[0])
    pygame.draw.rect(window, charstreambackgroundcol, morsestreamresults[1])
    pygame.draw.rect(window, mckeytopbox, mckeycomponents[3])
    pygame.draw.rect(window, mckeyvertbar, mckeycomponents[2])
    pygame.draw.circle(window, mckeycircle, mckeycomponents[0], mckeycomponents[1])

    #get the sound effects
    dashsound = pygame.mixer.Sound("dash.ogg")
    dotsound = pygame.mixer.Sound("dot.ogg")
    downsound = pygame.mixer.Sound("keydown.ogg")

    dashsound.set_volume(soundvolume)
    dotsound.set_volume(soundvolume)
    downsound.set_volume(soundvolume)

    for pos in keysposresults[0]:
        mid = ((pos[0]+pos[2])/2,(pos[1]+pos[3])/2)
        pygame.draw.polygon(window, keytop, [(pos[0],pos[1]),(pos[2],pos[1]),mid])
        pygame.draw.polygon(window, keysid, [(pos[0],pos[1]),(pos[0],pos[3]),mid])
        pygame.draw.polygon(window, keysid, [(pos[2],pos[1]),(pos[2],pos[3]),mid])
        pygame.draw.polygon(window, keybot, [(pos[0],pos[3]),(pos[2],pos[3]),mid])
        pygame.draw.rect(window,keycol,(pos[0]+keysposresults[1],pos[1]+keysposresults[2],keysposresults[1]*6,keysposresults[2]*6))

    def updatekey(key):
        mid = ((key[0]+key[2])/2,(key[1]+key[3])/2)
        pygame.draw.polygon(window, keybot, [(key[0],key[1]),(key[2],key[1]),mid])
        pygame.draw.polygon(window, keysiddown, [(key[0],key[1]),(key[0],key[3]),mid])
        pygame.draw.polygon(window, keysiddown, [(key[2],key[1]),(key[2],key[3]),mid])
        pygame.draw.polygon(window, keytop, [(key[0],key[3]),(key[2],key[3]),mid])
        pygame.draw.rect(window,keysid,(key[0]+keysposresults[1],key[1]+keysposresults[2],keysposresults[1]*6,keysposresults[2]*6))

    def resetkey(key):
        mid = ((key[0]+key[2])/2,(key[1]+key[3])/2)
        pygame.draw.polygon(window, keytop, [(key[0],key[1]),(key[2],key[1]),mid])
        pygame.draw.polygon(window, keysid, [(key[0],key[1]),(key[0],key[3]),mid])
        pygame.draw.polygon(window, keysid, [(key[2],key[1]),(key[2],key[3]),mid])
        pygame.draw.polygon(window, keybot, [(key[0],key[3]),(key[2],key[3]),mid])
        pygame.draw.rect(window,keycol,(key[0]+keysposresults[1],key[1]+keysposresults[2],keysposresults[1]*6,keysposresults[2]*6))

    #pygame.display.update()

    #setting up the keyboard
    keyboardfont = pygame.font.SysFont("FreeMono",int(keysposresults[2]*6))
    backspacefont = pygame.font.SysFont("FreeMono",int(keysposresults[2]*3))
    charstreamfont = pygame.font.SysFont("FreeMono",int(charstreamresults[1][3]-1*yres/32))
    A = keyboardfont.render("A",True,keytextcol)
    B = keyboardfont.render("B",True,keytextcol)
    C = keyboardfont.render("C",True,keytextcol)
    D = keyboardfont.render("D",True,keytextcol)
    E = keyboardfont.render("E",True,keytextcol)
    F = keyboardfont.render("F",True,keytextcol)
    G = keyboardfont.render("G",True,keytextcol)
    H = keyboardfont.render("H",True,keytextcol)
    I = keyboardfont.render("I",True,keytextcol)
    J = keyboardfont.render("J",True,keytextcol)
    K = keyboardfont.render("K",True,keytextcol)
    L = keyboardfont.render("L",True,keytextcol)
    M = keyboardfont.render("M",True,keytextcol)
    N = keyboardfont.render("N",True,keytextcol)
    O = keyboardfont.render("O",True,keytextcol)
    P = keyboardfont.render("P",True,keytextcol)
    Q = keyboardfont.render("Q",True,keytextcol)
    R = keyboardfont.render("R",True,keytextcol)
    S = keyboardfont.render("S",True,keytextcol)
    T = keyboardfont.render("T",True,keytextcol)
    U = keyboardfont.render("U",True,keytextcol)
    V = keyboardfont.render("V",True,keytextcol)
    W = keyboardfont.render("W",True,keytextcol)
    X = keyboardfont.render("X",True,keytextcol)
    Y = keyboardfont.render("Y",True,keytextcol)
    Z = keyboardfont.render("Z",True,keytextcol)
    _1 = keyboardfont.render("1",True,keytextcol)
    _2 = keyboardfont.render("2",True,keytextcol)
    _3 = keyboardfont.render("3",True,keytextcol)
    _4 = keyboardfont.render("4",True,keytextcol)
    _5 = keyboardfont.render("5",True,keytextcol)
    _6 = keyboardfont.render("6",True,keytextcol)
    _7 = keyboardfont.render("7",True,keytextcol)
    _8 = keyboardfont.render("8",True,keytextcol)
    _9 = keyboardfont.render("9",True,keytextcol)
    _0 = keyboardfont.render("0",True,keytextcol)
    BK = backspacefont.render("BK",True,keytextcol)

    #the list of keys, the first key, the x position
    def putkeys():
        #Numbers
        window.blit(_1,((keysposresults[0][0][0]+keysposresults[0][0][2])/2-_1.get_width()/2,(keysposresults[0][0][1]+keysposresults[0][0][3])/2-_1.get_height()/2))
        window.blit(_2,((keysposresults[0][1][0]+keysposresults[0][1][2])/2-_2.get_width()/2,(keysposresults[0][1][1]+keysposresults[0][1][3])/2-_2.get_height()/2))
        window.blit(_3,((keysposresults[0][2][0]+keysposresults[0][2][2])/2-_3.get_width()/2,(keysposresults[0][2][1]+keysposresults[0][2][3])/2-_3.get_height()/2))
        window.blit(_4,((keysposresults[0][3][0]+keysposresults[0][3][2])/2-_4.get_width()/2,(keysposresults[0][3][1]+keysposresults[0][3][3])/2-_4.get_height()/2))
        window.blit(_5,((keysposresults[0][4][0]+keysposresults[0][4][2])/2-_5.get_width()/2,(keysposresults[0][4][1]+keysposresults[0][4][3])/2-_5.get_height()/2))
        window.blit(_6,((keysposresults[0][5][0]+keysposresults[0][5][2])/2-_6.get_width()/2,(keysposresults[0][5][1]+keysposresults[0][5][3])/2-_6.get_height()/2))
        window.blit(_7,((keysposresults[0][6][0]+keysposresults[0][6][2])/2-_7.get_width()/2,(keysposresults[0][6][1]+keysposresults[0][6][3])/2-_7.get_height()/2))
        window.blit(_8,((keysposresults[0][7][0]+keysposresults[0][7][2])/2-_8.get_width()/2,(keysposresults[0][7][1]+keysposresults[0][7][3])/2-_8.get_height()/2))
        window.blit(_9,((keysposresults[0][8][0]+keysposresults[0][8][2])/2-_9.get_width()/2,(keysposresults[0][8][1]+keysposresults[0][8][3])/2-_9.get_height()/2))
        window.blit(_0,((keysposresults[0][9][0]+keysposresults[0][9][2])/2-_0.get_width()/2,(keysposresults[0][9][1]+keysposresults[0][9][3])/2-_0.get_height()/2))
        #Letters, row 1
        window.blit(Q,((keysposresults[0][10][0]+keysposresults[0][10][2])/2-Q.get_width()/2,(keysposresults[0][10][1]+keysposresults[0][10][3])/2-Q.get_height()/2))
        window.blit(W,((keysposresults[0][11][0]+keysposresults[0][11][2])/2-W.get_width()/2,(keysposresults[0][11][1]+keysposresults[0][11][3])/2-W.get_height()/2))
        window.blit(E,((keysposresults[0][12][0]+keysposresults[0][12][2])/2-E.get_width()/2,(keysposresults[0][12][1]+keysposresults[0][12][3])/2-E.get_height()/2))
        window.blit(R,((keysposresults[0][13][0]+keysposresults[0][13][2])/2-R.get_width()/2,(keysposresults[0][13][1]+keysposresults[0][13][3])/2-R.get_height()/2))
        window.blit(T,((keysposresults[0][14][0]+keysposresults[0][14][2])/2-T.get_width()/2,(keysposresults[0][14][1]+keysposresults[0][14][3])/2-T.get_height()/2))
        window.blit(Y,((keysposresults[0][15][0]+keysposresults[0][15][2])/2-Y.get_width()/2,(keysposresults[0][15][1]+keysposresults[0][15][3])/2-Y.get_height()/2))
        window.blit(U,((keysposresults[0][16][0]+keysposresults[0][16][2])/2-U.get_width()/2,(keysposresults[0][16][1]+keysposresults[0][16][3])/2-U.get_height()/2))
        window.blit(I,((keysposresults[0][17][0]+keysposresults[0][17][2])/2-I.get_width()/2,(keysposresults[0][17][1]+keysposresults[0][17][3])/2-I.get_height()/2))
        window.blit(O,((keysposresults[0][18][0]+keysposresults[0][18][2])/2-O.get_width()/2,(keysposresults[0][18][1]+keysposresults[0][18][3])/2-O.get_height()/2))
        window.blit(P,((keysposresults[0][19][0]+keysposresults[0][19][2])/2-P.get_width()/2,(keysposresults[0][19][1]+keysposresults[0][19][3])/2-P.get_height()/2))
        #row 2
        window.blit(A,((keysposresults[0][20][0]+keysposresults[0][20][2])/2-A.get_width()/2,(keysposresults[0][20][1]+keysposresults[0][20][3])/2-A.get_height()/2))
        window.blit(S,((keysposresults[0][21][0]+keysposresults[0][21][2])/2-S.get_width()/2,(keysposresults[0][21][1]+keysposresults[0][21][3])/2-S.get_height()/2))
        window.blit(D,((keysposresults[0][22][0]+keysposresults[0][22][2])/2-D.get_width()/2,(keysposresults[0][22][1]+keysposresults[0][22][3])/2-D.get_height()/2))
        window.blit(F,((keysposresults[0][23][0]+keysposresults[0][23][2])/2-F.get_width()/2,(keysposresults[0][23][1]+keysposresults[0][23][3])/2-F.get_height()/2))
        window.blit(G,((keysposresults[0][24][0]+keysposresults[0][24][2])/2-G.get_width()/2,(keysposresults[0][24][1]+keysposresults[0][24][3])/2-G.get_height()/2))
        window.blit(H,((keysposresults[0][25][0]+keysposresults[0][25][2])/2-H.get_width()/2,(keysposresults[0][25][1]+keysposresults[0][25][3])/2-H.get_height()/2))
        window.blit(J,((keysposresults[0][26][0]+keysposresults[0][26][2])/2-J.get_width()/2,(keysposresults[0][26][1]+keysposresults[0][26][3])/2-J.get_height()/2))
        window.blit(K,((keysposresults[0][27][0]+keysposresults[0][27][2])/2-K.get_width()/2,(keysposresults[0][27][1]+keysposresults[0][27][3])/2-K.get_height()/2))
        window.blit(L,((keysposresults[0][28][0]+keysposresults[0][28][2])/2-L.get_width()/2,(keysposresults[0][28][1]+keysposresults[0][28][3])/2-L.get_height()/2))
        #row 3
        window.blit(Z,((keysposresults[0][29][0]+keysposresults[0][29][2])/2-Z.get_width()/2,(keysposresults[0][29][1]+keysposresults[0][29][3])/2-Z.get_height()/2))
        window.blit(X,((keysposresults[0][30][0]+keysposresults[0][30][2])/2-X.get_width()/2,(keysposresults[0][30][1]+keysposresults[0][30][3])/2-X.get_height()/2))
        window.blit(C,((keysposresults[0][31][0]+keysposresults[0][31][2])/2-C.get_width()/2,(keysposresults[0][31][1]+keysposresults[0][31][3])/2-C.get_height()/2))
        window.blit(V,((keysposresults[0][32][0]+keysposresults[0][32][2])/2-V.get_width()/2,(keysposresults[0][32][1]+keysposresults[0][32][3])/2-V.get_height()/2))
        window.blit(B,((keysposresults[0][33][0]+keysposresults[0][33][2])/2-B.get_width()/2,(keysposresults[0][33][1]+keysposresults[0][33][3])/2-B.get_height()/2))
        window.blit(N,((keysposresults[0][34][0]+keysposresults[0][34][2])/2-N.get_width()/2,(keysposresults[0][34][1]+keysposresults[0][34][3])/2-N.get_height()/2))
        window.blit(M,((keysposresults[0][35][0]+keysposresults[0][35][2])/2-M.get_width()/2,(keysposresults[0][35][1]+keysposresults[0][35][3])/2-M.get_height()/2))
        #backspace
        window.blit(BK,((keysposresults[0][36][0]+keysposresults[0][36][2])/2-BK.get_width()/2,(keysposresults[0][36][1]+keysposresults[0][36][3])/2-BK.get_height()))
        pygame.draw.polygon(window, keytextcol, [(keysposresults[0][36][0]+keysposresults[1]+(-keysposresults[0][36][0]+keysposresults[0][36][2]-2*keysposresults[1])/8,keysposresults[0][35][1]+keysposresults[2]+(keysposresults[0][35][3]-keysposresults[0][35][1]-2*keysposresults[2])*3/4),
                                              (keysposresults[0][36][0]+keysposresults[1]+(-keysposresults[0][36][0]+keysposresults[0][36][2]-2*keysposresults[1])/4,keysposresults[0][35][1]+keysposresults[2]+(keysposresults[0][35][3]-keysposresults[0][35][1]-2*keysposresults[2])*5/8),
                                              (keysposresults[0][36][0]+keysposresults[1]+(-keysposresults[0][36][0]+keysposresults[0][36][2]-2*keysposresults[1])/4,keysposresults[0][35][1]+keysposresults[2]+(keysposresults[0][35][3]-keysposresults[0][35][1]-2*keysposresults[2])*7/8)])
        pygame.draw.rect(window, keytextcol, (keysposresults[0][36][0]+keysposresults[1]+(-keysposresults[0][36][0]+keysposresults[0][36][2]-2*keysposresults[1])/4,keysposresults[0][35][1]+keysposresults[2]+(keysposresults[0][35][3]-keysposresults[0][35][1]-2*keysposresults[2])*23/32,
                                              (-keysposresults[0][36][0]+keysposresults[0][36][2]-2*keysposresults[1])*5/8,(keysposresults[0][35][3]-keysposresults[0][35][1]-2*keysposresults[2])*1/16))

    putkeys()
    pygame.display.update()

    keystring = ""
    oldkeystring = ""
    word = ""
    key = ""
    end = time()
    start = 0

    keydown = False
    while True:
        if onapi:
            #detecting the physical key
            if (GPIO.input(gpiokey) == False and keydown == False):
                keydown = True
                start = time()
                if soundactive:
                    downsound.play(-1)
                key = "KEY"
                pygame.draw.rect(window, keyboardcol, mckeyposresults)
                pygame.draw.rect(window, mckeytopbox, mckeycomponents[3])
                pygame.draw.rect(window, mckeyvertbardark, mckeycomponents[2])
                pygame.draw.circle(window, mckeycircledark, (mckeycomponents[0][0], mckeycomponents[0][1]+2), mckeycomponents[1])
                pygame.display.update()
            elif (key == "KEY" and GPIO.input(gpiokey) == True and keydown == True):
                keydown = False
                key = ""
                end = time()
                downsound.stop()
                pygame.draw.rect(window, keyboardcol, mckeyposresults)
                pygame.draw.rect(window, mckeytopbox, mckeycomponents[3])
                pygame.draw.rect(window, mckeyvertbar, mckeycomponents[2])
                pygame.draw.circle(window, mckeycircle, mckeycomponents[0], mckeycomponents[1])
                keytime = end-start
                if keytime < dot_threshold:
                    keystring += "."
                else:
                    keystring += "-"
                pygame.display.update()


        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE and escapetoclose:
                pygame.quit()
                exit()
                #detecting the on-screen keyboard being clicked
                #1
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][0][0] and event.pos[0] < keysposresults[0][0][2] and event.pos[1] > keysposresults[0][0][1] and event.pos[1] < keysposresults[0][0][3]) or (event.type == KEYDOWN and event.key == K_1):
                key = "1"
                updatekey(keysposresults[0][0])
                window.blit(_1,((keysposresults[0][0][0]+keysposresults[0][0][2])/2-_1.get_width()/2,(keysposresults[0][0][1]+keysposresults[0][0][3])/2-_1.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "1":
                end = time()
                keystring += ".----"
                resetkey(keysposresults[0][0])
                window.blit(_1,((keysposresults[0][0][0]+keysposresults[0][0][2])/2-_1.get_width()/2,(keysposresults[0][0][1]+keysposresults[0][0][3])/2-_1.get_height()/2))
                key = ""
                pygame.display.update()
                #2
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][1][0] and event.pos[0] < keysposresults[0][1][2] and event.pos[1] > keysposresults[0][1][1] and event.pos[1] < keysposresults[0][1][3]) or (event.type == KEYDOWN and event.key == K_2):
                key = "2"
                updatekey(keysposresults[0][1])
                window.blit(_2,((keysposresults[0][1][0]+keysposresults[0][1][2])/2-_2.get_width()/2,(keysposresults[0][1][1]+keysposresults[0][1][3])/2-_2.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "2":
                end = time()
                keystring += "..---"
                resetkey(keysposresults[0][1])
                window.blit(_2,((keysposresults[0][1][0]+keysposresults[0][1][2])/2-_2.get_width()/2,(keysposresults[0][1][1]+keysposresults[0][1][3])/2-_2.get_height()/2))
                key = ""
                pygame.display.update()
                #3
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][2][0] and event.pos[0] < keysposresults[0][2][2] and event.pos[1] > keysposresults[0][2][1] and event.pos[1] < keysposresults[0][2][3]) or (event.type == KEYDOWN and event.key == K_3):
                key = "3"
                updatekey(keysposresults[0][2])
                window.blit(_3,((keysposresults[0][2][0]+keysposresults[0][2][2])/2-_3.get_width()/2,(keysposresults[0][2][1]+keysposresults[0][2][3])/2-_3.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "3":
                end = time()
                keystring += "...--"
                resetkey(keysposresults[0][2])
                window.blit(_3,((keysposresults[0][2][0]+keysposresults[0][2][2])/2-_3.get_width()/2,(keysposresults[0][2][1]+keysposresults[0][2][3])/2-_3.get_height()/2))
                key = ""
                pygame.display.update()
                #4
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][3][0] and event.pos[0] < keysposresults[0][3][2] and event.pos[1] > keysposresults[0][3][1] and event.pos[1] < keysposresults[0][3][3]) or (event.type == KEYDOWN and event.key == K_4):
                key = "4"
                end = time()
                updatekey(keysposresults[0][3])
                window.blit(_4,((keysposresults[0][3][0]+keysposresults[0][3][2])/2-_4.get_width()/2,(keysposresults[0][3][1]+keysposresults[0][3][3])/2-_4.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "4":
                end = time()
                keystring += "....-"
                resetkey(keysposresults[0][3])
                window.blit(_4,((keysposresults[0][3][0]+keysposresults[0][3][2])/2-_4.get_width()/2,(keysposresults[0][3][1]+keysposresults[0][3][3])/2-_4.get_height()/2))
                key = ""
                pygame.display.update()
                #5
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][4][0] and event.pos[0] < keysposresults[0][4][2] and event.pos[1] > keysposresults[0][4][1] and event.pos[1] < keysposresults[0][4][3]) or (event.type == KEYDOWN and event.key == K_5):
                key = "5"
                updatekey(keysposresults[0][4])
                window.blit(_5,((keysposresults[0][4][0]+keysposresults[0][4][2])/2-_5.get_width()/2,(keysposresults[0][4][1]+keysposresults[0][4][3])/2-_5.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "5":
                end = time()
                keystring += "....."
                resetkey(keysposresults[0][4])
                window.blit(_5,((keysposresults[0][4][0]+keysposresults[0][4][2])/2-_5.get_width()/2,(keysposresults[0][4][1]+keysposresults[0][4][3])/2-_5.get_height()/2))
                key = ""
                pygame.display.update()
                #6
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][5][0] and event.pos[0] < keysposresults[0][5][2] and event.pos[1] > keysposresults[0][5][1] and event.pos[1] < keysposresults[0][5][3]) or (event.type == KEYDOWN and event.key == K_6):
                key = "6"
                updatekey(keysposresults[0][5])
                window.blit(_6,((keysposresults[0][5][0]+keysposresults[0][5][2])/2-_6.get_width()/2,(keysposresults[0][5][1]+keysposresults[0][5][3])/2-_6.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "6":
                end = time()
                keystring += "-...."
                resetkey(keysposresults[0][5])
                window.blit(_6,((keysposresults[0][5][0]+keysposresults[0][5][2])/2-_6.get_width()/2,(keysposresults[0][5][1]+keysposresults[0][5][3])/2-_6.get_height()/2))
                key = ""
                pygame.display.update()
                #7
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][6][0] and event.pos[0] < keysposresults[0][6][2] and event.pos[1] > keysposresults[0][6][1] and event.pos[1] < keysposresults[0][6][3]) or (event.type == KEYDOWN and event.key == K_7):
                key = "7"
                updatekey(keysposresults[0][6])
                window.blit(_7,((keysposresults[0][6][0]+keysposresults[0][6][2])/2-_7.get_width()/2,(keysposresults[0][6][1]+keysposresults[0][6][3])/2-_7.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "7":
                end = time()
                keystring += "--..."
                resetkey(keysposresults[0][6])
                window.blit(_7,((keysposresults[0][6][0]+keysposresults[0][6][2])/2-_7.get_width()/2,(keysposresults[0][6][1]+keysposresults[0][6][3])/2-_7.get_height()/2))
                key = ""
                pygame.display.update()
                #8
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][7][0] and event.pos[0] < keysposresults[0][7][2] and event.pos[1] > keysposresults[0][7][1] and event.pos[1] < keysposresults[0][7][3]) or (event.type == KEYDOWN and event.key == K_8):
                key = "8"
                updatekey(keysposresults[0][7])
                window.blit(_8,((keysposresults[0][7][0]+keysposresults[0][7][2])/2-_8.get_width()/2,(keysposresults[0][7][1]+keysposresults[0][7][3])/2-_8.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "8":
                end = time()
                keystring += "---.."
                resetkey(keysposresults[0][7])
                window.blit(_8,((keysposresults[0][7][0]+keysposresults[0][7][2])/2-_8.get_width()/2,(keysposresults[0][7][1]+keysposresults[0][7][3])/2-_8.get_height()/2))
                key = ""
                pygame.display.update()
                #9
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][8][0] and event.pos[0] < keysposresults[0][8][2] and event.pos[1] > keysposresults[0][8][1] and event.pos[1] < keysposresults[0][8][3]) or (event.type == KEYDOWN and event.key == K_9):
                key = "9"
                updatekey(keysposresults[0][8])
                window.blit(_9,((keysposresults[0][8][0]+keysposresults[0][8][2])/2-_9.get_width()/2,(keysposresults[0][8][1]+keysposresults[0][8][3])/2-_9.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "9":
                end = time()
                keystring += "----."
                resetkey(keysposresults[0][8])
                window.blit(_9,((keysposresults[0][8][0]+keysposresults[0][8][2])/2-_9.get_width()/2,(keysposresults[0][8][1]+keysposresults[0][8][3])/2-_9.get_height()/2))
                key = ""
                pygame.display.update()
                #0
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][9][0] and event.pos[0] < keysposresults[0][9][2] and event.pos[1] > keysposresults[0][9][1] and event.pos[1] < keysposresults[0][9][3]) or (event.type == KEYDOWN and event.key == K_0):
                key = "0"
                updatekey(keysposresults[0][9])
                window.blit(_0,((keysposresults[0][9][0]+keysposresults[0][9][2])/2-_0.get_width()/2,(keysposresults[0][9][1]+keysposresults[0][9][3])/2-_0.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "0":
                end = time()
                keystring += "-----"
                resetkey(keysposresults[0][9])
                window.blit(_0,((keysposresults[0][9][0]+keysposresults[0][9][2])/2-_0.get_width()/2,(keysposresults[0][9][1]+keysposresults[0][9][3])/2-_0.get_height()/2))
                key = ""
                pygame.display.update()
                #Q
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][10][0] and event.pos[0] < keysposresults[0][10][2] and event.pos[1] > keysposresults[0][10][1] and event.pos[1] < keysposresults[0][10][3]) or (event.type == KEYDOWN and event.key == K_q):
                key = "Q"
                updatekey(keysposresults[0][10])
                window.blit(Q,((keysposresults[0][10][0]+keysposresults[0][10][2])/2-Q.get_width()/2,(keysposresults[0][10][1]+keysposresults[0][10][3])/2-Q.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "Q":
                end = time()
                keystring += "--.-"
                resetkey(keysposresults[0][10])
                window.blit(Q,((keysposresults[0][10][0]+keysposresults[0][10][2])/2-Q.get_width()/2,(keysposresults[0][10][1]+keysposresults[0][10][3])/2-Q.get_height()/2))
                key = ""
                pygame.display.update()
                #W
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][11][0] and event.pos[0] < keysposresults[0][11][2] and event.pos[1] > keysposresults[0][11][1] and event.pos[1] < keysposresults[0][11][3]) or (event.type == KEYDOWN and event.key == K_w):
                key = "W"
                updatekey(keysposresults[0][11])
                window.blit(W,((keysposresults[0][11][0]+keysposresults[0][11][2])/2-W.get_width()/2,(keysposresults[0][11][1]+keysposresults[0][11][3])/2-W.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "W":
                end = time()
                keystring += ".--"
                resetkey(keysposresults[0][11])
                window.blit(W,((keysposresults[0][11][0]+keysposresults[0][11][2])/2-W.get_width()/2,(keysposresults[0][11][1]+keysposresults[0][11][3])/2-W.get_height()/2))
                key = ""
                pygame.display.update()
                #E
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][12][0] and event.pos[0] < keysposresults[0][12][2] and event.pos[1] > keysposresults[0][12][1] and event.pos[1] < keysposresults[0][12][3]) or (event.type == KEYDOWN and event.key == K_e):
                key = "E"
                updatekey(keysposresults[0][12])
                window.blit(E,((keysposresults[0][12][0]+keysposresults[0][12][2])/2-E.get_width()/2,(keysposresults[0][12][1]+keysposresults[0][12][3])/2-E.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "E":
                end = time()
                keystring += "."
                resetkey(keysposresults[0][12])
                window.blit(E,((keysposresults[0][12][0]+keysposresults[0][12][2])/2-E.get_width()/2,(keysposresults[0][12][1]+keysposresults[0][12][3])/2-E.get_height()/2))
                key = ""
                pygame.display.update()
                #R
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][13][0] and event.pos[0] < keysposresults[0][13][2] and event.pos[1] > keysposresults[0][13][1] and event.pos[1] < keysposresults[0][13][3]) or (event.type == KEYDOWN and event.key == K_r):
                key = "R"
                updatekey(keysposresults[0][13])
                window.blit(R,((keysposresults[0][13][0]+keysposresults[0][13][2])/2-R.get_width()/2,(keysposresults[0][13][1]+keysposresults[0][13][3])/2-R.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "R":
                end = time()
                keystring += ".-."
                resetkey(keysposresults[0][13])
                window.blit(R,((keysposresults[0][13][0]+keysposresults[0][13][2])/2-R.get_width()/2,(keysposresults[0][13][1]+keysposresults[0][13][3])/2-R.get_height()/2))
                key = ""
                pygame.display.update()
                #T
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][14][0] and event.pos[0] < keysposresults[0][14][2] and event.pos[1] > keysposresults[0][14][1] and event.pos[1] < keysposresults[0][14][3]) or (event.type == KEYDOWN and event.key == K_t):
                key = "T"
                updatekey(keysposresults[0][14])
                window.blit(T,((keysposresults[0][14][0]+keysposresults[0][14][2])/2-T.get_width()/2,(keysposresults[0][14][1]+keysposresults[0][14][3])/2-T.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "T":
                end = time()
                keystring += "-"
                resetkey(keysposresults[0][14])
                window.blit(T,((keysposresults[0][14][0]+keysposresults[0][14][2])/2-T.get_width()/2,(keysposresults[0][14][1]+keysposresults[0][14][3])/2-T.get_height()/2))
                key = ""
                pygame.display.update()
                #Y
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][15][0] and event.pos[0] < keysposresults[0][15][2] and event.pos[1] > keysposresults[0][15][1] and event.pos[1] < keysposresults[0][15][3]) or (event.type == KEYDOWN and event.key == K_y):
                key = "Y"
                updatekey(keysposresults[0][15])
                window.blit(Y,((keysposresults[0][15][0]+keysposresults[0][15][2])/2-Y.get_width()/2,(keysposresults[0][15][1]+keysposresults[0][15][3])/2-Y.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "Y":
                end = time()
                keystring += "-.--"
                resetkey(keysposresults[0][15])
                window.blit(Y,((keysposresults[0][15][0]+keysposresults[0][15][2])/2-Y.get_width()/2,(keysposresults[0][15][1]+keysposresults[0][15][3])/2-Y.get_height()/2))
                key = ""
                pygame.display.update()
                #U
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][16][0] and event.pos[0] < keysposresults[0][16][2] and event.pos[1] > keysposresults[0][16][1] and event.pos[1] < keysposresults[0][16][3]) or (event.type == KEYDOWN and event.key == K_u):
                key = "U"
                updatekey(keysposresults[0][16])
                window.blit(U,((keysposresults[0][16][0]+keysposresults[0][16][2])/2-U.get_width()/2,(keysposresults[0][16][1]+keysposresults[0][16][3])/2-U.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "U":
                end = time()
                keystring += "..-"
                resetkey(keysposresults[0][16])
                window.blit(U,((keysposresults[0][16][0]+keysposresults[0][16][2])/2-U.get_width()/2,(keysposresults[0][16][1]+keysposresults[0][16][3])/2-U.get_height()/2))
                key = ""
                pygame.display.update()
                #I
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][17][0] and event.pos[0] < keysposresults[0][17][2] and event.pos[1] > keysposresults[0][17][1] and event.pos[1] < keysposresults[0][17][3]) or (event.type == KEYDOWN and event.key == K_i):
                key = "I"
                updatekey(keysposresults[0][17])
                window.blit(I,((keysposresults[0][17][0]+keysposresults[0][17][2])/2-I.get_width()/2,(keysposresults[0][17][1]+keysposresults[0][17][3])/2-I.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "I":
                end = time()
                keystring += ".."
                resetkey(keysposresults[0][17])
                window.blit(I,((keysposresults[0][17][0]+keysposresults[0][17][2])/2-I.get_width()/2,(keysposresults[0][17][1]+keysposresults[0][17][3])/2-I.get_height()/2))
                key = ""
                pygame.display.update()
                #O
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][18][0] and event.pos[0] < keysposresults[0][18][2] and event.pos[1] > keysposresults[0][18][1] and event.pos[1] < keysposresults[0][18][3]) or (event.type == KEYDOWN and event.key == K_o):
                key = "O"
                updatekey(keysposresults[0][18])
                window.blit(O,((keysposresults[0][18][0]+keysposresults[0][18][2])/2-O.get_width()/2,(keysposresults[0][18][1]+keysposresults[0][18][3])/2-O.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "O":
                end = time()
                keystring += "---"
                resetkey(keysposresults[0][18])
                window.blit(O,((keysposresults[0][18][0]+keysposresults[0][18][2])/2-O.get_width()/2,(keysposresults[0][18][1]+keysposresults[0][18][3])/2-O.get_height()/2))
                key = ""
                pygame.display.update()
                #P
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][19][0] and event.pos[0] < keysposresults[0][19][2] and event.pos[1] > keysposresults[0][19][1] and event.pos[1] < keysposresults[0][19][3]) or (event.type == KEYDOWN and event.key == K_p):
                key = "P"
                updatekey(keysposresults[0][19])
                window.blit(P,((keysposresults[0][19][0]+keysposresults[0][19][2])/2-P.get_width()/2,(keysposresults[0][19][1]+keysposresults[0][19][3])/2-P.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "P":
                end = time()
                keystring += ".--."
                resetkey(keysposresults[0][19])
                window.blit(P,((keysposresults[0][19][0]+keysposresults[0][19][2])/2-P.get_width()/2,(keysposresults[0][19][1]+keysposresults[0][19][3])/2-P.get_height()/2))
                key = ""
                pygame.display.update()
                #A
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][20][0] and event.pos[0] < keysposresults[0][20][2] and event.pos[1] > keysposresults[0][20][1] and event.pos[1] < keysposresults[0][20][3]) or (event.type == KEYDOWN and event.key == K_a):
                key = "A"
                updatekey(keysposresults[0][20])
                window.blit(A,((keysposresults[0][20][0]+keysposresults[0][20][2])/2-A.get_width()/2,(keysposresults[0][20][1]+keysposresults[0][20][3])/2-A.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "A":
                end = time()
                keystring += ".-"
                resetkey(keysposresults[0][20])
                window.blit(A,((keysposresults[0][20][0]+keysposresults[0][20][2])/2-A.get_width()/2,(keysposresults[0][20][1]+keysposresults[0][20][3])/2-A.get_height()/2))
                key = ""
                pygame.display.update()
                #S
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][21][0] and event.pos[0] < keysposresults[0][21][2] and event.pos[1] > keysposresults[0][21][1] and event.pos[1] < keysposresults[0][21][3]) or (event.type == KEYDOWN and event.key == K_s):
                key = "S"
                updatekey(keysposresults[0][21])
                window.blit(S,((keysposresults[0][21][0]+keysposresults[0][21][2])/2-S.get_width()/2,(keysposresults[0][21][1]+keysposresults[0][21][3])/2-S.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "S":
                end = time()
                keystring += "..."
                resetkey(keysposresults[0][21])
                window.blit(S,((keysposresults[0][21][0]+keysposresults[0][21][2])/2-S.get_width()/2,(keysposresults[0][21][1]+keysposresults[0][21][3])/2-Q.get_height()/2))
                key = ""
                pygame.display.update()
                #D
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][22][0] and event.pos[0] < keysposresults[0][22][2] and event.pos[1] > keysposresults[0][22][1] and event.pos[1] < keysposresults[0][22][3]) or (event.type == KEYDOWN and event.key == K_d):
                key = "D"
                updatekey(keysposresults[0][22])
                window.blit(D,((keysposresults[0][22][0]+keysposresults[0][22][2])/2-D.get_width()/2,(keysposresults[0][22][1]+keysposresults[0][22][3])/2-D.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "D":
                end = time()
                keystring += "-.."
                resetkey(keysposresults[0][22])
                window.blit(D,((keysposresults[0][22][0]+keysposresults[0][22][2])/2-D.get_width()/2,(keysposresults[0][22][1]+keysposresults[0][22][3])/2-Q.get_height()/2))
                key = ""
                pygame.display.update()
                #F
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][23][0] and event.pos[0] < keysposresults[0][23][2] and event.pos[1] > keysposresults[0][23][1] and event.pos[1] < keysposresults[0][23][3]) or (event.type == KEYDOWN and event.key == K_f):
                key = "F"
                updatekey(keysposresults[0][23])
                window.blit(F,((keysposresults[0][23][0]+keysposresults[0][23][2])/2-F.get_width()/2,(keysposresults[0][23][1]+keysposresults[0][23][3])/2-F.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "F":
                end = time()
                keystring += "..-."
                resetkey(keysposresults[0][23])
                window.blit(F,((keysposresults[0][23][0]+keysposresults[0][23][2])/2-F.get_width()/2,(keysposresults[0][23][1]+keysposresults[0][23][3])/2-F.get_height()/2))
                key = ""
                pygame.display.update()
                #G
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][24][0] and event.pos[0] < keysposresults[0][24][2] and event.pos[1] > keysposresults[0][24][1] and event.pos[1] < keysposresults[0][24][3]) or (event.type == KEYDOWN and event.key == K_g):
                key = "G"
                updatekey(keysposresults[0][24])
                window.blit(G,((keysposresults[0][24][0]+keysposresults[0][24][2])/2-G.get_width()/2,(keysposresults[0][24][1]+keysposresults[0][24][3])/2-G.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "G":
                end = time()
                keystring += "--."
                resetkey(keysposresults[0][24])
                window.blit(G,((keysposresults[0][24][0]+keysposresults[0][24][2])/2-G.get_width()/2,(keysposresults[0][24][1]+keysposresults[0][24][3])/2-G.get_height()/2))
                key = ""
                pygame.display.update()
                #H
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][25][0] and event.pos[0] < keysposresults[0][25][2] and event.pos[1] > keysposresults[0][25][1] and event.pos[1] < keysposresults[0][25][3]) or (event.type == KEYDOWN and event.key == K_h):
                key = "H"
                updatekey(keysposresults[0][25])
                window.blit(H,((keysposresults[0][25][0]+keysposresults[0][25][2])/2-H.get_width()/2,(keysposresults[0][25][1]+keysposresults[0][25][3])/2-H.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "H":
                end = time()
                keystring += "...."
                resetkey(keysposresults[0][25])
                window.blit(H,((keysposresults[0][25][0]+keysposresults[0][25][2])/2-H.get_width()/2,(keysposresults[0][25][1]+keysposresults[0][25][3])/2-H.get_height()/2))
                key = ""
                pygame.display.update()
                #J
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][26][0] and event.pos[0] < keysposresults[0][26][2] and event.pos[1] > keysposresults[0][26][1] and event.pos[1] < keysposresults[0][26][3]) or (event.type == KEYDOWN and event.key == K_j):
                key = "J"
                updatekey(keysposresults[0][26])
                window.blit(J,((keysposresults[0][26][0]+keysposresults[0][26][2])/2-J.get_width()/2,(keysposresults[0][26][1]+keysposresults[0][26][3])/2-J.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "J":
                end = time()
                keystring += ".---"
                resetkey(keysposresults[0][26])
                window.blit(J,((keysposresults[0][26][0]+keysposresults[0][26][2])/2-J.get_width()/2,(keysposresults[0][26][1]+keysposresults[0][26][3])/2-J.get_height()/2))
                key = ""
                pygame.display.update()
                #K
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][27][0] and event.pos[0] < keysposresults[0][27][2] and event.pos[1] > keysposresults[0][27][1] and event.pos[1] < keysposresults[0][27][3]) or (event.type == KEYDOWN and event.key == K_k):
                key = "K"
                updatekey(keysposresults[0][27])
                window.blit(K,((keysposresults[0][27][0]+keysposresults[0][27][2])/2-K.get_width()/2,(keysposresults[0][27][1]+keysposresults[0][27][3])/2-K.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "K":
                end = time()
                keystring += "-.-"
                resetkey(keysposresults[0][27])
                window.blit(K,((keysposresults[0][27][0]+keysposresults[0][27][2])/2-K.get_width()/2,(keysposresults[0][27][1]+keysposresults[0][27][3])/2-K.get_height()/2))
                key = ""
                pygame.display.update()
                #L
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][28][0] and event.pos[0] < keysposresults[0][28][2] and event.pos[1] > keysposresults[0][28][1] and event.pos[1] < keysposresults[0][28][3]) or (event.type == KEYDOWN and event.key == K_l):
                key = "L"
                updatekey(keysposresults[0][28])
                window.blit(L,((keysposresults[0][28][0]+keysposresults[0][28][2])/2-L.get_width()/2,(keysposresults[0][28][1]+keysposresults[0][28][3])/2-L.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "L":
                end = time()
                keystring += ".-.."
                resetkey(keysposresults[0][28])
                window.blit(L,((keysposresults[0][28][0]+keysposresults[0][28][2])/2-L.get_width()/2,(keysposresults[0][28][1]+keysposresults[0][28][3])/2-L.get_height()/2))
                key = ""
                pygame.display.update()
                #Z
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][29][0] and event.pos[0] < keysposresults[0][29][2] and event.pos[1] > keysposresults[0][29][1] and event.pos[1] < keysposresults[0][29][3]) or (event.type == KEYDOWN and event.key == K_z):
                key = "Z"
                updatekey(keysposresults[0][29])
                window.blit(Z,((keysposresults[0][29][0]+keysposresults[0][29][2])/2-Z.get_width()/2,(keysposresults[0][29][1]+keysposresults[0][29][3])/2-Z.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "Z":
                end = time()
                keystring += "--.."
                resetkey(keysposresults[0][29])
                window.blit(Z,((keysposresults[0][29][0]+keysposresults[0][29][2])/2-Z.get_width()/2,(keysposresults[0][29][1]+keysposresults[0][29][3])/2-Z.get_height()/2))
                key = ""
                pygame.display.update()
                #X
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][30][0] and event.pos[0] < keysposresults[0][30][2] and event.pos[1] > keysposresults[0][30][1] and event.pos[1] < keysposresults[0][30][3]) or (event.type == KEYDOWN and event.key == K_x):
                key = "X"
                updatekey(keysposresults[0][30])
                window.blit(X,((keysposresults[0][30][0]+keysposresults[0][30][2])/2-X.get_width()/2,(keysposresults[0][30][1]+keysposresults[0][30][3])/2-X.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "X":
                end = time()
                keystring += "-..-"
                resetkey(keysposresults[0][30])
                window.blit(X,((keysposresults[0][30][0]+keysposresults[0][30][2])/2-X.get_width()/2,(keysposresults[0][30][1]+keysposresults[0][30][3])/2-X.get_height()/2))
                key = ""
                pygame.display.update()
                #C
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][31][0] and event.pos[0] < keysposresults[0][31][2] and event.pos[1] > keysposresults[0][31][1] and event.pos[1] < keysposresults[0][31][3]) or (event.type == KEYDOWN and event.key == K_c):
                key = "C"
                updatekey(keysposresults[0][31])
                window.blit(C,((keysposresults[0][31][0]+keysposresults[0][31][2])/2-C.get_width()/2,(keysposresults[0][31][1]+keysposresults[0][31][3])/2-C.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "C":
                end = time()
                keystring += "-.-."
                resetkey(keysposresults[0][31])
                window.blit(C,((keysposresults[0][31][0]+keysposresults[0][31][2])/2-C.get_width()/2,(keysposresults[0][31][1]+keysposresults[0][31][3])/2-C.get_height()/2))
                key = ""
                pygame.display.update()
                #V
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][32][0] and event.pos[0] < keysposresults[0][32][2] and event.pos[1] > keysposresults[0][32][1] and event.pos[1] < keysposresults[0][32][3]) or (event.type == KEYDOWN and event.key == K_v):
                key = "V"
                updatekey(keysposresults[0][32])
                window.blit(V,((keysposresults[0][32][0]+keysposresults[0][32][2])/2-V.get_width()/2,(keysposresults[0][32][1]+keysposresults[0][32][3])/2-V.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "V":
                end = time()
                keystring += "...-"
                resetkey(keysposresults[0][32])
                window.blit(V,((keysposresults[0][32][0]+keysposresults[0][32][2])/2-V.get_width()/2,(keysposresults[0][32][1]+keysposresults[0][32][3])/2-V.get_height()/2))
                key = ""
                pygame.display.update()
                #B
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][33][0] and event.pos[0] < keysposresults[0][33][2] and event.pos[1] > keysposresults[0][33][1] and event.pos[1] < keysposresults[0][33][3]) or (event.type == KEYDOWN and event.key == K_b):
                key = "B"
                updatekey(keysposresults[0][33])
                window.blit(B,((keysposresults[0][33][0]+keysposresults[0][33][2])/2-B.get_width()/2,(keysposresults[0][33][1]+keysposresults[0][33][3])/2-B.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "B":
                end = time()
                keystring += "-..."
                resetkey(keysposresults[0][33])
                window.blit(B,((keysposresults[0][33][0]+keysposresults[0][33][2])/2-B.get_width()/2,(keysposresults[0][33][1]+keysposresults[0][33][3])/2-B.get_height()/2))
                key = ""
                pygame.display.update()
                #N
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][34][0] and event.pos[0] < keysposresults[0][34][2] and event.pos[1] > keysposresults[0][34][1] and event.pos[1] < keysposresults[0][34][3]) or (event.type == KEYDOWN and event.key == K_n):
                key = "N"
                updatekey(keysposresults[0][34])
                window.blit(N,((keysposresults[0][34][0]+keysposresults[0][34][2])/2-N.get_width()/2,(keysposresults[0][34][1]+keysposresults[0][34][3])/2-N.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "N":
                end = time()
                keystring += "-."
                resetkey(keysposresults[0][34])
                window.blit(N,((keysposresults[0][34][0]+keysposresults[0][34][2])/2-N.get_width()/2,(keysposresults[0][34][1]+keysposresults[0][34][3])/2-N.get_height()/2))
                key = ""
                pygame.display.update()
                #M
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][35][0] and event.pos[0] < keysposresults[0][35][2] and event.pos[1] > keysposresults[0][35][1] and event.pos[1] < keysposresults[0][35][3]) or (event.type == KEYDOWN and event.key == K_m):
                key = "M"
                updatekey(keysposresults[0][35])
                window.blit(M,((keysposresults[0][35][0]+keysposresults[0][35][2])/2-M.get_width()/2,(keysposresults[0][35][1]+keysposresults[0][35][3])/2-M.get_height()/2))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "M":
                end = time()
                keystring += "--"
                resetkey(keysposresults[0][35])
                window.blit(M,((keysposresults[0][35][0]+keysposresults[0][35][2])/2-M.get_width()/2,(keysposresults[0][35][1]+keysposresults[0][35][3])/2-Q.get_height()/2))
                key = ""
                pygame.display.update()
                #Backspace
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > keysposresults[0][36][0] and event.pos[0] < keysposresults[0][36][2] and event.pos[1] > keysposresults[0][36][1] and event.pos[1] < keysposresults[0][36][3]) or (event.type == KEYDOWN and event.key == K_BACKSPACE):
                key = "BK"
                updatekey(keysposresults[0][36])
                window.blit(BK,((keysposresults[0][36][0]+keysposresults[0][36][2])/2-BK.get_width()/2,(keysposresults[0][36][1]+keysposresults[0][36][3])/2-BK.get_height()))
                pygame.draw.polygon(window, keytextcol, [(keysposresults[0][36][0]+keysposresults[1]+(-keysposresults[0][36][0]+keysposresults[0][36][2]-2*keysposresults[1])/8,keysposresults[0][35][1]+keysposresults[2]+(keysposresults[0][35][3]-keysposresults[0][35][1]-2*keysposresults[2])*3/4),
                                                      (keysposresults[0][36][0]+keysposresults[1]+(-keysposresults[0][36][0]+keysposresults[0][36][2]-2*keysposresults[1])/4,keysposresults[0][35][1]+keysposresults[2]+(keysposresults[0][35][3]-keysposresults[0][35][1]-2*keysposresults[2])*5/8),
                                                      (keysposresults[0][36][0]+keysposresults[1]+(-keysposresults[0][36][0]+keysposresults[0][36][2]-2*keysposresults[1])/4,keysposresults[0][35][1]+keysposresults[2]+(keysposresults[0][35][3]-keysposresults[0][35][1]-2*keysposresults[2])*7/8)])
                pygame.draw.rect(window, keytextcol, (keysposresults[0][36][0]+keysposresults[1]+(-keysposresults[0][36][0]+keysposresults[0][36][2]-2*keysposresults[1])/4,keysposresults[0][35][1]+keysposresults[2]+(keysposresults[0][35][3]-keysposresults[0][35][1]-2*keysposresults[2])*23/32,
                                                      (-keysposresults[0][36][0]+keysposresults[0][36][2]-2*keysposresults[1])*5/8,(keysposresults[0][35][3]-keysposresults[0][35][1]-2*keysposresults[2])*1/16))
                pygame.display.update()
            elif ((event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYUP)) and key == "BK":
                end = time()
                keystring += "........"
                resetkey(keysposresults[0][36])
                window.blit(BK,((keysposresults[0][36][0]+keysposresults[0][36][2])/2-BK.get_width()/2,(keysposresults[0][36][1]+keysposresults[0][36][3])/2-BK.get_height()))
                pygame.draw.polygon(window, keytextcol, [(keysposresults[0][36][0]+keysposresults[1]+(-keysposresults[0][36][0]+keysposresults[0][36][2]-2*keysposresults[1])/8,keysposresults[0][35][1]+keysposresults[2]+(keysposresults[0][35][3]-keysposresults[0][35][1]-2*keysposresults[2])*3/4),
                                                      (keysposresults[0][36][0]+keysposresults[1]+(-keysposresults[0][36][0]+keysposresults[0][36][2]-2*keysposresults[1])/4,keysposresults[0][35][1]+keysposresults[2]+(keysposresults[0][35][3]-keysposresults[0][35][1]-2*keysposresults[2])*5/8),
                                                      (keysposresults[0][36][0]+keysposresults[1]+(-keysposresults[0][36][0]+keysposresults[0][36][2]-2*keysposresults[1])/4,keysposresults[0][35][1]+keysposresults[2]+(keysposresults[0][35][3]-keysposresults[0][35][1]-2*keysposresults[2])*7/8)])
                pygame.draw.rect(window, keytextcol, (keysposresults[0][36][0]+keysposresults[1]+(-keysposresults[0][36][0]+keysposresults[0][36][2]-2*keysposresults[1])/4,keysposresults[0][35][1]+keysposresults[2]+(keysposresults[0][35][3]-keysposresults[0][35][1]-2*keysposresults[2])*23/32,
                                                      (-keysposresults[0][36][0]+keysposresults[0][36][2]-2*keysposresults[1])*5/8,(keysposresults[0][35][3]-keysposresults[0][35][1]-2*keysposresults[2])*1/16))
                key = ""
                pygame.display.update()

                #The space bar or on-screen key
            elif (event.type == KEYDOWN and event.key == K_SPACE) or (event.type == MOUSEBUTTONDOWN and event.button == 1 and sqrt(((event.pos[0]-mckeycomponents[0][0])**2)+((event.pos[1]-mckeycomponents[0][1])**2)) < mckeycomponents[1]):
                start = time()
                if soundactive:
                    downsound.play(-1)
                key = "KEY"
                pygame.draw.rect(window, keyboardcol, mckeyposresults)
                pygame.draw.rect(window, mckeytopbox, mckeycomponents[3])
                pygame.draw.rect(window, mckeyvertbardark, mckeycomponents[2])
                pygame.draw.circle(window, mckeycircledark, (mckeycomponents[0][0], mckeycomponents[0][1]+2), mckeycomponents[1])
                pygame.display.update()
            elif ((event.type == KEYUP and event.key == K_SPACE) or (event.type == MOUSEBUTTONUP and event.button == 1)) and key == "KEY":
                key = ""
                end = time()
                downsound.stop()
                pygame.draw.rect(window, keyboardcol, mckeyposresults)
                pygame.draw.rect(window, mckeytopbox, mckeycomponents[3])
                pygame.draw.rect(window, mckeyvertbar, mckeycomponents[2])
                pygame.draw.circle(window, mckeycircle, mckeycomponents[0], mckeycomponents[1])
                keytime = end-start
                if keytime < dot_threshold:
                    keystring += "."
                else:
                    keystring += "-"

                pygame.display.update()
        if keystring != oldkeystring:
            pygame.draw.rect(window, charstreambackgroundcol, morsestreamresults[1])
            oldkeystring = keystring
            keylength = 0
            for character in keystring:
                if character == "-":
                    keylength += 2
                if character == ".":
                    keylength += 1
            testkeylength = keylength
            while testkeylength > 15:
                keystring = keystring[1:]
                keylength = 0
                for character in keystring:
                    if character == "-":
                        keylength += 2
                    if character == ".":
                        keylength += 1
                testkeylength = keylength
            startpos = dashstart - keylength * dashwidth
            for character in keystring:
                if character == ".":
                    pygame.draw.circle(window, morsewritecol, (int(startpos), int(morsestreamarea[1]+dashradius)), int(dashradius))
                    startpos += 2*dashwidth
                elif character == "-":
                    pygame.draw.circle(window, morsewritecol, (int(startpos), int(morsestreamarea[1]+dashradius)), int(dashradius))
                    pygame.draw.rect(window, morsewritecol, (int(startpos),int(morsestreamarea[1]),int(2*dashwidth),int(2*dashradius)))
                    pygame.draw.circle(window, morsewritecol, (int(startpos + 2 * dashwidth), int(morsestreamarea[1]+dashradius)), int(dashradius))
                    startpos += 4*dashwidth
            pygame.display.update()

        if keystring != "" and time() - end > letterdelaytime:
            char = getchar(keystring) if getchar(keystring) else ""
            if char != "Backspace" and char != "":
                word += char
                col = morsegoodcol
            elif char == "Backspace":
                if len(word) > 0:
                    word = word[:-1]
                col = morsegoodcol
            else:
                col = morsebadcol

            if word.lower() == exitword.lower():
                pygame.quit()
                exit()
            pygame.draw.rect(window, charstreambackgroundcol, morsestreamresults[1])
            oldkeystring = keystring
            keylength = 0
            for character in keystring:
                if character == "-":
                    keylength += 2
                if character == ".":
                    keylength += 1
            startpos = dashstart - keylength * dashwidth
            for character in keystring:
                if character == ".":
                    pygame.draw.circle(window, col, (int(startpos), int(morsestreamarea[1]+dashradius)), int(dashradius))
                    startpos += 2*dashwidth
                elif character == "-":
                    pygame.draw.circle(window, col, (int(startpos), int(morsestreamarea[1]+dashradius)), int(dashradius))
                    pygame.draw.rect(window, col, (int(startpos),int(morsestreamarea[1]),int(2*dashwidth),int(2*dashradius)))
                    pygame.draw.circle(window, col, (int(startpos + 2 * dashwidth), int(morsestreamarea[1]+dashradius)), int(dashradius))
                    startpos += 4*dashwidth
            theword = charstreamfont.render(word,True,charstreamtextcol)
            while theword.get_width()>charstreamresults[1][2]+20:
                word = word[1:]
                theword = charstreamfont.render(word,True,charstreamtextcol)
            pygame.draw.rect(window, charstreambackgroundcol, charstreamresults[1])
            window.blit(theword,(xres/2-theword.get_width()/2,(charstreamresults[0][1]+charstreamresults[0][1]+charstreamresults[0][3])/2-theword.get_height()/2))
            keystring = ""
            pygame.display.update()
            sleep(0.1)
            pygame.draw.rect(window, charstreambackgroundcol, morsestreamresults[1])
            pygame.display.update()

        #go into demo mode (silently type words) if a set amount of inactive time has passed
        if demoactive:
            if keystring == "" and time() > end + demotime and key == "":
                indemo = True
                currentdemotime = time()
                word = ""
                demoword = demowords[randint(0,len(demowords)-1)].upper()
                demokey = reverse_lookup[demoword[0]]
                if len(demoword) > 1:
                    demoword = demoword[1:]
                else: demoword = ""
                while indemo:
                    #allow the user to escape the demo
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            exit()
                        elif event.type == KEYDOWN and event.key == K_ESCAPE and escapetoclose:
                            pygame.quit()
                            exit()
                        elif event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                            indemo = False
                            keystring = ""
                            word = ""
                            pygame.draw.rect(window, charstreambackgroundcol, morsestreamresults[1])
                            pygame.draw.rect(window, charstreambackgroundcol, charstreamresults[1])
                            pygame.display.update()
                        if event.type == QUIT:
                            pygame.quit()
                            exit()
                    if onapi:
                        if GPIO.input(gpiokey) == False:
                            indemo = False
                            keystring = ""
                            word = ""
                            pygame.draw.rect(window, charstreambackgroundcol, morsestreamresults[1])
                            pygame.draw.rect(window, charstreambackgroundcol, charstreamresults[1])
                            pygame.display.update

                    if indemo:
                        if time() > currentdemotime + dottodash and len(demokey) > 0:
                            keystring += demokey[0]
                            currentdemotime = time()
                            if len(demokey) > 1:
                                demokey = demokey[1:]
                            else: demokey = ""
                        if time() > currentdemotime + codetochar and len(demokey) == 0 and len(keystring) == 0 and len(demoword) > 0:
                            demokey = reverse_lookup[demoword[0]]
                            if len(demoword) > 1:
                                demoword = demoword[1:]
                            else: demoword = ""
                        if time() > currentdemotime + wordtodot and len(demoword) == 0 and len(keystring) == 0:
                            word = ""
                            demoword = demowords[randint(0,len(demowords)-1)].upper()

                        #copy and pasting the code that draws morse code to the screen
                        if keystring != oldkeystring:
                            pygame.draw.rect(window, charstreambackgroundcol, morsestreamresults[1])
                            oldkeystring = keystring
                            keylength = 0
                            for character in keystring:
                                if character == "-":
                                    keylength += 2
                                if character == ".":
                                    keylength += 1
                            testkeylength = keylength
                            while testkeylength > 15:
                                keystring = keystring[1:]
                                keylength = 0
                                for character in keystring:
                                    if character == "-":
                                        keylength += 2
                                    if character == ".":
                                        keylength += 1
                                testkeylength = keylength
                            startpos = dashstart - keylength * dashwidth
                            for character in keystring:
                                if character == ".":
                                    pygame.draw.circle(window, morsewritecol, (int(startpos), int(morsestreamarea[1]+dashradius)), int(dashradius))
                                    startpos += 2*dashwidth
                                elif character == "-":
                                    pygame.draw.circle(window, morsewritecol, (int(startpos), int(morsestreamarea[1]+dashradius)), int(dashradius))
                                    pygame.draw.rect(window, morsewritecol, (int(startpos),int(morsestreamarea[1]),int(2*dashwidth),int(2*dashradius)))
                                    pygame.draw.circle(window, morsewritecol, (int(startpos + 2 * dashwidth), int(morsestreamarea[1]+dashradius)), int(dashradius))
                                    startpos += 4*dashwidth
                            pygame.display.update()

                        #copy and pasting the code that draws characters to the screen based on the dots and dashes
                        if keystring != "" and len(demokey) == 0 and time() > currentdemotime + codetochar:
                            char = getchar(keystring) if getchar(keystring) else ""
                            if char != "Backspace" and char != "":
                                word += char
                                col = morsegoodcol
                            elif char == "Backspace":
                                if len(word) > 0:
                                    word = word[:-1]
                                col = morsegoodcol
                            else:
                                col = morsebadcol

                            if word.lower() == exitword.lower():
                                pygame.quit()
                                exit()
                            pygame.draw.rect(window, charstreambackgroundcol, morsestreamresults[1])
                            oldkeystring = keystring
                            keylength = 0
                            for character in keystring:
                                if character == "-":
                                    keylength += 2
                                if character == ".":
                                    keylength += 1
                            startpos = dashstart - keylength * dashwidth
                            for character in keystring:
                                if character == ".":
                                    pygame.draw.circle(window, col, (int(startpos), int(morsestreamarea[1]+dashradius)), int(dashradius))
                                    startpos += 2*dashwidth
                                elif character == "-":
                                    pygame.draw.circle(window, col, (int(startpos), int(morsestreamarea[1]+dashradius)), int(dashradius))
                                    pygame.draw.rect(window, col, (int(startpos),int(morsestreamarea[1]),int(2*dashwidth),int(2*dashradius)))
                                    pygame.draw.circle(window, col, (int(startpos + 2 * dashwidth), int(morsestreamarea[1]+dashradius)), int(dashradius))
                                    startpos += 4*dashwidth
                            theword = charstreamfont.render(word,True,charstreamtextcol)
                            while theword.get_width()>charstreamresults[1][2]+20:
                                word = word[1:]
                                theword = charstreamfont.render(word,True,charstreamtextcol)
                            pygame.draw.rect(window, charstreambackgroundcol, charstreamresults[1])
                            window.blit(theword,(xres/2-theword.get_width()/2,(charstreamresults[0][1]+charstreamresults[0][1]+charstreamresults[0][3])/2-theword.get_height()/2))
                            keystring = ""
                            pygame.display.update()
                            sleep(0.1)
                            pygame.draw.rect(window, charstreambackgroundcol, morsestreamresults[1])
                            pygame.display.update()
                            currentdemotime = time()

                start = time()
                end = time()

                """
                NEVER SLEEP - it will lead to unattractive delays getting back to user control
                set 'indemo' flag
                all this is while indemo
                get random word from list
                get char from word
                get keystring of char
                push keystring to screen
                if x time passes push letter to screen, clear codestream
                if y time passes push keystring of next letter


                dottodash = 0.25
                codetochar = 0.75
                wordtodot = 4

                """

while True:
    try:
        main()
    except(SystemExit):
        break

    except Exception as e:
        #this is here so when it breaks at any point in full screen, it won't trap the user in full screen and force a restart
        print("An error has occured:")
        print(e)
        pygame.quit()
