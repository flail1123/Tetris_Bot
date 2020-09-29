from block import Block



def correctPosition(position):
    # y coordinate can be negative (at first position after rotation often is)
    return 0 <= position[0] < 10 and position[1] < 18


def positionInsideMap(position):
    return 0 <= position[0] < 10 and 0 <= position[1] < 18


def blockPossibleInPosition(block, position, map):
    # returns true if block can be put in this position, so it doesn't stick out of the map and there is no other block
    for (x, y) in block.currentComponentParts():
        if (not (correctPosition((position[0] + x, position[1] + y)))) or (
                position[1] + y >= 0 and map[position[0] + x][position[1] + y] == 1):
            return False
    return True


def dfsAccessibility(position, block, visited, gradesFromCurrentBlock, map):
    visited[position[0]][position[1]] = True
    # adds one to grade of every field that this block would land on if if it's main part was in 'position' position
    for (x, y) in block.currentComponentParts():
        if position[1] + y >= 0:
            gradesFromCurrentBlock[position[0] + x][position[1] + y] = 1
    directions = [(1, 0), (-1, 0), (0, 1)]  # block can go down, left or right
    for direction in directions:
        newPosition = (position[0] + direction[0], position[1] + direction[1])
        if positionInsideMap(newPosition) and not visited[newPosition[0]][newPosition[1]] and blockPossibleInPosition(
                block, newPosition, map):
            dfsAccessibility(newPosition, block, visited, gradesFromCurrentBlock, map)

def printMap(map):
    for y in range(18):
        for x in range(10):
            print(map[x][y], end=' ')
        print('')
    print('-=---=')

def newPosition(position, direction):
    x, y = position
    if direction == 'right':
        return x + 1, y
    if direction == 'left':
        return x - 1, y
    if direction == 'down':
        return x, y + 1
    if direction == 'up':
        return x, y - 1


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
    x, y = position
    # if it is in last column and is trying to go right than it means dfs is finished
    if x == 9 and direction == 'right':
        return 1

    x1, y1 = newPosition(position, direction)
    # there are 3 option that can happen:
    if correctPosition((x1, y1)) and (y1 < 0 or map[x1][y1] != 1):
        positionOnRight = newPosition((x1, y1), turnRight(direction))
        if correctPosition(positionOnRight) and (
                positionOnRight[1] < 0 or map[positionOnRight[0]][positionOnRight[1]] != 1):
            # first option: there is nothing in front and on the right of the block in front
            return 1 + dfsIrregularity(positionOnRight, turnRight(direction), map)
        else:
            # second option: there is nothing in front and there is something on the right of the block in front
            return 1 + dfsIrregularity((x1, y1), direction, map)
    else:
        # third option: there is something in front
        return 1 + dfsIrregularity(position, turnLeft(direction), map)


class GameMap:
    def calculateAccessibilityOfFields(self):
        # returns matrix of grades of accessibility of every field by counting how many blocks in how many rotations
        # can be put on that particular field
        grades = [[0 for j in range(18)] for i in range(10)]
        # test every block
        for i in range(1, 8):
            block = Block(i)
            # and every rotation
            for rotation in block.rotations():
                block.currentRotation = rotation
                visited = [[False for j in range(18)] for i in range(10)]
                gradesFromCurrentBlock = [[0 for j in range(18)] for i in range(10)]
                dfsAccessibility((block.position()), block, visited, gradesFromCurrentBlock, self.__map)
                # add grades from this block to grades
                for x in range(10):
                    for y in range(18):
                        grades[x][y] += gradesFromCurrentBlock[x][y]
        return grades

    def calculateAccessibility(self):
        # returns average accessibility of a field where 19 for a field means the field is occupied or every
        # block in every rotation can access this field, and -250 means that no block can access this field
        grades = self.calculateAccessibilityOfFields()
        sumOfGrades = 0
        for x in range(10):
            for y in range(18):
                # if grade of field is 0, so no block can access field, it should be punished -150
                if grades[x][y] == 0 and self.__map[x][y] == 0:
                    grades[x][y] += -150

                if self.__map[x][y] == 1:
                    grades[x][y] = 19

                sumOfGrades += grades[x][y]
        for x in range(10):
            if grades[x][17] == -150:
                grades[x][17] == -15000
        return sumOfGrades / (10 * 18)

    def calculateDensity(self, heightPenalty):
        # calculates average number of row that occupied field is in
        sumOfRows = 0
        numberOfOccupiedFieldsOnMap = 0
        for y in range(0, 18):
            numberOfOccupiedFieldsInRow = sum([(self.__map[x][y] == 1) for x in range(0, 10)])
            # high fields should be penalize more, so the program doesn't make towers of block
            if y <= 5:
                penalty = heightPenalty * 8
            elif y <= 12:
                penalty = heightPenalty * 4
            else:
                penalty = 0
            sumOfRows += numberOfOccupiedFieldsInRow * (y - penalty)
            numberOfOccupiedFieldsOnMap += numberOfOccupiedFieldsInRow
        if numberOfOccupiedFieldsOnMap == 0:
            return 17
        return sumOfRows / numberOfOccupiedFieldsOnMap

    def calculateIrregularity(self):
        # returns length of line that blocks make, in other words it calculates 'bumpiness' of arrangement of blocks
        position = (0, 17)
        for y in range(0, 18):
            if self.__map[0][y] == 1:
                position = (0, y - 1)
                break
        direction = 'right'
        #print(self, "dfs Irregularity")
        length = dfsIrregularity(position, direction, self.__map)
        return length

    def calculateRightColumnPenalty(self):
        # right column should be free in most cases to do better tetris move
        result = 0
        for y in range(0, 18):
            if self.__map[9][y] == 1:
                result += 1
        return result

    def calculateNumberOfOccupiedFields(self):
        result = 0
        for x in range(0, 10):
            for y in range(0, 18):
                result += self.__map[x][y]
        return result

    def calculateGrade(self, level):
        if level <= 4:
            self.__grade = 15 * (self.calculateAccessibility() - 18) + 2.6 * self.calculateDensity(1) - 1.5 * (
                    self.calculateIrregularity() - 5) - 4.5 * self.calculateRightColumnPenalty() + (
                               0.5) * self.calculateNumberOfOccupiedFields()
        elif level <= 8:
            self.__grade = 15 * (self.calculateAccessibility() - 18) + 3.5 * self.calculateDensity(2) - 1.5 * (
                    self.calculateIrregularity() - 5) - 4.5 * self.calculateRightColumnPenalty()
        else:
            self.__grade = 15 * (self.calculateAccessibility() - 18) + 5 * self.calculateDensity(3) - 1.5 * (
                    self.calculateIrregularity() - 5) - 3 * self.calculateRightColumnPenalty()

    def __init__(self, oldGameMap=None):
        self.__map = [[0 for j in range(18)] for i in range(10)]
        if oldGameMap != None:
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

    def addBlock(self, block, position, level):
        for (x, y) in block.currentComponentParts():
            if positionInsideMap((position[0] + x, position[1] + y)):
                self.__map[position[0] + x][position[1] + y] = 1
        self.clearFullLines()
        self.calculateGrade(level)

    def __str__(self):
        string = ''
        for y in range(18):
            for x in range(10):
                string += str(self.__map[x][y]) + ' '
            string += '\n'
        return string
