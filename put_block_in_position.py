import pyautogui as gui
import time
from game_map import blockPossibleInPosition


def letterToKeyName(letter):
    if letter == 'u':
        return 'up'
    if letter == 'd':
        return 'down'
    if letter == 'l':
        return 'left'
    if letter == 'r':
        return 'right'


def putBlockInPosition(listOfSteps, timeSinceBlockOccurred, timeForBlockToFallOneField, gameMap, block):
    print("start")
    position = block.position()
    howManyDownsShouldBe = 0
    for key in [letterToKeyName(letter) for letter in listOfSteps]:
        howManyDownsAre = (time.time() - timeSinceBlockOccurred) / timeForBlockToFallOneField
        if key == 'down':
            position = (position[0], position[1] + 1)
            howManyDownsShouldBe += 1
            if howManyDownsAre < howManyDownsShouldBe:
                timeToSleep = (timeForBlockToFallOneField * howManyDownsShouldBe) - (time.time() - timeSinceBlockOccurred) - 0.1
                if timeToSleep > 0:
                    time.sleep(timeToSleep)

        elif key == 'up':
            gui.typewrite([key])
            time.sleep(0.2)
        else:
            if key == 'right':
                position = (position[0] + 1, position[1])
            else:  # left
                position = (position[0] - 1, position[1])
            if blockPossibleInPosition(block, (position[0], position[1] - 1), gameMap.map()):
                print('+')
                gui.typewrite([key])
                time.sleep(0.10)
            else:
                print('-')
                gui.keyDown(key)
                time.sleep(0.3)
                gui.keyUp(key)
                time.sleep((0.05))
        print(key, position)
    print("stop")
    return howManyDownsShouldBe
