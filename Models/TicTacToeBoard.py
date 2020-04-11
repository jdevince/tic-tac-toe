import enum

class CellState(enum.Enum):
    Empty = 0,
    Ours = 1,
    Opponent = 2

class TicTacToeBoard:
    # Cell numbers start in top left and go right, one row at a time
    # 0 | 1 | 2
    # 3 | 4 | 5
    # 6 | 7 | 8
    cells = [CellState.Empty, CellState.Empty, CellState.Empty, CellState.Empty, CellState.Empty, 
                CellState.Empty, CellState.Empty, CellState.Empty, CellState.Empty]
    
    def getEmptyCells(self):
        availableCells = []

        for cellIndex in range(9):
            if (self.cells[cellIndex] == CellState.Empty):
                availableCells.append(cellIndex)

        return availableCells
    
    def isGameOver(self):
        if (self.__areSame(0, 1, 2)
            or self.__areSame(3, 4, 5)
            or self.__areSame(6, 7, 8)
            or self.__areSame(0, 3, 6)
            or self.__areSame(1, 4, 7)
            or self.__areSame(2, 5, 8)
            or self.__areSame(0, 4, 8)
            or self.__areSame(6, 4, 2)):
            return True
        else:
            return False

    def __areSame(self, cellIndexOne, cellIndexTwo, cellIndexThree):
        if (self.cells[cellIndexOne] != CellState.Empty
                and self.cells[cellIndexOne] == self.cells[cellIndexTwo] 
                and self.cells[cellIndexOne] == self.cells[cellIndexThree]):
            return True
        else:
            return False

