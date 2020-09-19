import time
import pyautogui as gui


def waitForRoundTime(currentTime, timeForBlockToFallOneField):
    howManyDown = (currentTime - time.time()) / timeForBlockToFallOneField
    howManyWholeFieldsDown = (currentTime - time.time()) // timeForBlockToFallOneField
    timeToWait = (1 - (howManyDown - howManyWholeFieldsDown)) * timeForBlockToFallOneField
    time.sleep(timeToWait)


def adjustTime(currentTime, block, oldMap, positionOfLeftUpCorner, timeForBlockToFallOneField, screenShot):
    rotation = block.currentRotation
    block.currentRotation = 0
    startTime = time.time()
    print(time.time())
    # position of left up corner of the game map
    x1, y1 = (positionOfLeftUpCorner[0] + 103, positionOfLeftUpCorner[1] + 46)
    # map = [[0 for j in range(18)] for i in range(10)]
    blocksFields = []
    for x in range(0, 10):
        for y in range(0, 7):
            r, g, b = screenShot.getpixel((x1 + 14 + x * 28, y1 + 14 + y * 28))
            if not (160 < r < 210 and 180 < g < 230 and 210 < b < 255):
                # this block is occupied then
                # map[x][y] = 1
                if oldMap[x][y] == 0:
                    blocksFields.append((x, y))
            # else:
            # map[x][y] = 0
    print(blocksFields)
    theMainField = (-1, -1)
    # looks which fields is the main one for block by trying everyone
    for field in blocksFields:
        print(field, "field")
        isStillAChanceThatThisFieldIsTheMainOne = True
        for part in block.currentComponentParts():
            if not ((field[0] + part[0], field[1] + part[1]) in blocksFields):
                print(field, part)
                isStillAChanceThatThisFieldIsTheMainOne = False
                break
        if isStillAChanceThatThisFieldIsTheMainOne:
            theMainField = field
    print(theMainField)
    if theMainField == (-1, -1):
        print("eerrroooooooooorrrrr")
        return currentTime, [], 0
    howMuchDownBlockIs = theMainField[1] - block.position()[1]
    howMuchDownProgramThinksBlockIs = (startTime - currentTime) / timeForBlockToFallOneField
    newCurrentTime = currentTime + (howMuchDownProgramThinksBlockIs - howMuchDownBlockIs) * timeForBlockToFallOneField
    print(currentTime, newCurrentTime, "time")
    extraSteps = []
    differenceInXAxis = theMainField[0] - block.position()[0]
    print(theMainField[0], block.position()[0], differenceInXAxis, ['r'] * differenceInXAxis, differenceInXAxis > 0)
    if differenceInXAxis < 0:
        print("iiiiiiiiii")
        extraSteps = ['r'] * (-differenceInXAxis)
    elif differenceInXAxis > 0:
        print("jjjjjjjjjj")
        extraSteps = ['l'] * differenceInXAxis
    print('extraSteps: ', extraSteps)
    block.currentRotation = rotation
    return newCurrentTime, extraSteps, differenceInXAxis
    '''  
    print(time.time())
    print("*******************")
    printMap(map)
    print("*******************")
    '''
