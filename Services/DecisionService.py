import random

from Models.TicTacToeBoard import TicTacToeBoard, CellState

def getNextMove(currentBoard):
    availableMoves = currentBoard.getEmptyCells()
    return random.choice(availableMoves)