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


def putBlockInPosition(listOfSteps, timeSinceBlockOccurred, timeForBlockToFallOneField, gameMap, block, differenceInXAxis):
    position = (block.position()[0] + differenceInXAxis, block.position()[1])
    howManyDownsShouldBe = 0
    for i, key in enumerate([letterToKeyName(letter) for letter in listOfSteps]):
        howManyDownsAre = (time.time() - timeSinceBlockOccurred) / timeForBlockToFallOneField
        if key == 'down':
            position = (position[0], position[1] + 1)
            howManyDownsShouldBe += 1
            if howManyDownsAre < howManyDownsShouldBe:
                timeToSleep = (timeForBlockToFallOneField * howManyDownsShouldBe) - (time.time() - timeSinceBlockOccurred) - timeForBlockToFallOneField / 5.5
                if timeToSleep > 0:
                    time.sleep(timeToSleep)

        elif key == 'up':
            gui.typewrite([key])
            time.sleep(timeForBlockToFallOneField / 2.7)
        else:
            if key == 'right':
                position = (position[0] + 1, position[1])
            else:  # left
                position = (position[0] - 1, position[1])
            if blockPossibleInPosition(block, (position[0], position[1] - 1), gameMap.map()):
                gui.typewrite([key])
                time.sleep(timeForBlockToFallOneField / 5.5)
            else:
                gui.keyDown(key)
                time.sleep(timeForBlockToFallOneField / 1.85)
                gui.keyUp(key)
                time.sleep(timeForBlockToFallOneField / 11)
        print(key, position)
    return howManyDownsShouldBe
