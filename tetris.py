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
    print(positionOfLeftUpCorner)
    # start game
    left, top, width, height = gui.locateOnScreen('play_game.png')
    gui.click(left + width // 2, top + height // 2)


timesForBlocksToFallOneFieldDependingOnLevel = [0, 8.85 / 16, 8.00 / 16, 7.47 / 16, 6.53 / 16]


def adjustLevel(screenShot):
    a, b, c = screenShot.getpixel((positionOfLeftUpCorner[0] + 611, positionOfLeftUpCorner[1] + 203))
    if a == 220 and b == 237 and c == 255:
        return 2
    a, b, c = screenShot.getpixel((positionOfLeftUpCorner[0] + 606, positionOfLeftUpCorner[1] + 198))
    if a == 220 and b == 237 and c == 255:
        return 1
    a, b, c = screenShot.getpixel((positionOfLeftUpCorner[0] + 608, positionOfLeftUpCorner[1] + 202))
    if a == 220 and b == 237 and c == 255:
        return 3
    return 4


def play(level):
    points = 0
    timeForBlockToFallOneField = timesForBlocksToFallOneFieldDependingOnLevel[level]
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
    print("game started")
    currentTime = time.time()
    gameMap, listOfSteps, place = calculatePosition(gameMap, currentBlock)
    lastMoveOfPreviousBlock = listOfSteps[-1]
    print('screenShot')
    screenShot = gui.screenshot()
    print(adjustLevel(screenShot), ' level')
    nextBlock = Block(whichBlockIsNext(screenShot))
    howManyDown = putBlockInPosition(listOfSteps, currentTime, timeForBlockToFallOneField, gameMap, currentBlock, 0)
    nr = 0
    print('done', nr)
    time.sleep((timeForBlockToFallOneField * (howManyDown + 1)) - (time.time() - currentTime))
    print(gameMap)
    while True:
        nr += 1
        print("start", nr, nextBlock.number())
        currentTime = time.time()
        currentBlock = nextBlock
        howManyFieldsAreOccupied = gameMap.calculateNumberOfOccupiedFields()
        oldMap = [[0 for j in range(18)] for i in range(10)]
        for x in range(0, 10):
            for y in range(0, 18):
                oldMap[x][y] = gameMap.map()[x][y]
        try:
            # calculates where and how to put block
            gameMap, listOfSteps, place = calculatePosition(gameMap, currentBlock)
        except GameOver:
            break
        print(gameMap.grade(), 'grade')
        if currentBlock.number() == 7:
            time.sleep(0.2)
        else:
            time.sleep(0.4)
        waitForRoundTime(currentTime, timeForBlockToFallOneField)
        print('screenShot')
        startTime = time.time()
        screenShot = gui.screenshot()
        screenShot.save("block" + str(currentBlock.number()) + ".jpg")
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

        timeToSleep = (timeForBlockToFallOneField * howManyDown + 0.4) - (time.time() - currentTime)
        if timeToSleep > 0:
            time.sleep(timeToSleep)

        linesCleared = (howManyFieldsAreOccupied - gameMap.calculateNumberOfOccupiedFields()) / 9
        # if some lines were cleared it has to be looked if level has changed
        if linesCleared:
            newLevel = adjustLevel(screenShot)
            print(newLevel, 'newLevel')
            if newLevel != level:
                level = newLevel
                timeForBlockToFallOneField = timesForBlocksToFallOneFieldDependingOnLevel[level]

        print("next block: ", nextBlock.number())
        print('done', nr)
        print(gameMap)

    print('Game Over!')


# level = int(input('Level: '))
level = 3
startGame()
play(level)
