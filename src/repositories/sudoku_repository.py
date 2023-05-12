from sqlite3 import IntegrityError
from entities.sudoku import Sudoku
from database_connection import get_database_connection


class SudokuExistsError(Exception):
    """A class for error raised when creating a new sudoku
        with existing name or puzzle numbers.
    """


class SudokuRepository:
    """A class connecting SudokuService class and database.
        Handles Sudoku objects and sudoku and stats tables in the database.

        Attributes:
            connection: the database connection.
    """

    def __init__(self, connection):
        """Initialize the repository class.

        Args:
            connection: database connection.
        """

        self._connection = connection

    def delete_all_sudokus(self):
        """Delete all sudokus from database.
        """

        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM sudokus")

        self._connection.commit()

    def delete_sudokus_from_db(self, sudoku_ids):
        """Delete certain sudokus from database.

        Args:
            sudoku_ids: A list of one or more sudoku id's to delete.
        """

        cursor = self._connection.cursor()
        for sudoku_id in sudoku_ids:
            cursor.execute("DELETE FROM sudokus WHERE id=?", (sudoku_id,))
        self._connection.commit()

    def create_sudoku(self, sudoku):
        """Save sudoku to the database.
            Don't save if sudoku of the same name or same numbers exists.

        Args:
            sudoku: a Sudoku object
        """

        cursor = self._connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO sudokus (name, puzzle, level) values (?, ?, ?)",
                (sudoku.name, sudoku.puzzle, sudoku.level)
            )

            self._connection.commit()
        except IntegrityError as exc:
            raise SudokuExistsError(
                "Sudoku of given name or numbers already exists") from exc

    def get_all_sudokus(self):
        """Get all the sudokus in the database.

            Returns:
                A list of all the sudoku objects.
        """

        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT * FROM sudokus")

        sudokus = cursor.fetchall()

        return sudokus

    def get_sudokus(self, level):
        """Get all the sudokus of the given level.

        Args:
            level: level of sudokus

        Returns:
            A list of sudoku objects if they match the level.
        """

        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT * FROM sudokus WHERE level=? ORDER BY name", (level,))

        sudokus = cursor.fetchall()

        return [Sudoku(sudoku["name"], sudoku["puzzle"], sudoku["level"]) for sudoku in sudokus]

    def get_sudoku_id(self, name):
        """Get id of given sudoku.

        Args:
            name: name of the sudoku.

        Returns:
            id of the sudoku.
        """

        cursor = self._connection.cursor()

        cursor.execute("SELECT id FROM sudokus WHERE name=?", (name,))

        sudoku_id = cursor.fetchone()

        return sudoku_id[0] if sudoku_id else None


sudoku_repo = SudokuRepository(get_database_connection())
