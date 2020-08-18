allComponentParts = [[], [[(0, 0), (1, 0), (2, 0), (3, 0)], [(0, 0), (0, 1), (0, 2), (0, 3)]],
                     [[(0, 0), (1, 0), (2, 0), (0, 1)], [(0, 0), (1, 0), (1, 1), (1, 2)],
                      [(0, 0), (1, 0), (2, 0), (2, -1)], [(0, 0), (0, 1), (0, 2), (1, 2)]],
                     [[(0, 0), (1, 0), (2, 0), (2, 1)], [(0, 0), (0, 1), (0, 2), (-1, 2)],
                      [(0, 0), (1, 0), (2, 0), (0, -1)], [(0, 0), (0, 1), (0, 2), (1, 0)]],
                     [[(0, 0), (1, 0), (2, 0), (1, 1)], [(0, 0), (0, 1), (0, 2), (-1, 1)],
                      [(0, 0), (1, 0), (2, 0), (1, -1)], [(0, 0), (0, 1), (0, 2), (1, 1)]],
                     [[(0, 0), (1, 0), (1, -1), (2, -1)], [(0, 0), (0, 1), (1, 1), (1, 2)]],
                     [[(0, 0), (1, 0), (1, 1), (2, 1)], [(0, 0), (0, 1), (1, 0), (1, -1)]],
                     [[(0, 0), (0, 1), (1, 0), (1, 1)]]]
allRotations = [[], [0, 90], [0, 90, 180, 270], [0, 90, 180, 270], [0, 90, 180, 270], [0, 90], [0, 90], [0]]

allFirstPositions = [(), (3, 0), (3, 0), (3, 0), (3, 0), (3, 1), (3, 0), (4, 0)]

class Block:
    def __init__(self, number):
        self.__componentPart = allComponentParts[number]  # this is a list of component parts at every rotation
        self.__rotations = allRotations[number]  # this is a list of roations of block for example [0, 90, 180, 270]
        self.currentRotation = 0
        self.__firstPosition = allFirstPositions[number]
        self.__number = number

    def number(self):
        return self.__number

    def currentComponentParts(self):
        if self.currentRotation == 0:
            return self.__componentPart[0]
        elif self.currentRotation == 90:
            return self.__componentPart[1]
        elif self.currentRotation == 180:
            return self.__componentPart[2]
        elif self.currentRotation == 270:
            return self.__componentPart[3]

    def rotations(self):
        return self.__rotations

    def firstPosition(self):
        return self.__firstPosition
