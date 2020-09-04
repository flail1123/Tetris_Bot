import pyautogui as gui
import time


def letterToKeyName(letter):
    if letter == 'u':
        return 'up'
    if letter == 'd':
        return 'down'
    if letter == 'l':
        return 'left'
    if letter == 'r':
        return 'right'


def putBlockInPosition(listOfSteps, timeSinceBlockOccured, timeForBlockToFallOneField):
    print("start")
    howManyDownsShouldBe = 0
    for key in [letterToKeyName(letter) for letter in listOfSteps]:
        howManyDownsAre = (time.time() - timeSinceBlockOccured) / timeForBlockToFallOneField
        if key == 'down':
            howManyDownsShouldBe += 1
            if howManyDownsAre < howManyDownsShouldBe:
                time.sleep((timeForBlockToFallOneField * howManyDownsShouldBe) - (time.time() - timeSinceBlockOccured) )

        else:
            gui.typewrite([key])
            time.sleep(0.1)
        print(key)
    print("stop")
    return howManyDownsShouldBe