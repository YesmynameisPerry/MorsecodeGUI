#changing these values will change how the thing behaves/looks
#all sets of three numbers like this => (255,255,255)


#the max length of a dot (seconds)
dot_threshold = 0.15

#the time after the key has been pressed that the computer will try to find a character
letterdelaytime = 0.8

#background colour in rgb
backgroundcol = (255,255,255)

#the background colour of the keyboard
keyboardcol = (100,100,100)

#the key colour
keycol = (200,200,200)

#the key edge colours (based off keycol, don't modify unless you know what you're doing here)
keytop = (keycol[0] + 10 if keycol[0] + 10 < 256 else 255,
          keycol[1] + 10 if keycol[1] + 10 < 256 else 255,
          keycol[2] + 10 if keycol[2] + 10 < 256 else 255)
keysid = (keycol[0] - 10 if keycol[0] - 10 > -1 else 0,
          keycol[1] - 10 if keycol[1] - 10 > -1 else 0,
          keycol[2] - 10 if keycol[2] - 10 > -1 else 0)
keysiddown = (keycol[0] - 15 if keycol[0] - 15 > -1 else 0,
              keycol[1] - 15 if keycol[1] - 15 > -1 else 0,
              keycol[2] - 15 if keycol[2] - 15 > -1 else 0)
keybot = (keycol[0] - 20 if keycol[0] - 20 > -1 else 0,
          keycol[1] - 20 if keycol[1] - 20 > -1 else 0,
          keycol[2] - 20 if keycol[2] - 20 > -1 else 0)

#the colour of the text on the keys of the keyboard
keytextcol = (0,0,0)

#the colour of the outline of the character stream
charstreamoutlinecol = (150,150,150)

#the colour of the background of the character stream
charstreambackgroundcol = (10,10,10)

#the colour of the text in the character stream
charstreamtextcol = (200,255,200)

#the three colours that the morse code can be, typing, recognised, and error
morsewritecol = (155,155,155)
morsegoodcol = (155,255,155)
morsebadcol = (255,155,155)

#the colours of the morse code key's components
mckeytopbox = (0,0,0)
mckeyvertbar = (222,184,135)
mckeycircle = (70,70,70)

#the colours the components of the key change to during the little 'pressed' animation
mckeyvertbardark = (mckeyvertbar[0] - 15 if mckeyvertbar[0] - 10 > -1 else 0,
                    mckeyvertbar[1] - 15 if mckeyvertbar[1] - 10 > -1 else 0,
                    mckeyvertbar[2] - 15 if mckeyvertbar[2] - 10 > -1 else 0)
mckeycircledark = (mckeycircle[0] - 10 if mckeycircle[0] - 10 > -1 else 0,
                   mckeycircle[1] - 10 if mckeycircle[1] - 10 > -1 else 0,
                   mckeycircle[2] - 10 if mckeycircle[2] - 10 > -1 else 0)

#the gpio pin that the physical key is tied to
gpiokey = 4

#the list of words that will cycle through if left alone for 'demotime' amount of time (seconds)
demowords = ["scouts","morse","code","dot","dash","history"]
demotime = 3

#the time (seconds) of the demo 'animations'
dottodash = 0.25
codetochar = 0.75
wordtodot = 4

#type this word to make the program close
exitword = "quit"

#DO NOT MODIFY ANYTHING BELOW THIS LINE.
#below this line is checking that any modifications above this line aren't going to break anything.
colourvars = [backgroundcol,keyboardcol,keycol,keytop,keysid,keysiddown,keybot,keytextcol,charstreamoutlinecol,charstreambackgroundcol,charstreamtextcol,morsewritecol,morsegoodcol,morsebadcol,mckeytopbox,mckeyvertbar,mckeycircle,mckeyvertbardark,mckeycircledark]
colourvarnames = ["backgroundcol","keyboardcol","keycol","keytop","keysid","keysiddown","keybot","keytextcol","charstreamoutlinecol","charstreambackgroundcol","charstreamtextcol","morsewritecol","morsegoodcol","morsebadcol","mckeytopbox","mckeyvertbar","mckeycircle","mckeyvertbardark","mckeycircledark"]
for rgbindex in range(len(colourvars)-1):
    count = 1
    for col in colourvars[rgbindex]:
        if count == 1:
            num = "1st"
        elif count == 2:
            num = "2nd"
        else: num = "3rd"
        if col < 0:
            raise ValueError("Invalid colour in config.py: The " + num + " value: '" + str(col) + "' in " + colourvarnames[rgbindex] + " is too low, the minimum value is 0")
        if col > 255:
            raise ValueError("Invalid colour in config.py: The " + num + " value: '" + str(col) + "' in " + colourvarnames[rgbindex] + " is too high, the maximum value is 255")
        count += 1

if len(demowords) == 0:
    demoactive = False
else: demoactive = True
