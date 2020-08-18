from block import Block


def positionInsideMap(position):
    return 0 <= position[0] < 10 and 0 <= position[1] < 18


def blockPossibleInPosition(block, position, map):
    for (x, y) in block.currentComponentParts():
        if not (positionInsideMap((position[0] + x, position[1] + y))) or map[position[0] + x][position[1] + y] == 1:
            return False
    return True


def dfs(position, block, visited, gradesFromCurrentBlock, map):
    visited[position[0]][position[1]] = True
    for (x, y) in block.currentComponentParts():
        gradesFromCurrentBlock[position[0] + x][position[1] + y] = 1
    directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    for direction in directions:
        if positionInsideMap((position[0] + direction[0], position[1] + direction[1])) and \
                not visited[position[0] + direction[0]][position[1] + direction[1]] and blockPossibleInPosition(block, (position[0] + direction[0], position[1] + direction[1]), map):
            dfs((position[0] + direction[0], position[1] + direction[1]), block, visited, gradesFromCurrentBlock, map)


def printMap(map):
    for y in range(18):
        for x in range(10):
            print(map[x][y], end=' ')
        print('')
    print('-=---=')


class GameMap:
    def calculateGrade(self):
        grades = [[0 for j in range(18)] for i in range(10)]
        # test every block
        for i in range(1, 8):
            print('number:', i)
            block = Block(i)
            # and every rotation
            for rotation in block.rotations():
                print('rotation: ', rotation)
                block.currentRotation = rotation
                visited = [[False for j in range(18)] for i in range(10)]
                gradesFromCurrentBlock = [[0 for j in range(18)] for i in range(10)]
                dfs((block.firstPosition()[0], block.firstPosition()[1] + 1), block, visited, gradesFromCurrentBlock, self.__map)
                # add grades from this block to grades
                for x in range(10):
                    for y in range(18):
                        grades[x][y] += gradesFromCurrentBlock[x][y]
                printMap(gradesFromCurrentBlock)
                printMap(visited)
                print("------------------")
            print('++++++++++++++++++++++++++++')
        printMap(grades)
        sumOfGrades = 0
        numberOfFields = 0
        for x in range(10):
            for y in range(18):
                if self.__map[x][y] == 2:
                    # if grade of field is 0, so no block can access field, it should be punished by -5
                    if grades[x][y] == 0:
                        sumOfGrades += -5
                    else:
                        sumOfGrades += grades[x][y]
                    numberOfFields += 1
        self.__grade = sumOfGrades / numberOfFields
        print(90 * "*")

    def __init__(self, oldGameMap=None):
        self.__map = [[0 for j in range(18)] for i in range(10)]
        if oldGameMap is None:
            for i in range(9):
                self.__map[i][17] = 2
        else:
            for x in range(10):
                for y in range(18):
                    self.__map[x][y] = oldGameMap.map()[x][y]
        if oldGameMap is None:
            self.calculateGrade()
        else:
            self.__grade = oldGameMap.grade()

    def grade(self):
        return self.__grade

    def map(self):
        return self.__map

    def calculateWhere2s(self):
        for x in range(9):  # last column isn't interesting
            for y in range(18):
                if self.__map[x][y] == 2:
                    self.__map[x][y] = 0
        for x in range(9):  # last column isn't interesting
            for y in range(18):
                if self.__map[x][y] != 1:
                    if y == 17:
                        self.__map[x][y] = 2
                    else:
                        directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
                        for direction in directions:
                            if positionInsideMap((x + direction[0], y + direction[1])) and self.__map[x][y + 1] == 1:
                                self.__map[x][y] = 2

    def clearFullLines(self):
        for y in range(18):
            isLineClear = True
            for x in range(10):
                if self.__map[x][y] != 1:
                    isLineClear = False
                    break
            if isLineClear:
                # move lines that are over this line one down
                if y == 0:
                    for xx in range(10):
                        self.__map[xx][0] = 0
                else:
                    for yy in range(y, 1, -1):
                        for xx in range(10):
                            self.__map[xx][yy] = self.__map[xx][yy - 1]
                    for xx in range(10):
                        self.__map[xx][0] = 0

    def addBlock(self, block, position):
        for (x, y) in block.currentComponentParts():
            if positionInsideMap((position[0] + x, position[1] + y)):
                self.__map[position[0] + x][position[1] + y] = 1
        print(self)
        self.clearFullLines()
        print(self)
        self.calculateWhere2s()
        print(self)

        self.calculateGrade()

    def __str__(self):
        string = ''
        for y in range(18):
            for x in range(10):
                string += str(self.__map[x][y]) + ' '
            string += '\n'
        return string


gameMap = GameMap()
block = Block(1)
gameMap.addBlock(block, (0, 17))
gameMap.addBlock(block, (4, 17))
gameMap.addBlock(block, (0, 16))
gameMap.addBlock(block, (4, 16))
gameMap.addBlock(block, (0, 15))
gameMap.addBlock(block, (4, 15))
gameMap.addBlock(block, (0, 14))
gameMap.addBlock(block, (4, 14))
block.currentRotation = 90
gameMap.addBlock(block, (8, 14))


print(gameMap)
print(gameMap.grade())
