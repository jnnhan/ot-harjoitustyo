from entities.sudoku import Sudoku

class SudokuRepository:
    def __init__(self, connection):
        self._connection = connection

    def create_sudoku(self, sudoku):
        cursor = self._connection.cursor()
        cursor.execute("INSERT INTO sudokus (puzzle, level) values (?, ?)", (sudoku.puzzle, sudoku.level))

        self._connection.commit()

    
