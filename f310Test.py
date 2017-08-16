'''import pygamepad

pad = pygamepad.Gamepad()


while True:
    pad._read_gamepad()
    if pad.changed:
        print(pad._state)'''

import pygame
import time

pygame.init()
print pygame.joystick.get_count()
j = pygame.joystick.Joystick(0)
j.init()

print 'Initialized Joystick : %s' % j.get_name()

"""
Returns a vector of the following form:
[LThumbstickX, LThumbstickY, Unknown Coupled Axis???, 
RThumbstickX, RThumbstickY, 
Button 1/X, Button 2/A, Button 3/B, Button 4/Y, 
Left Bumper, Right Bumper, Left Trigger, Right Triller,
Select, Start, Left Thumb Press, Right Thumb Press]

Note:
No D-Pad.
Triggers are switches, not variable. 
Your controller may be different
"""

def get():
    out = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    it = 0 #iterator
    pygame.event.pump()

    #Read input from the two joysticks
    for i in range(0, j.get_numaxes()):
        out[it] = j.get_axis(i)
        it+=1
    #Read input from buttons
    for i in range(0, 12):
        out[it] = j.get_button(i)
        it+=1
    return out

def test():
    try:
        while True:
            #print j.get_button(0), j.get_button(1), j.get_button(2), j.get_button(3)
            print get()
            time.sleep(0.1)
    except KeyboardInterrupt:
        j.quit()

test()