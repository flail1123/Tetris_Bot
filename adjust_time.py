import time
import pyautogui as gui


def waitForRoundTime(currentTime, timeForBlockToFallOneField):
    howManyDown = (currentTime - time.time()) / timeForBlockToFallOneField
    howManyWholeFieldsDown = (currentTime - time.time()) // timeForBlockToFallOneField
    timeToWait = (1 - (howManyDown - howManyWholeFieldsDown)) * timeForBlockToFallOneField
    time.sleep(timeToWait)


def adjustTime(startTime, currentTime, block, oldMap, positionOfLeftUpCorner, timeForBlockToFallOneField, screenShot, lastMoveOfPreviousBlock):
    rotation = block.currentRotation
    block.currentRotation = 0
    # position of left up corner of the game map
    x1, y1 = (positionOfLeftUpCorner[0] + 103, positionOfLeftUpCorner[1] + 46)
    # map = [[0 for j in range(18)] for i in range(10)]
    blocksFields = []
    left = 3
    right = 7
    if lastMoveOfPreviousBlock == 'r':
        right = 10
    elif lastMoveOfPreviousBlock == 'l':
        left = 0
    for x in range(left, right):
        for y in range(0, 7):
            r, g, b = screenShot.getpixel((x1 + 14 + x * 28, y1 + 14 + y * 28))
            if not (160 < r < 210 and 180 < g < 230 and 210 < b < 255):
                # this block is occupied then
                if oldMap[x][y] == 0:
                    blocksFields.append((x, y))
    theMainField = (-1, -1)
    # looks which fields is the main one for block by trying everyone
    for field in blocksFields:
        isStillAChanceThatThisFieldIsTheMainOne = True
        for part in block.currentComponentParts():
            if not ((field[0] + part[0], field[1] + part[1]) in blocksFields):
                print(field, part)
                isStillAChanceThatThisFieldIsTheMainOne = False
                break
        if isStillAChanceThatThisFieldIsTheMainOne:
            theMainField = field
    print(theMainField, 'theMainField')
    if theMainField == (-1, -1):
        return currentTime, [], 0
    howMuchDownBlockIs = theMainField[1] - block.position()[1]

    howMuchDownProgramThinksBlockIs = (startTime - currentTime) / timeForBlockToFallOneField
    newCurrentTime = currentTime + (howMuchDownProgramThinksBlockIs - howMuchDownBlockIs) * timeForBlockToFallOneField
    extraSteps = []
    differenceInXAxis = theMainField[0] - block.position()[0]
    if differenceInXAxis < 0:
        extraSteps = ['r'] * (-differenceInXAxis)
    elif differenceInXAxis > 0:
        extraSteps = ['l'] * differenceInXAxis
    block.currentRotation = rotation
    return newCurrentTime, extraSteps, differenceInXAxis

