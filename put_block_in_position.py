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
    # position of block is the starting position with adjusted x coordinate
    position = (block.position()[0] + differenceInXAxis, block.position()[1])
    # this will count how many 'down' keys were done
    howManyDownsShouldBe = 0
    for i, key in enumerate([letterToKeyName(letter) for letter in listOfSteps]):
        # this calculates how many fields block is already down
        howManyDownsAre = (time.time() - timeSinceBlockOccurred) / timeForBlockToFallOneField
        if key == 'down':
            position = (position[0], position[1] + 1)
            howManyDownsShouldBe += 1
            # if block is higher than it seems from doing 'down' keys
            # than program has to wait for block to go one field down
            if howManyDownsAre < howManyDownsShouldBe:
                timeToSleep = (timeForBlockToFallOneField * howManyDownsShouldBe) - (time.time() - timeSinceBlockOccurred) - timeForBlockToFallOneField / 5.5
                if timeToSleep > 0:
                    time.sleep(timeToSleep)

        elif key == 'up':
            gui.typewrite([key])
            time.sleep(timeForBlockToFallOneField / 2.7)
        else:
            # the position is adjusted
            if key == 'right':
                position = (position[0] + 1, position[1])
            else:  # left
                position = (position[0] - 1, position[1])
            # if there is nothing up from the position that block is going to be than one click is enough
            # but if that is not the case key should be pressed longer than one click to be sure
            if blockPossibleInPosition(block, (position[0], position[1] - 1), gameMap.map()):
                gui.typewrite([key])
                time.sleep(timeForBlockToFallOneField / 5.5)
            else:
                gui.keyDown(key)
                time.sleep(timeForBlockToFallOneField / 1.85)
                gui.keyUp(key)
                time.sleep(timeForBlockToFallOneField / 11)
    return howManyDownsShouldBe
