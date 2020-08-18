from game_map import GameMap


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
    #tetris can be only done with '4' long perpendicular block
    if block.number != 1 or block.currentRotation != 90:
        return False
    #last 4 lines have to be full without last (10th) column
    for y in range(14, 18):
        for x in range(9):
            if gameMap.map()[x][y] != 1:
                False
    return True

def findPossiblePlacesForBlock(gameMap, block):


def calculatePositionKnowingRotation(gameMap, block):
    if isTetrisPossible(gameMap, block):
        newGameMap = gameMap.addBlock(block, (9, 17))
        listOfMoves = [1, 'u', 5, 'r', 15, 'd']
        place = (9, 17)
        raise Tetris((newGameMap, listOfMoves, place))
    # list in format [((x1, y1), listOfMoves1), ((x2, y2), listOfMoves2), ...] where first argument is possible place
    # for block and second list of moves to get there
    listOfPossiblePlacesForBlockWithMoves = findPossiblePlacesForBlock(gameMap, block)
    results = []
    for (place, listOfMoves) in listOfPossiblePlacesForBlockWithMoves:
        newGameMap = GameMap(oldGameMap=gameMap)
        newGameMap.addBlock(place)
        results.append((newGameMap, listOfMoves, place))
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
