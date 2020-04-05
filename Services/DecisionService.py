import random

def getNextMove(currentBoard):
    availableMoves = __getAvailableMoves(currentBoard)
    return random.choice(availableMoves)

def __getAvailableMoves(currentBoard):
    availableCells = []

    if (currentBoard.cellOne):
        availableCells.append(1)
    elif (currentBoard.cellTwo):
        availableCells.append(2)
    elif (currentBoard.cellThree):
        availableCells.append(3)
    elif (currentBoard.cellFour):
        availableCells.append(4)
    elif (currentBoard.cellFive):
        availableCells.append(5)
    elif (currentBoard.cellSix):
        availableCells.append(6)
    elif (currentBoard.cellSeven):
        availableCells.append(7)
    elif (currentBoard.cellEight):
        availableCells.append(8)
    elif (currentBoard.cellNine):
        availableCells.append(9)

    return availableCells