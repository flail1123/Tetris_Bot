import pyautogui as gui

print('CTRL-C to quit')

try:
    while True:
        print('X: ' + str(gui.position().x).rjust(4) + ' Y: ' + str(gui.position().y).rjust(4) + ' Color: ' + str(gui.screenshot().getpixel(gui.position())))
except KeyboardInterrupt:
    print('Done\n')