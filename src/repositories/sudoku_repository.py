from entities.sudoku import Sudoku


class SudokuRepository:
    def __init__(self, connection):
        self._connection = connection

    def create_sudoku(self, sudoku):
        cursor = self._connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO sudokus (name, puzzle, level) values (?, ?, ?)",
                (sudoku.name, sudoku.puzzle, sudoku.level)
            )

            self._connection.commit()
        except:
            pass

    def get_sudokus(self, level):
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM sudokus WHERE level=?", (level,))

        sudokus = cursor.fetchall()

        return [Sudoku(sudoku["name"], sudoku["puzzle"], sudoku["level"]) for sudoku in sudokus]
