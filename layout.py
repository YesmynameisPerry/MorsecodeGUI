#where things are laid out on the screen, based on the screen size so it all should scale nicely

#where the keyboard is, returns the keyboard x and y coordinates and x and y length
def keyboardpos(xres,yres):
    ypos = 33*yres/64
    xpos = 5*yres/64
    ylen = 15*yres/32
    xlen = 3*xres/4-xpos
    return(xpos,ypos,xlen,ylen)

#where the keys on the keyboard are, takes the output of keyboardpos and returns the key positions in a list (x left side, y top, x right side, y bottom)
#as well as the length of the keys in both directions / 8
def keyspos(keyboardpos):
    xpos = keyboardpos[0]
    ypos = keyboardpos[1]
    xres = keyboardpos[2]
    yres = keyboardpos[3]
    ylen = yres/4
    xlen = xres/10
    keyslist = []
    for i in range(10):
        keyslist += [(xpos+i*xlen,ypos,xpos+i*xlen+xlen,ypos+ylen)]
    for i in range(10):
        keyslist += [(xpos+i*xlen,ypos+ylen,xpos+i*xlen+xlen,ypos+2*ylen)]
    for i in range(9):
        keyslist += [(xpos+xlen/2+i*xlen,ypos+2*ylen,xpos+xlen/2+i*xlen+xlen,ypos+3*ylen)]
    for i in range(8):
        keyslist += [(xpos+(i+1)*xlen,ypos+3*ylen,xpos+(i+1)*xlen+xlen,ypos+4*ylen)]
    return (keyslist,xlen/8,ylen/8)

#where the on screen morse code key is
def mckeypos(xres,yres):
    ypos = 17*yres/32
    xpos = 7*xres/8-xres/16
    ylen = 7*yres/16
    xlen = xres/8
    return(xpos,ypos,xlen,ylen)

#where the character stream is
def charstreampos(xres,yres):
    xpos = xres/8
    ypos = yres/32
    xlen = 3*xres/4
    ylen = 7*yres/32
    inxpos = xpos + yres/64
    inypos = ypos + yres/64
    inxlen = xlen - yres/32
    inylen = ylen - yres/32
    return((xpos,ypos,xlen,ylen),(inxpos,inypos,inxlen,inylen))

#where the stream of morse code is
def morsestreampos(xres,yres):
    xpos = xres/4
    ypos = 17*yres/64
    xlen = xres/2
    ylen = 3*yres/32
    inxpos = xpos + yres/64
    inypos = ypos + yres/64
    inxlen = xlen - yres/32
    inylen = ylen - yres/32
    innxpos = inxpos + yres/64
    innypos = inypos + yres/64
    innxlen = inxlen - yres/32
    innylen = inylen - yres/32
    return((xpos,ypos,xlen,ylen),(inxpos,inypos,inxlen,inylen),(innxpos,innypos,innxlen,innylen))

#where the on screen key's components are, based on the position and dimensions of the on screen key
def mckeyinnards(mckeypos):
    mccirclerad = int(mckeypos[2]*3/8)
    mccirclex = int(mckeypos[0]+mckeypos[2]/2)
    mccircley = int(mckeypos[1]+mckeypos[3]*3/4)
    mcvertbar = (mckeypos[0]+mckeypos[2]*7/16,mckeypos[1]+mckeypos[3]/8, mckeypos[2]/8, mckeypos[3]*5/8)
    mctopbox = (mckeypos[0]+mckeypos[2]*3/8,mckeypos[1]+mckeypos[3]/16, mckeypos[2]/4, mckeypos[3]/4)
    return ((mccirclex,mccircley),mccirclerad,mcvertbar,mctopbox)

#where the demo alerts appear
def demoalertpos(xres,yres):
    xposl = xres/8
    xposr = 3*xres/4+yres/64
    ypos = 17*yres/64
    xlen = xres/8-yres/64
    ylen = 3*yres/32
    return((xposl,ypos,xlen,ylen),(xposr,ypos,xlen,ylen))

#where the clear button appears
def clearbuttonpos(xres,yres):
    lefpos = 13*xres/32
    toppos = 3*yres/8
    rigpos = lefpos+3*xres/16
    botpos = yres/2
    lspot = (lefpos+yres/16,toppos+yres/16)
    rspot = (rigpos-yres/16,toppos+yres/16)
    innerbox = (lefpos+yres/64,toppos+yres/64,rigpos-lefpos-yres/32,botpos-toppos-yres/32)
    return ((toppos,lefpos,botpos,rigpos),lspot,rspot,innerbox)

#where the play/pause button appears
def playpausepos(xres,yres):
    lefpos = 19*xres/32+yres/64
    rigpos = lefpos + yres/8
    toppos = 3*yres/8
    botpos = yres/2
    mid = ((lefpos+rigpos)/2,(toppos+botpos)/2)
    innerbox = (lefpos+yres/64,toppos+yres/64,rigpos-lefpos-yres/32,botpos-toppos-yres/32)
    return ((lefpos,toppos,rigpos,botpos),mid,innerbox)

#where the mute button appears
def mutebuttonpos(xres,yres):
    lefpos = 13/32*xres-9/64*yres
    rigpos = lefpos + yres/8
    toppos = 3*yres/8
    botpos = yres/2
    mid = (int((lefpos+rigpos)/2),int((toppos+botpos)/2))
    innerbox = (lefpos+yres/64,toppos+yres/64,rigpos-lefpos-yres/32,botpos-toppos-yres/32)
    size1 = int(yres/64)
    size2 = int(yres/32)
    size3 = int(yres/25)
    size4 = int(yres/100)
    size5 = int(yres/40)
    return ((lefpos,toppos,rigpos,botpos),mid,innerbox,size1,size2,size3,size4,size5)
