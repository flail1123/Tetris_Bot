from block import Block


def correctPosition(position):
    # y coordinate can be negative (at first position after rotation often is, but block can't go up)
    return 0 <= position[0] < 10 and position[1] < 18


def positionInsideMap(position):
    return 0 <= position[0] < 10 and 0 <= position[1] < 18


def blockPossibleInPosition(block, position, map):
    for (x, y) in block.currentComponentParts():
        if (not (correctPosition((position[0] + x, position[1] + y)))) or (
                position[1] + y >= 0 and map[position[0] + x][position[1] + y] == 1):
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


def newPosition(position, direction):
    x, y = position
    if direction == 'right':
        return (x + 1, y)
    if direction == 'left':
        return (x - 1, y)
    if direction == 'down':
        return (x, y + 1)
    if direction == 'up':
        return (x, y - 1)


def turnRight(direction):
    if direction == 'right':
        return 'down'
    if direction == 'left':
        return 'up'
    if direction == 'down':
        return 'left'
    if direction == 'up':
        return 'right'


def turnLeft(direction):
    if direction == 'right':
        return 'up'
    if direction == 'left':
        return 'down'
    if direction == 'down':
        return 'right'
    if direction == 'up':
        return 'left'


def dfsIrregularity(position, direction, map):
    print(position, direction)
    x, y = position
    if x == 9 and direction == 'right':
        return 1

    x1, y1 = newPosition(position, direction)
    if correctPosition((x1, y1)) and map[x1][y1] != 1:
        positionOnRight = newPosition((x1, y1), turnRight(direction))
        if correctPosition(positionOnRight) and map[positionOnRight[0]][positionOnRight[1]] != 1:
            # print('1')
            return 1 + dfsIrregularity(positionOnRight, turnRight(direction), map)
        else:
            # print('2')
            return 1 + dfsIrregularity((x1, y1), direction, map)
    else:
        # print('3')
        return 1 + dfsIrregularity(position, turnLeft(direction), map)


class GameMap:
    def calculateGrades(self):
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
        return grades

    def calculateAccessibility(self):
        # print(self)
        grades = self.calculateGrades()
        for x in range(10):
            for y in range(18):
                # if grade of field is 0, so no block can access field, it should be punished by -100
                if grades[x][y] == 0:
                    grades[x][y] += -100
        # printMap(grades)
        sumOfGrades = 0
        numberOfFields = 0
        for x in range(10):
            for y in range(18):
                if self.__map[x][y] == 1:
                    sumOfGrades += 19
                else:
                    sumOfGrades += grades[x][y]
                numberOfFields += 1
        # print(sumOfGrades / numberOfFields, "----")
        return sumOfGrades / numberOfFields

    def calculateDensity(self):
        # calculates average number of row that occupied field is in
        sumOfRows = 0
        numberOfOccupiedFieldsOnMap = 0
        for y in range(0, 18):
            numberOfOccupiedFieldsInRow = sum([(self.__map[x][y] == 1) for x in range(0, 10)])
            sumOfRows += numberOfOccupiedFieldsInRow * y
            numberOfOccupiedFieldsOnMap += numberOfOccupiedFieldsInRow
        # print(sumOfRows / numberOfOccupiedFieldsOnMap, "+++")
        return sumOfRows / numberOfOccupiedFieldsOnMap

    def calculateIrregularity(self):
        # returns length of a that ......
        position = (0, 17)
        for y in range(0, 18):
            if self.__map[0][y] == 1:
                position = (0, y - 1)
                break
        direction = 'right'
        print(self, position, direction)
        length = dfsIrregularity(position, direction, self.__map)
        # print(length)
        return length

    def calculateRightColumnPenalty(self):
        result = 0
        for y in range(0, 18):
            if self.__map[9][y] == 1:
                result += 1
        # print(result)
        return result

    def calculateNumberOfOccupiedFields(self):
        result = 0
        for x in range(0, 10):
            for y in range(0, 18):
                result += self.__map[x][y]
        return result

    def calculateGrade(self):
        self.__grade = 10 * (self.calculateAccessibility() - 17) + (1 / 2) * self.calculateDensity() - (
                self.calculateIrregularity() - 5) - 2 * self.calculateRightColumnPenalty() + self.calculateNumberOfOccupiedFields()

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
            self.__grade = 0
        else:
            self.__grade = oldGameMap.grade()

    def grade(self):
        return self.__grade

    def map(self):
        return self.__map

    def calculateWhere2s(self):
        # erase old 2s
        for x in range(10):
            for y in range(18):
                if self.__map[x][y] == 2:
                    self.__map[x][y] = 0
        for x in range(10):
            for y in range(18):
                if self.__map[x][y] != 1:
                    if y == 17:
                        self.__map[x][y] = 2
                    else:
                        # 2 should be in field if there is block under field or blocks\wall are on both left and right
                        if self.__map[x][y + 1] == 1 or (((positionInsideMap((x + 1, y)) and self.__map[x + 1][
                            y] == 1) or not positionInsideMap((x + 1, y))) \
                                                         and ((positionInsideMap((x - 1, y)) and self.__map[x - 1][
                                    y] == 1) or not positionInsideMap((x - 1, y)))):
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

    def howManyFieldsAreOccupied(self):
        result = 0
        for y in range(18):
            for x in range(10):
                result += self.__map[x][y] == 1
        return result


'''

gameMap = GameMap()
block = Block(6)
block.currentRotation = 0
gameMap.addBlock(block, (6, 16))
print(gameMap, gameMap.grade())


block = Block(6)
gameMap.addBlock(block, (0, 14))
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
