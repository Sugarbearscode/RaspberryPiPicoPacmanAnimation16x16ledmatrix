from machine import Pin
from neopixel import NeoPixel
import time

pin = Pin(22, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
np = NeoPixel(pin, 256)   # create NeoPixel driver on GPIO0 for 8 pixels

# 1,1,1 = white
# 1,0,0 = red
# 0,1,9 = green
# 0,0,1 = blue

# this is really simpole script that animates a basic sprite onto a 16 x 16 ws2812 matrix.
# the matrix starts from the bottom left and then goes right, and then up one line and left and so on (i.e. a S pattern repeated).
# this is a PICO script for the Raspberry PI PICO. I designed the sprites using excel and then copied that to a text file and changed the tabs to commas, and the full stops (Which I used to indicate no colour to zero).
#  becuase it only used very basic low level colours the pico can power the whole array using 5v. If you want to make the LED's brighter than you will need an external power source.
#  this script animates a packman ghost.

#  this ghost is split into the head, eyes, body and it's entrails.

#  the lookup matrix is a mapping of the WS2812 matrix to where it would sit relative to the top left position. (i.e. lookupmatrix [0] = top left, [254] = bottom right

lookupmatrix = [255,254,253,252,251,250,249,248,247,246,245,244,243,242,241,240,
                224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,
                223,222,221,220,219,218,217,216,215,214,213,212,211,210,209,208,
                192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,
                191,190,189,188,187,186,185,184,183,182,181,180,179,178,177,176,
                160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,
                159,158,157,156,155,154,153,152,151,150,149,148,147,146,145,144,
                128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,
                127,126,125,124,123,122,121,120,119,118,117,116,115,114,113,112,
                96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,
                95,94,93,92,91,90,89,88,87,86,85,84,83,82,81,80,
                64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,
                63,62,61,60,59,58,57,56,55,54,53,52,51,50,49,48,
                32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,
                31,30,29,28,27,26,25,24,23,22,21,20,19,18,17,16,
                0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

#These are the sprite parts themselves 

ghost_head = [0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0]
ghost_lower1 = [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,1,0,1,1,0,0,1,0,0,0,1,1,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
ghost_lower2 = [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0,0,0,1,1,0,0,0,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
ghost_eyeL = [0,0,1,2,2,1,1,1,2,2,1,1,1,1,0,0,0,0,2,2,2,2,1,2,2,2,2,1,1,1,0,0,0,0,3,3,2,2,1,3,3,2,2,1,1,1,0,0,0,1,3,3,2,2,1,3,3,2,2,1,1,1,1,0,0,1,1,2,2,1,1,1,2,2,1,1,1,1,1,0]
ghost_eyeR = [0,0,1,1,1,1,2,2,1,1,1,2,2,1,0,0,0,0,1,1,1,2,2,2,2,1,2,2,2,2,0,0,0,0,1,1,1,2,2,3,3,1,2,2,3,3,0,0,0,1,1,1,1,2,2,3,3,1,2,2,3,3,1,0,0,1,1,1,1,1,2,2,1,1,1,2,2,1,1,0]


# build the first ghost animation using the above sprite parts 
ghost1 = []
ghost1.extend(ghost_head)
ghost1.extend(ghost_eyeR)
ghost1.extend(ghost_lower1)
# build the seecond ghost animation 
ghost2 = []
ghost2.extend(ghost_head)
ghost2.extend(ghost_eyeL)
ghost2.extend(ghost_lower2)

myimage = []
# myimage.extend(ghost2)

print(len(myimage)) 

animation_step = 0
while (True):

    pixelno = 0
    if animation_step == 0:
        animation_step = 1
        myimage = ghost1
    else:
        animation_step = 0
        myimage = ghost2
            
    while pixelno < 256:

            
        colour = myimage[pixelno]
        actual_pixel_no = lookupmatrix[pixelno]

        if (colour == 0):
            colr = 0
            colg = 0
            colb = 0
        if (colour == 1):
            colr = 1
            colg = 0
            colb = 0
        if (colour == 2):
            colr = 1
            colg = 1
            colb = 1
        if (colour == 3):
            colr = 0
            colg = 0
            colb = 1
        if (colour == 4):
            colr = 5
            colg = 5
            colb = 5
        if (colour == 9):
            colr = 4
            colg = 2
            colb = 1       

        np[actual_pixel_no] = (colr, colg, colb)
        pixelno += 1
    np.write()
    time.sleep_ms(250)



