import webbrowser
import time
import pyautogui as gui
from PIL import Image
from block import Block
from game_map import GameMap
from calculate_position import calculatePosition, GameOver
from put_block_in_position import putBlockInPosition


class NoBlockHasBeenFound(Exception):
    pass


# returns a number from 1 to 7, that represents certain kind of block(pictures in working folder describes which
# number is what) if no block is found exception is raised
def whichBlockIsNext():
    screenShot = gui.screenshot()
    (a, b, c) = screenShot.getpixel((1109, 291))
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

    # waite until game starts
    while gui.locateOnScreen('play_game.png') is None:
        time.sleep(1)
    # fix the level
    left, top, width, height = gui.locateOnScreen('level.png')
    for i in range(level - 1):
        gui.click(left + width // 2, top + height // 2)
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
            currentBlock = Block(whichBlockIsNext())
            break
        except NoBlockHasBeenFound:
            pass
    time.sleep(1.8)
    # game has started
    print("game started")
    currentTime = time.time()
    gameMap, listOfSteps, place = calculatePosition(gameMap, currentBlock)
    nextBlock = Block(whichBlockIsNext())
    howManyDown = putBlockInPosition(listOfSteps, currentTime, timeForBlockToFallOneField)
    nr = 0
    print('done', nr)
    time.sleep((timeForBlockToFallOneField * (howManyDown + 1)) - (time.time() - currentTime) )
    print(gameMap)
    while True:
        nr += 1
        print("start", nr, nextBlock.number())
        currentTime = time.time()
        currentBlock = nextBlock
        nextBlock = Block(whichBlockIsNext())
        try:
            # calculates where and how to put block
            gameMap, listOfSteps, place = calculatePosition(gameMap, currentBlock)
        except GameOver:
            break
        # puts block in the position in the game
        howManyDown = putBlockInPosition(listOfSteps, currentTime, timeForBlockToFallOneField)
        time.sleep((timeForBlockToFallOneField * (howManyDown + 1)) - (time.time() - currentTime) )
        print('done', nr)
        print(gameMap)

    print('Game Over!')


# level = int(input('Level: '))
level = 1
startGame()
play(level)
