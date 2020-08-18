import webbrowser
import time
import pyautogui as gui
from PIL import Image
from block import Block
from game_map import GameMap
from calculate_position import calculatePosition, GameOver

def startGame(level):
    webbrowser.open('https://www.freetetris.org/game.php')
    # waite until game starts
    while gui.locateOnScreen('play_game.png') == None:
        time.sleep(1)
    # fix the level
    left, top, width, height = gui.locateOnScreen('level.png')
    for i in range(level - 1):
        gui.click(left + width // 2, top + height // 2)
    # start game
    left, top, width, height = gui.locateOnScreen('play_game.png')
    gui.click(left + width // 2, top + height // 2)


# returns a number from 1 to 7, that represents certain kind of block(pictures in working folder describes which number is what)
# if no block is found exception is raised
def whichBlockIsNext():
    print('looking...')
    screenShot = gui.screenshot()
    print(screenShot.getpixel((1109, 291)))
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

    raise Exception('No block has been found')


def play():
    gameMap = GameMap()
    currentBlock = None
    nextBlock = Block(whichBlockIsNext())
    # wait for the first block
    while nextBlock.number() == whichBlockIsNext():
        time.sleep(0.1)
    while True:  # I didn't lose
        currentBlock = nextBlock
        nextBlock = Block(whichBlockIsNext())
        try:
            gameMap, listOfSteps, place = calculatePosition(gameMap, currentBlock)  # calculates where and how to put block
        except GameOver:
            break
        putBlockInPossition(place)  # it puts block in the position in game
    print('Game Over!')

level = int(input('Level: '))
startGame(level)
play()
