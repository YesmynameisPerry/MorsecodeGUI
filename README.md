# MorsecodeGUI
a morse code gui made for a scout thing

Designed to run on a raspberry pi, unknown screen size so everything is just based on fractions of the screen and an assumed standard aspect ratio.

## Features still to add:
- A clear button to remove all text from the screen
- A demo mode that displays random scouty words after x amount of inactive time
- Sound
- Auto-update (a call to check this repo on start to check that it's the latest version)

## How To:

### Close the program:
There's a word called `exitword` in 'config.py'. Type it to close the program.
If you don't want it to be the default of `quit` (because people might type it accidentally), feel free to change it to something else.

### Change the colours:
All colours are represented in the 'config.py' file, inside parentheses with an rgb format, and look like this: `(126,255,0)` Each number represents the red, green, and blue values of a colour in that order, and can be any number in the range from 0 to 255 (inclusive).

For example, `(255,0,0)` would be pure red, as the red value is at its maximum, and blue and green are at their minimum.
Feel free to change any colours you see like that to make it look as pretty as you want.

### Change the demo behaviour
There's a list of words called `demowords` in 'config.py' that are randomly chosen to type out by the program in demo mode.
Feel free to add/subtract your own words to this list to make it fit the theme of what you're going for.

Just ensure that all words are inside quotations `"like this"` or `'like this'` but not `'like this"` `"or this'`

There's also a number right next to`demowords` called `demotime`, which is simply the number of seconds that the program has to be left alone to begin cycling through words. Feel free to change this as well.
To turn off demo mode completely just delete all the words in `demowords`, so it looks like this: `demowords = []` and demo mode will never begin.
