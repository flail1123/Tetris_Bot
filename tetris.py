import webbrowser
import time
import pyautogui as gui
from block import Block
from game_map import GameMap
from calculate_position import calculatePosition, GameOver
from put_block_in_position import putBlockInPosition
from game_map import printMap
from adjust_time import adjustTime, waitForRoundTime


class NoBlockHasBeenFound(Exception):
    pass


positionOfLeftUpCorner = None


# returns a number from 1 to 7, that represents certain kind of block(pictures in working folder describes which
# number is what) if no block is found exception is raised
def whichBlockIsNext(screenShot):
    (a, b, c) = screenShot.getpixel((positionOfLeftUpCorner[0] + 520, positionOfLeftUpCorner[1] + 94))
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
    # print(left, top, width, height)
    # determine positionOfLeftUpCorner variable
    positionOfLeftUpCorner = (left - 140, top - 171)
    # print(positionOfLeftUpCorner)
    # start game
    left, top, width, height = gui.locateOnScreen('play_game.png')
    gui.click(left + width // 2, top + height // 2)


timesForBlocksToFallOneFieldDependingOnLevel = [0, 8.85 / 16]


def play(level):
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
    time.sleep(1.8)
    # game has started
    print("game started")
    currentTime = time.time()
    gameMap, listOfSteps, place = calculatePosition(gameMap, currentBlock)
    screenShot = gui.screenshot()
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
        howManyFieldsAreOccupied = gameMap.howManyFieldsAreOccupied()
        oldMap = [[0 for j in range(18)] for i in range(10)]
        for x in range(0, 10):
            for y in range(0, 18):
                oldMap[x][y] = gameMap.map()[x][y]
        try:
            # calculates where and how to put block
            gameMap, listOfSteps, place = calculatePosition(gameMap, currentBlock)
        except GameOver:
            break
        print("place: ", place)
        time.sleep(0.5)
        waitForRoundTime(currentTime, timeForBlockToFallOneField)
        print('screenShot')
        screenShot = gui.screenshot()
        currentTime, extraSteps, differenceInXAxis = adjustTime(currentTime, currentBlock, oldMap,
                                                        positionOfLeftUpCorner, timeForBlockToFallOneField, screenShot)
        listOfSteps = extraSteps + listOfSteps
        try:
            nextBlock = Block(whichBlockIsNext(screenShot))
        except NoBlockHasBeenFound:
            # gameOver
            break

        # puts block in the position in the game
        howManyDown = putBlockInPosition(listOfSteps, currentTime, timeForBlockToFallOneField, gameMap, currentBlock,
                                         differenceInXAxis)

        timeToSleep = (timeForBlockToFallOneField * howManyDown + 0.5) - (time.time() - currentTime)
        if timeToSleep > 0:
            time.sleep(timeToSleep)

        # if some lines were cleared time has to be added
        if howManyFieldsAreOccupied > gameMap.howManyFieldsAreOccupied():
            # more lines cleared at the same time, more time has to be  spent on waiting
            time.sleep(0.25 + 0.05 * ((howManyFieldsAreOccupied - gameMap.howManyFieldsAreOccupied()) / 9))

        print("next block: ", nextBlock.number())
        print('done', nr)
        print(gameMap)

    print('Game Over!')


# level = int(input('Level: '))
level = 1
startGame()
play(level)
