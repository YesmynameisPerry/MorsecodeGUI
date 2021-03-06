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

#the colour of the clear button
clearcol = (200,200,200)

#the colour button edge colours (based off clearcol, don't modify unless you know what you're doing here)
cleartop = (clearcol[0] + 10 if clearcol[0] + 10 < 256 else 255,
          clearcol[1] + 10 if clearcol[1] + 10 < 256 else 255,
          clearcol[2] + 10 if clearcol[2] + 10 < 256 else 255)
clearsid = (clearcol[0] - 10 if clearcol[0] - 10 > -1 else 0,
          clearcol[1] - 10 if clearcol[1] - 10 > -1 else 0,
          clearcol[2] - 10 if clearcol[2] - 10 > -1 else 0)
clearsiddown = (clearcol[0] - 15 if clearcol[0] - 15 > -1 else 0,
              clearcol[1] - 15 if clearcol[1] - 15 > -1 else 0,
              clearcol[2] - 15 if clearcol[2] - 15 > -1 else 0)
clearbot = (clearcol[0] - 20 if clearcol[0] - 20 > -1 else 0,
          clearcol[1] - 20 if clearcol[1] - 20 > -1 else 0,
          clearcol[2] - 20 if clearcol[2] - 20 > -1 else 0)

#the colour of the text on the clear button
cleartextcol = (0,0,0)

#the colour of the mute button
mutecol = (200,200,200)

#the mute button edge colours (based off mutecol, don't modify unless you know what you're doing here)
mutetop = (mutecol[0] + 10 if mutecol[0] + 10 < 256 else 255,
          mutecol[1] + 10 if mutecol[1] + 10 < 256 else 255,
          mutecol[2] + 10 if mutecol[2] + 10 < 256 else 255)
mutesid = (mutecol[0] - 10 if mutecol[0] - 10 > -1 else 0,
          mutecol[1] - 10 if mutecol[1] - 10 > -1 else 0,
          mutecol[2] - 10 if mutecol[2] - 10 > -1 else 0)
mutesiddown = (mutecol[0] - 15 if mutecol[0] - 15 > -1 else 0,
              mutecol[1] - 15 if mutecol[1] - 15 > -1 else 0,
              mutecol[2] - 15 if mutecol[2] - 15 > -1 else 0)
mutebot = (mutecol[0] - 20 if mutecol[0] - 20 > -1 else 0,
          mutecol[1] - 20 if mutecol[1] - 20 > -1 else 0,
          mutecol[2] - 20 if mutecol[2] - 20 > -1 else 0)

#the colour of the images on the mute button
muteimage1col = (0,0,0)
muteimage2col = (255,0,0)

#the colour of the play/pause button
playpausecol = (200,200,200)

#the play/pause button edge colours (based off playpausecol, don't modify unless you know what you're doing here)
playpausetop = (playpausecol[0] + 10 if playpausecol[0] + 10 < 256 else 255,
          playpausecol[1] + 10 if playpausecol[1] + 10 < 256 else 255,
          playpausecol[2] + 10 if playpausecol[2] + 10 < 256 else 255)
playpausesid = (playpausecol[0] - 10 if playpausecol[0] - 10 > -1 else 0,
          playpausecol[1] - 10 if playpausecol[1] - 10 > -1 else 0,
          playpausecol[2] - 10 if playpausecol[2] - 10 > -1 else 0)
playpausesiddown = (playpausecol[0] - 15 if playpausecol[0] - 15 > -1 else 0,
              playpausecol[1] - 15 if playpausecol[1] - 15 > -1 else 0,
              playpausecol[2] - 15 if playpausecol[2] - 15 > -1 else 0)
playpausebot = (playpausecol[0] - 20 if playpausecol[0] - 20 > -1 else 0,
          playpausecol[1] - 20 if playpausecol[1] - 20 > -1 else 0,
          playpausecol[2] - 20 if playpausecol[2] - 20 > -1 else 0)

#the colour of the image on the play/pause button
playpauseimagecol = (0,0,0)

#the colour of the outline of the character stream
charstreamoutlinecol = (150,150,150)

#the colour of the background of the character stream
charstreambackgroundcol = (10,10,10)

#the colour of the text in the character stream
charstreamtextcol = (200,200,200)

#the colour of the character currently being played in playback mode
playbacktextcol = (155,255,155)

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
demowords = ["scouts","morse","code","dot","dash","history","joeys","cubs","venturers","rovers","leaders","baden","powell","brownsea"]
demotime = 4

demoalertbackgroundcol = (100,100,100)
demoalerttextcol = (255,50,50)

#randomly choose words from demowords if True, go through in order and loop if False
randomword = True

#the time (seconds) of the demo 'animations'
dottodash = 0.25
codetochar = 0.75
chartocode = 2
wordtodot = 4

#type this word to make the program close
exitword = "quit"

escapetoclose = True

#this is so the sound can be turned on and off, and have its volume adjusted. Mainly so i don't drive myself crazy with the sound of it during testing
soundactive = True
#the maximum volume is any number greater than 0 (off) and  less than or equal to 1 (maximum sound)
maxsoundvolume = (1)


#DO NOT MODIFY ANYTHING BELOW THIS LINE.
#below this line is checking that any modifications above this line aren't going to break anything.

#checking that all variables that need to exist still exist
#print("Don't forget to check that variables still exist")

#checking all the values in the colours are within the acceptable ranges
colourvars = [clearcol,cleartop,clearsid,clearsiddown,cleartextcol,backgroundcol,keyboardcol,keycol,keytop,keysid,keysiddown,keybot,keytextcol,charstreamoutlinecol,charstreambackgroundcol,charstreamtextcol,morsewritecol,morsegoodcol,morsebadcol,mckeytopbox,mckeyvertbar,mckeycircle,mckeyvertbardark,mckeycircledark]
colourvarnames = ["clearcol","cleartop","clearsid","clearsiddown","cleartextcol","backgroundcol","keyboardcol","keycol","keytop","keysid","keysiddown","keybot","keytextcol","charstreamoutlinecol","charstreambackgroundcol","charstreamtextcol","morsewritecol","morsegoodcol","morsebadcol","mckeytopbox","mckeyvertbar","mckeycircle","mckeyvertbardark","mckeycircledark"]
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

#turning on/off demomode if the list is empty
if len(demowords) == 0:
    demoactive = False
else: demoactive = True
