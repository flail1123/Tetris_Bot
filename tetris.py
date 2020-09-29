import webbrowser
import time
import pyautogui as gui
from block import Block
from game_map import GameMap
from PIL import Image
from calculate_position import calculatePosition, GameOver
from put_block_in_position import putBlockInPosition
from adjust_time import adjustTime, waitForRoundTime


class NoBlockHasBeenFound(Exception):
    pass


positionOfLeftUpCorner = None


# returns a number from 1 to 7, that represents certain kind of block(pictures in working folder describes which
# number is what) if no block is found exception is raised
def whichBlockIsNext(screenShot):
    a, b, c = screenShot.getpixel((positionOfLeftUpCorner[0] + 520, positionOfLeftUpCorner[1] + 94))
    if (a, b, c) == (245, 112, 0):
        return 1
    if (a, b, c) == (4, 49, 247):
        return 2
    if (a, b, c) == (197, 57, 246):
        return 3
    if (a, b, c) == (244, 242, 0):
        return 4
    if (a, b, c) == (87, 195, 245):
        return 5
    if (a, b, c) == (0, 244, 0):
        return 6
    if (a, b, c) == (247, 36, 0):
        return 7

    raise NoBlockHasBeenFound


def startGame():
    webbrowser.open('https://www.freetetris.org/game.php')
    global positionOfLeftUpCorner
    # waite until game starts
    while gui.locateOnScreen('play_game.png') is None:
        time.sleep(1)
    # fix the level
    left, top, width, height = gui.locateOnScreen('level.png')
    for i in range(level - 1):
        gui.click(left + width // 2, top + height // 2)
    # determine positionOfLeftUpCorner variable
    positionOfLeftUpCorner = (left - 140, top - 171)
    # start game
    left, top, width, height = gui.locateOnScreen('play_game.png')
    gui.click(left + width // 2, top + height // 2)


timesForBlocksToFallWholeMapFieldDependingOnLevel = [0, 8.85, 8.00, 7.47, 6.53, 5.62, 4.84, 4.12, 3.31, 2.52, 1.59]


def whatLevelIsNow(screenShot):
    # returns number of level that it is now
    if screenShot.getpixel((positionOfLeftUpCorner[0] + 605, positionOfLeftUpCorner[1] + 183)) == (220, 237, 255):
        return 1
    if screenShot.getpixel((positionOfLeftUpCorner[0] + 613, positionOfLeftUpCorner[1] + 203)) == (220, 237, 255):
        return 2
    if screenShot.getpixel((positionOfLeftUpCorner[0] + 604, positionOfLeftUpCorner[1] + 193)) == (220, 237, 255):
        return 3
    if screenShot.getpixel((positionOfLeftUpCorner[0] + 608, positionOfLeftUpCorner[1] + 182)) == (220, 237, 255):
        return 4
    if screenShot.getpixel((positionOfLeftUpCorner[0] + 612, positionOfLeftUpCorner[1] + 189)) == (220, 237, 255):
        return 5
    if screenShot.getpixel((positionOfLeftUpCorner[0] + 612, positionOfLeftUpCorner[1] + 193)) == (220, 237, 255):
        return 6
    if screenShot.getpixel((positionOfLeftUpCorner[0] + 604, positionOfLeftUpCorner[1] + 197)) == (220, 237, 255):
        return 7
    if screenShot.getpixel((positionOfLeftUpCorner[0] + 604, positionOfLeftUpCorner[1] + 200)) == (220, 237, 255):
        return 9
    if screenShot.getpixel((positionOfLeftUpCorner[0] + 608, positionOfLeftUpCorner[1] + 196)) == (220, 237, 255):
        return 10
    return 8


def play(level):
    timeForBlockToFallOneField = timesForBlocksToFallWholeMapFieldDependingOnLevel[level] / 16
    gameMap = GameMap()
    # tries finding what is the first block
    while True:
        try:
            screenShot = gui.screenshot()
            currentBlock = Block(whichBlockIsNext(screenShot))
            break
        except NoBlockHasBeenFound:
            pass
    time.sleep(1.9)
    # game has started
    currentTime = time.time()
    gameMap, listOfSteps, place = calculatePosition(gameMap, currentBlock, level)
    lastMoveOfPreviousBlock = listOfSteps[-1]
    screenShot = gui.screenshot()
    nextBlock = Block(whichBlockIsNext(screenShot))
    howManyDown = putBlockInPosition(listOfSteps, currentTime, timeForBlockToFallOneField, gameMap, currentBlock, 0)
    time.sleep((timeForBlockToFallOneField * (howManyDown + 1)) - (time.time() - currentTime))
    while True:
        currentTime = time.time()
        currentBlock = nextBlock
        howManyFieldsAreOccupied = gameMap.calculateNumberOfOccupiedFields()
        # copy current map
        oldMap = [[0 for j in range(18)] for i in range(10)]
        for x in range(0, 10):
            for y in range(0, 18):
                oldMap[x][y] = gameMap.map()[x][y]
        try:
            # calculates where and how to put block
            gameMap, listOfSteps, place = calculatePosition(gameMap, currentBlock, level)
        except GameOver:
            break
        # waits to be sure block has appeared, in most cases block number 7 appears faster
        if currentBlock.number() == 7:
            time.sleep(timeForBlockToFallOneField / 2.8)
        else:
            time.sleep(timeForBlockToFallOneField / 1.4)
        waitForRoundTime(currentTime, timeForBlockToFallOneField)
        screenShot = gui.screenshot()
        startTime = time.time()
        # takes screenshot and changes currentTime so it reflects where the block really is
        currentTime, extraSteps, differenceInXAxis = adjustTime(startTime, currentTime, currentBlock, oldMap,
                                                                positionOfLeftUpCorner, timeForBlockToFallOneField,
                                                                screenShot, lastMoveOfPreviousBlock)
        listOfSteps = extraSteps + listOfSteps
        lastMoveOfPreviousBlock = listOfSteps[-1]
        try:
            nextBlock = Block(whichBlockIsNext(screenShot))
        except NoBlockHasBeenFound:
            # gameOver
            break

        # puts block in the position in the game
        howManyDown = putBlockInPosition(listOfSteps, currentTime, timeForBlockToFallOneField, gameMap, currentBlock,
                                         differenceInXAxis)

        timeToSleep = (timeForBlockToFallOneField * howManyDown + timeForBlockToFallOneField / 1.4) - (
                    time.time() - currentTime)
        if timeToSleep > 0:
            time.sleep(timeToSleep)

        linesCleared = (howManyFieldsAreOccupied - gameMap.calculateNumberOfOccupiedFields()) // 9
        # if some lines were cleared it has to be looked if level has changed
        if linesCleared:
            newLevel = whatLevelIsNow(screenShot)
            if newLevel != level:
                level = newLevel
                timeForBlockToFallOneField = timesForBlocksToFallWholeMapFieldDependingOnLevel[level] / 16

    print('Game Over!')

print("Type level that should be played, new tab in the browser will open, you can skip ad, after that you can't touch mouse or keybord, now you can watch magic happen.")
level = int(input('Level: '))
startGame()
play(level)
