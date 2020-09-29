import time
import pyautogui as gui


def waitForRoundTime(currentTime, timeForBlockToFallOneField):
    howManyDown = (currentTime - time.time()) / timeForBlockToFallOneField
    howManyWholeFieldsDown = (currentTime - time.time()) // timeForBlockToFallOneField
    timeToWait = (1 - (howManyDown - howManyWholeFieldsDown)) * timeForBlockToFallOneField
    time.sleep(timeToWait + timeForBlockToFallOneField / 5.5)


def adjustTime(startTime, currentTime, block, oldMap, positionOfLeftUpCorner, timeForBlockToFallOneField, screenShot, lastMoveOfPreviousBlock):
    # target rotation of block has to be saved and changed to a real one (0) and changed back when program ends
    rotation = block.currentRotation
    block.currentRotation = 0
    # position of left up corner of the game map
    x1, y1 = (positionOfLeftUpCorner[0] + 103, positionOfLeftUpCorner[1] + 46)
    blocksFields = []
    left = 3
    right = 7
    # if the last move of previous was for example right it makes sense to look for block more in the right direction
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
                    # if block is occupied but on the map it isn't than it means that it is part of the block
                    blocksFields.append((x, y))
    theMainField = (-1, -1)
    # looks which fields is the main one for block by trying everyone
    for field in blocksFields:
        isStillAChanceThatThisFieldIsTheMainOne = True
        for part in block.currentComponentParts():
            if not ((field[0] + part[0], field[1] + part[1]) in blocksFields):
                isStillAChanceThatThisFieldIsTheMainOne = False
                break
        if isStillAChanceThatThisFieldIsTheMainOne:
            theMainField = field

    # not currentTime has to be changed so it reflects where the block really is
    howMuchDownBlockIs = theMainField[1] - block.position()[1]
    howMuchDownProgramThinksBlockIs = (startTime - currentTime) / timeForBlockToFallOneField
    newCurrentTime = currentTime + (howMuchDownProgramThinksBlockIs - howMuchDownBlockIs) * timeForBlockToFallOneField
    differenceInXAxis = theMainField[0] - block.position()[0]
    # if there has to be some adjustment to x position of the block than extra moves are going to be added to
    # listOfMoves
    extraSteps = []
    if differenceInXAxis < 0:
        extraSteps = ['r'] * (-differenceInXAxis)
    elif differenceInXAxis > 0:
        extraSteps = ['l'] * differenceInXAxis
    # rotation is put back to what it was
    block.currentRotation = rotation
    return newCurrentTime, extraSteps, differenceInXAxis

