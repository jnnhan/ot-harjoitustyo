from entities.sudoku import Sudoku
from repositories.sudoku_repository import (
    sudoku_repo as default_sudoku_repository, SudokuExistsError)


class InvalidSudokuInputError(Exception):
    """A class for error raised by incorrect inputs for new sudoku."""


class SudokuService:
    """A Class for application logic that connects user via UI to
        sudoku repository.

    Attributes:
        sudoku: current or recently played sudoku
        sudoku_repository: SudokuRepository object
    """

    def __init__(
        self,
        sudoku_repository=default_sudoku_repository
    ):
        """Initialize the service class.

        Args:
            sudoku_repository: SudokuRepository object for accessing the db
        """

        self._sudoku = None
        self._sudoku_repository = sudoku_repository

    def get_sudokus(self, level):
        """Get all the sudokus by given level.

        Args: 
            level (int): level for sudokus

        Returns:
            sudokus: a list of Sudoku objects
        """

        sudokus = self._sudoku_repository.get_sudokus(level)
        return sudokus

    def save_sudoku(self, name, level, puzzle):
        """Save a new sudoku to the database if user inputs are valid.

        Args:
            name: a name for the new sudoku.
            level: level of the new sudoku.
            puzzle: new sudoku.

        Raises:
            InvalidSudokuInputError: Raise the error if name of the sudoku is too long or too short,
                if level of sudoku is incorrect or if sudoku contains letters or is invalid length.
            SudokuExistsError: Raise the error if sudoku with same name or numbers exists.
        """

        if len(name) > 12 or len(name) < 1:
            raise InvalidSudokuInputError(
                "Name of sudoku must be 1-12 characters")

        if not level.isnumeric() or int(level) < 1 or int(level) > 3:
            raise InvalidSudokuInputError(
                "Level of sudoku must be a number between 1-3")

        if not puzzle.isnumeric() or len(puzzle) != 81:
            raise InvalidSudokuInputError(
                "Sudoku must contain exactly 81 numbers")

        sudoku = Sudoku(name, puzzle, int(level))
        if not self.check_new_sudoku_input(sudoku):
            raise InvalidSudokuInputError(
                "This sudoku can not be solved")

        try:
            self._sudoku_repository.create_sudoku(sudoku)
        except SudokuExistsError as error:
            raise SudokuExistsError(error) from error

    def get_sudoku_id(self, sudoku):
        """Returns an id for a specific sudoku given by the user.

        Args:
            sudoku: Sudoku object

        Returns:
            sudoku_id: The id for specified sudoku
        """

        sudoku_id = self._sudoku_repository.get_sudoku_id(sudoku.name)

        return sudoku_id

    def numbers_to_puzzle(self, sudoku):
        """Convert sudoku to matrix so it can be solved.
            Save the sudoku object as the current sudoku (self._sudoku).
        Args:
            sudoku: Sudoku object

        Returns:
            puzzle: 9x9 matrix
        """

        numbers = [int(n) for n in sudoku.puzzle]

        puzzle = [[[] for _ in range(9)] for _ in range(9)]

        k = 0
        for i in range(9):
            for j in range(9):
                puzzle[i][j].append(numbers[k])
                k += 1

        self._sudoku = sudoku
        return puzzle

    def get_current_sudoku(self):
        """Get current sudoku.

        Returns:
            sudoku: A sudoku object
        """

        return self._sudoku if self._sudoku else None

    def delete_sudokus(self, sudoku_names):
        """Delete suokus by name.
            Gets id's of given sudokus and deletes corresponding sudokus from the database.

        Args:
            sudoku_names: Names of sudokus to be deleted.
        """
        sudoku_ids = []

        for name in sudoku_names:
            sudoku_ids.append(self._sudoku_repository.get_sudoku_id(name))
        self._sudoku_repository.delete_sudokus_from_db(sudoku_ids)

    def remove_current_sudoku(self):
        """Remove current sudoku. This is done after sudoku is solved and it's status saved.
        """

        self._sudoku = None

    def check_new_sudoku_input(self, sudoku):
        """Check if a new sudoku can be solved.
            Other than zeros no same numbers can occur in a single
            row, column or square.

        Args:
            sudoku: A Sudoku object.

        Returns:
            True, if sudoku can be solved, False otherwise.
        """

        sudoku_matrix = self.numbers_to_puzzle(sudoku)
        return self.check_sudoku(sudoku_matrix)

    def _check_numbers(self, numbers):
        """If the sudoku exists in the database, check if the list
            contains all the numbers 1-9 once.
            If sudoku doesn't exist, check if it contains duplicate
            numbers other than zeros.

        Args:
            numbers: A list of numbers

        Returns:
            True, if the numbers are valid, otherwise False.
        """

        if len(numbers) > 9:
            return False

        if 0 in numbers and self.get_sudoku_id(self._sudoku) is None:
            numbers = [i for i in numbers if i != 0]
            return len(numbers) == len(set(numbers))

        return set(numbers) == set(range(1, 10))

    def _check_square(self, numbers):
        """Construct a list of numbers from a list of lists.

        Args:
            numbers: A list of lists, example:
            [[1],[4],[8],[3],[2],[6],[5],[7],[9]]

        Returns:
            True, if numbers are valid, otherwise False.
        """
        square = []
        for i in range(9):
            for number in numbers[i]:
                square.append(number)
        return self._check_numbers(square)

    def check_sudoku(self, sudoku):
        """Construct and check each row, column and square in the sudoku.
            If sudoku exists in the database, check if sudoku was solved correctly.
            If it doesn't exist, check if sudoku can be solved.

            Args:
                sudoku: a sudoku matrix.

            Returns:
                True, if all the rows, columns and squares are correct, otherwise False.
        """

        for i in range(9):
            row = []
            for j in range(9):
                for number in sudoku[i][j]:
                    row.append(number)
            if not self._check_numbers(row):
                return False

        for i in range(9):
            column = []
            for col in sudoku:
                for number in col[i]:
                    column.append(number)
            if not self._check_numbers(column):
                return False

        for row in range(3):
            for col in range(3):
                numbers = [sudoku[r][c]
                           for r in range(row * 3, (row + 1) * 3)
                           for c in range(col * 3, (col + 1) * 3)]
                if not self._check_square(numbers):
                    return False
        return True


sudoku_service = SudokuService()
