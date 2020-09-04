from game_map import GameMap, positionInsideMap, blockPossibleInPosition
from block import Block
from queue import Queue


class GameOver(Exception):
    pass


class NoPlaceFound(Exception):
    pass


class Tetris(Exception):
    def __init__(self, value):
        self.value = value


def sortByGameMapGrade(argument):
    (newGameMap, listOfMoves, place) = argument
    return newGameMap.grade()


def isTetrisPossible(gameMap, block):
    # tetris can be only done with '4' long perpendicular block
    if block.number != 1 or block.currentRotation != 90:
        return False
    # last 4 lines have to be full without last (10th) column
    for y in range(14, 18):
        for x in range(9):
            if gameMap.map()[x][y] != 1:
                False
    return True


def bfs(position, block, mapOfWhoFoundMe, map):
    #print('|||||||||||||||||||||||||||||')
    queue = Queue()
    queue.put(position)
    directions = [((1, 0), 'r'), ((-1, 0), 'l'), ((0, 1), 'd')]  # bloc can go 'down', 'left' or 'right'
    while not queue.empty():
        position = queue.get()
        #print(position)
        for (direction, letter) in directions:
            newPosition = (position[0] + direction[0], position[1] + direction[1])
            if positionInsideMap(newPosition) and mapOfWhoFoundMe[newPosition[0]][newPosition[1]] == '' and \
                    blockPossibleInPosition(block, newPosition, map):
                mapOfWhoFoundMe[newPosition[0]][newPosition[1]] = letter
                queue.put(newPosition)
        #print("------")
    #print("++++++++++++++++++++++")


def dfs(position, mapOfWhoFoundMe):
    letter = mapOfWhoFoundMe[position[0]][position[1]]
    if letter == 's':
        return []
    elif letter == 'l':
        return dfs((position[0] + 1, position[1]), mapOfWhoFoundMe) + [letter]
    elif letter == 'r':
        return dfs((position[0] - 1, position[1]), mapOfWhoFoundMe) + [letter]
    elif letter == 'd':
        return dfs((position[0], position[1] - 1), mapOfWhoFoundMe) + [letter]


def findPossiblePlacesForBlock(gameMap, block):
    # in each field there are coordinates of field that dfs came from to this field
    mapOfWhoFoundMe = [['' for j in range(18)] for i in range(10)]
    mapOfWhoFoundMe[block.position()[0]][block.position()[1]] = 's'  # that indicates that it is starting field
    bfs((block.position()[0], block.position()[1]), block, mapOfWhoFoundMe, gameMap.map())
    #print(mapOfWhoFoundMe)
    result = []
    if block.currentRotation == 0:
        firstMoves = []
    elif block.currentRotation == 90:
        firstMoves = ['u']
    elif block.currentRotation == 180:
        firstMoves = ['u', 'u']
    elif block.currentRotation == 270:
        firstMoves = ['u', 'u', 'u']
    for x in range(10):
        for y in range(18):
            if mapOfWhoFoundMe[x][y] != '' and (y == 17 or not blockPossibleInPosition(block, (x, y + 1), gameMap.map())):
                # if it is possible to put block in this position list of moves have to be saved
                #print(((x, y), dfs((x, y), mapOfWhoFoundMe)))
                result.append(((x, y), firstMoves + dfs((x, y), mapOfWhoFoundMe)))
    return result


def calculatePositionKnowingRotation(gameMap, block):
    if isTetrisPossible(gameMap, block):
        newGameMap = gameMap.addBlock(block, (9, 17))
        listOfMoves = ['u', 'r', 'r', 'r', 'r', 'r', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd',
                       'd', 'd']
        place = (9, 17)
        raise Tetris((newGameMap, listOfMoves, place))
    # list in format [((x1, y1), listOfMoves1), ((x2, y2), listOfMoves2), ...] where first argument is possible place
    # for block and second list of moves to get there
    listOfPossiblePlacesForBlockWithMoves = findPossiblePlacesForBlock(gameMap, block)
    results = []
    for (place, listOfMoves) in listOfPossiblePlacesForBlockWithMoves:
        newGameMap = GameMap(oldGameMap=gameMap)
        newGameMap.addBlock(block, place)
        #print(newGameMap, newGameMap.grade())
        results.append((newGameMap, listOfMoves, place))
    if not results:
        raise NoPlaceFound
    results.sort(key=sortByGameMapGrade)
    return results[-1]


def calculatePosition(gameMap, block):
    listOfResults = []
    for rotation in block.rotations():
        block.currentRotation = rotation
        try:
            newGameMap, listOfMoves, place = calculatePositionKnowingRotation(gameMap, block)
            listOfResults.append((newGameMap, listOfMoves, place))
        except NoPlaceFound:
            pass
        except Tetris as t:
            return t.value
    if not listOfResults:
        raise GameOver
    listOfResults.sort(key=sortByGameMapGrade)
    return listOfResults[-1]


'''
gameMap = GameMap()
block = Block(2)
gameMap, listOfSteps, place = calculatePosition(gameMap, block)
print(gameMap, listOfSteps, place)

print("|||||||||||||||||||||||||||||||||||||||| ")
block = Block(4)
gameMap, listOfSteps, place = calculatePosition(gameMap, block, 1)
print(gameMap, listOfSteps, place)
block = Block(4)
gameMap, listOfSteps, place = calculatePosition(gameMap, block, 1)
print(gameMap, listOfSteps, place)
block = Block(4)
gameMap, listOfSteps, place = calculatePosition(gameMap, block, 0)
print(gameMap, listOfSteps, place)
block = Block(7)
gameMap, listOfSteps, place = calculatePosition(gameMap, block, 0)
print(gameMap, listOfSteps, place)
'''
