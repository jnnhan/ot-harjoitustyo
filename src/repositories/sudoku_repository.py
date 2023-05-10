from pathlib import Path
from sqlite3 import IntegrityError
from entities.sudoku import Sudoku
from database_connection import get_database_connection


class SudokuExistsError(Exception):
    """A class for error raised when creating a new sudoku
        with existing name or puzzle numbers.
    """
    pass


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

    def get_sudoku_id(self, name):
        """Get id of given sudoku.

        Args:
            name: name of the sudoku.

        Returns:
            id of the sudoku.
        """

        cursor = self._connection.cursor()

        cursor.execute("SELECT * FROM sudokus WHERE name=?", (name,))

        return cursor.fetchone()[0]

    def _file_exists(self, file_path):
        Path(file_path).touch()

    def delete_sudokus_from_db(self, sudoku_names):
        cursor = self._connection.cursor()
        for name in sudoku_names:
            cursor.execute("DELETE FROM sudokus WHERE name=?", (name,))
        self._connection.commit()

    def delete_sudokus_from_file(self, file_path, sudoku_names):
        self._file_exists(file_path)
        pointer = 0

        with open(file_path, "r", encoding="utf-8") as file:
            data = file.readlines()

        with open(file_path, "w", encoding="utf-8") as file:
            for row in data:
                if row.strip("\n.") in sudoku_names:
                    pointer += 1
                elif pointer > 0 and pointer < 9:
                    pointer += 1
                elif pointer == 9:
                    pointer = 0
                else:
                    file.write(row)

    def read_sudokus(self, file_path, level):
        """Read sudokus from given file. 
            Add sudokus to the database if amount of numbers is 81 and sudoku contains only numbers.

            Args:
                file_path: path to the sudoku file.
                level: a level of the read sudokus.
        """

        content = ""
        name = ""

        self._file_exists(file_path)

        with open(file_path, "r", encoding="utf-8") as file:
            for row in file:
                row = row.replace("\n", "")
                parts = row.split("\n")

                if parts[0].isnumeric():
                    content += parts[0]
                    if len(content) == 81 and len(name) <= 12:
                        self.create_sudoku(
                            Sudoku(name, content, level))
                        content = ""
                elif parts[0].startswith("."):
                    name = parts[0][1:]

    def write_in_file(self, file_path, sudoku):
        """Write a sudoku in given file.

        Args:
            file_path: Path to the file.
            sudoku: A sudoku object.
        """

        self._file_exists(file_path)
        pointer = 0

        with open(file_path, "a", encoding="utf-8") as file:
            row = "." + sudoku.name
            file.write(row+"\n")

            for x in range(0, 9):
                row = sudoku.puzzle[pointer:(pointer+9)]

                file.write(row+"\n")
                pointer += 9

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
        except IntegrityError:
            raise SudokuExistsError(
                "Sudoku of given name or numbers already exists")

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


sudoku_repo = SudokuRepository(get_database_connection())
