from pathlib import Path
from sqlite3 import IntegrityError
from entities.sudoku import Sudoku
from database_connection import get_database_connection


class SudokuExistsError(Exception):
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

    def get_playtime(self, user_id, sudoku_id):
        """Get number of times given sudoku has been solved by user.

        Args:
            user_id: id of currently logged in user.
            sudoku_id: id of given sudoku.

        Returns:
            playtime: amount of times sudoku has been solved
        """

        cursor = self._connection.cursor()

        cursor.execute("SELECT playtime FROM stats WHERE user_id=? AND sudoku_id=?",
                       (user_id, sudoku_id))

        playtime = cursor.fetchone()

        return playtime[0] if playtime else None

    def save_status(self, user_id, sudoku_id):
        """Save or update the playtime of given sudoku.
            If no prior playtime exists, new playtime is 1. Otherwise add 1 to prior playtime.

        Args:
            user_id: currently logged in user.
            sudoku_id: id of recently solved sudoku.
        """

        cursor = self._connection.cursor()

        playtime = self.get_playtime(user_id, sudoku_id)

        if playtime is None:
            cursor.execute(
                "INSERT INTO stats (user_id, sudoku_id, playtime) values (?, ?, ?)",
                (user_id, sudoku_id, 1)
            )
        else:
            cursor.execute(
                "UPDATE stats SET playtime=? WHERE user_id=? AND sudoku_id=?",
                ((playtime+1), user_id, sudoku_id)
            )
        self._connection.commit()

    def get_user_playtime(self, user_id):
        """Get number of times sudokus have been solved by the user.

        Args:
            user_id: id of currently logged in user.

        Returns:
            sudokus: a number of times sudokus have been solved by the user.
        """

        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT SUM(playtime) FROM stats WHERE user_id=?", (user_id,)
        )

        playtime = cursor.fetchone()

        return playtime[0]

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
        """Ensure that the given file exists by creating it if it doesn't exist already.

            Args:
                file_path: A path to the file.
        """

        Path(file_path).touch()

    def read_sudokus(self, file_path, level):
        """Read sudokus from given file. 
            Add sudokus to the database if amount of numbers is 81 and sudoku contains only numbers.

            Args:
                file_path: path to the sudoku file.
                level: a level of the read sudokus.
        """

        content = ""

        self._file_exists(file_path)

        with open(file_path, "r", encoding="utf-8") as file:
            for row in file:
                row = row.replace("\n", "")
                parts = row.split("\n")

                if parts[0].startswith("."):
                    if len(content) == 81 and len(parts[0]) <= 12:
                        self.create_sudoku(
                            Sudoku(parts[0][1:], content, level))
                        content = ""
                else:
                    if content == "" or content.isnumeric():
                        content += parts[0]

    def write_in_file(self, file_path, sudoku):
        """Write a sudoku in given file.

        Args:
            file_path: Path to the file.
            sudoku: A sudoku object.
        """

        self._file_exists(file_path)
        pointer = 0

        with open(file_path, "a", encoding="utf-8") as file:
            for x in range(0, 9):
                row = sudoku.puzzle[pointer:(pointer+9)]

                file.write(row+"\n")
                pointer += 9

            row = "." + sudoku.name
            file.write(row+"\n")

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
