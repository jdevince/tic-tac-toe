import enum

class CellState(enum.Enum):
    Empty = 0,
    Ours = 1,
    Opponent = 2

class TicTacToeBoard:
    # Cell numbers start in top left and go right, one row at a time
    # 1 | 2 | 3
    # 4 | 5 | 6
    # 7 | 8 | 9
    cellOne = CellState.Empty
    cellTwo = CellState.Empty
    cellThree = CellState.Empty
    cellFour = CellState.Empty
    cellFive = CellState.Empty
    cellSix = CellState.Empty
    cellSeven = CellState.Empty
    cellEight = CellState.Empty
    cellNine = CellState.Empty

