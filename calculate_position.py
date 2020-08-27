from game_map import GameMap, positionInsideMap, blockPossibleInPosition
from block import Block

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


def dfs(position, block, visited, mapOfListsOfMoves, map, currentListOfMoves):
    visited[position[0]][position[1]] = True
    directions = [((0, 1), 'd'), ((1, 0), 'r'), ((-1, 0), 'l')]  # bloc can go 'down', 'left' or 'right'
    for (direction, letter) in directions:
        newPosition = (position[0] + direction[0], position[1] + direction[1])
        currentListOfMoves.append(letter)
        if positionInsideMap(newPosition) and not visited[newPosition[0]][newPosition[1]] and blockPossibleInPosition(
                block, newPosition, map):
            # if it is possible to put block in this position list of moves have to be saved
            if newPosition[1] == 17 or not blockPossibleInPosition(block, (newPosition[0], newPosition[1] + 1), map):
                mapOfListsOfMoves[newPosition[0]][newPosition[1]] = currentListOfMoves.copy()
            dfs(newPosition, block, visited, mapOfListsOfMoves, map, currentListOfMoves)
        currentListOfMoves.pop()

def findPossiblePlacesForBlock(gameMap, block):
    visited = [[False for j in range(18)] for i in range(10)]
    # in each field there is going to be list of moves that can get block there
    mapOfListsOfMoves = [[[] for j in range(18)] for i in range(10)]
    if block.currentRotation == 0:
        currentListOfMoves = []
    elif block.currentRotation == 90:
        currentListOfMoves = ['u']
    elif block.currentRotation == 180:
        currentListOfMoves = ['u', 'u']
    elif block.currentRotation == 270:
        currentListOfMoves = ['u', 'u', 'u']
    dfs(block.position(), block, visited, mapOfListsOfMoves, gameMap.map(), currentListOfMoves)
    result = []
    for x in range(10):
        for y in range(18):
            if mapOfListsOfMoves[x][y]:
                result.append(((x, y), mapOfListsOfMoves[x][y]))
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

gameMap = GameMap()
block = Block(2)
gameMap, listOfSteps, place = calculatePosition(gameMap, block)
print(gameMap, listOfSteps, place)
block = Block(4)
gameMap, listOfSteps, place = calculatePosition(gameMap, block)
print(gameMap, listOfSteps, place)
block = Block(4)
gameMap, listOfSteps, place = calculatePosition(gameMap, block)
print(gameMap, listOfSteps, place)
block = Block(4)
gameMap, listOfSteps, place = calculatePosition(gameMap, block)
print(gameMap, listOfSteps, place)
block = Block(7)
gameMap, listOfSteps, place = calculatePosition(gameMap, block)
print(gameMap, listOfSteps, place)