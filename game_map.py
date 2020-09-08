from block import Block


def correctPosition(position):
    # y coordinate can be negative (at first position after rotation often is, but block can't go up)
    return 0 <= position[0] < 10 and position[1] < 18


def positionInsideMap(position):
    return 0 <= position[0] < 10 and 0 <= position[1] < 18


def blockPossibleInPosition(block, position, map):
    for (x, y) in block.currentComponentParts():
        if (not (correctPosition((position[0] + x, position[1] + y)))) or (
                position[1] + y >= 0 and map[position[0] + x][position[1] + y] == 1) or position[0] + x == 9:
            return False
    return True


def dfs(position, block, visited, gradesFromCurrentBlock, map):
    visited[position[0]][position[1]] = True
    for (x, y) in block.currentComponentParts():
        if position[1] + y >= 0:
            gradesFromCurrentBlock[position[0] + x][position[1] + y] = 1
    directions = [(1, 0), (-1, 0), (0, 1)]  # block can go down, left or right
    for direction in directions:
        newPosition = (position[0] + direction[0], position[1] + direction[1])
        if positionInsideMap(newPosition) and not visited[newPosition[0]][newPosition[1]] and blockPossibleInPosition(
                block, newPosition, map):
            dfs(newPosition, block, visited, gradesFromCurrentBlock, map)


def printMap(map):
    for y in range(18):
        for x in range(10):
            print(map[x][y], end=' ')
        print('')
    print('-=---=')


class GameMap:
    def calculateAccessibility(self):
        # print(self)
        grades = [[0 for j in range(18)] for i in range(10)]
        # test every block
        for i in range(1, 8):
            # print('number:', i)
            block = Block(i)
            # and every rotation
            for rotation in block.rotations():
                # print('rotation: ', rotation)
                block.currentRotation = rotation
                visited = [[False for j in range(18)] for i in range(10)]
                gradesFromCurrentBlock = [[0 for j in range(18)] for i in range(10)]
                dfs((block.position()), block, visited, gradesFromCurrentBlock, self.__map)
                # printMap(gradesFromCurrentBlock)
                # add grades from this block to grades
                for x in range(10):
                    for y in range(18):
                        grades[x][y] += gradesFromCurrentBlock[x][y]
                # printMap(visited)
                # print("------------------")
            # print('++++++++++++++++++++++++++++')
        for x in range(10):
            for y in range(18):
                # high places should be discouraged
                if y <= 12:
                    grades[x][y] -= 1
                if y <= 5:
                    grades[x][y] -= 1

                # if grade of field is 0, so no block can access field, it should be punished by -20
                if grades[x][y] == 0:
                    grades[x][y] += -20
        # printMap(grades)
        sumOfGrades = 0
        numberOfFields = 0
        for x in range(10):
            for y in range(18):
                if self.__map[x][y] == 2:
                    sumOfGrades += grades[x][y]
                    numberOfFields += 1
        #print(sumOfGrades / numberOfFields)
        return sumOfGrades / numberOfFields

    def calculateAverageDensity(self):
        # calculates weighted average of density of rows in terms of fields with and without blocks
        weights = [i / 10 for i in range(10, 25)] + [2.6, 2.8, 3.0]
        numberOfOccupiedFieldsInMap = 0
        sumOfWeightsOfNotEmptyRows = 0
        for y in range(0, 18):
            numberOfOccupiedFieldsInRow = sum([(self.__map[x][y] == 1) for x in range(0, 10)])
            if numberOfOccupiedFieldsInRow > 0:
                sumOfWeightsOfNotEmptyRows += weights[y]
            numberOfOccupiedFieldsInMap += numberOfOccupiedFieldsInRow * weights[y]
        if sumOfWeightsOfNotEmptyRows == 0:
            return 0
        #print(numberOfOccupiedFieldsInMap, sumOfWeightsOfNotEmptyRows)
        #print(numberOfOccupiedFieldsInMap/sumOfWeightsOfNotEmptyRows)
        return numberOfOccupiedFieldsInMap/sumOfWeightsOfNotEmptyRows

    def calculateGrade(self):

        self.__grade = self.calculateAccessibility() + self.calculateAverageDensity()

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
            self.__grade = 161 / 9
        else:
            self.__grade = oldGameMap.grade()

    def grade(self):
        return self.__grade

    def map(self):
        return self.__map

    def calculateWhere2s(self):
        # erase old 2s
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
        # print(self)
        self.clearFullLines()
        # print(self)
        self.calculateWhere2s()
        # print(self)

        self.calculateGrade()

    def __str__(self):
        string = ''
        for y in range(18):
            for x in range(10):
                string += str(self.__map[x][y]) + ' '
            string += '\n'
        return string


'''

gameMap = GameMap()
block = Block(7)
block.currentRotation = 0
gameMap.addBlock(block, (0, 16))
print(gameMap, gameMap.grade())


gameMap = GameMap()
block = Block(6)
block.currentRotation = 0
gameMap.addBlock(block, (1, 16))
print(gameMap, gameMap.grade())

gameMap = GameMap()
block = Block(6)
block.currentRotation = 0
gameMap.addBlock(block, (2, 16))
print(gameMap, gameMap.grade())

for i in range(1, 8):
    block = Block(i)
    for rotation in block.rotations():
        block.currentRotation = rotation
        gameMap = GameMap()
        gameMap.addBlock(block, block.position())
        print(gameMap)
        print(gameMap.grade())
        print('8'*80)
block = Block(5)
gameMap = GameMap()
gameMap.addBlock(block, (0, 17))
print(gameMap, gameMap.grade())
'''
