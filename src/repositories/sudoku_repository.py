from sqlite3 import IntegrityError
from entities.sudoku import Sudoku
from database_connection import get_database_connection


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

    def get_user_sudokus(self, user_id):
        """Get all sudokus solved by the user.

        Args:
            user_id: id of currently logged in user.

        Returns:
            sudokus: a list of info about sudokus solved by the user.
        """

        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT sudokus.id, name, puzzle, level, playtime FROM\
            stats, sudokus WHERE stats.user_id=?", (user_id,)
        )

        sudokus = cursor.fetchall()

        return sudokus

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

    def read_sudokus(self, file_path, level):
        """Read sudokus from given file. 
            Add sudokus to the database.

            Args:
                file_path: path to the sudoku file.
                level: a level of the read sudokus.
        """

        content = ""

        with open(file_path, "r", encoding="utf-8") as file:
            for row in file:
                row = row.replace("\n", "")
                parts = row.split("\n")

                if parts[0].startswith("."):
                    self.create_sudoku(
                        Sudoku(parts[0][1:], content, level))
                    content = ""
                else:
                    content += parts[0]

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
            pass

    def get_sudokus(self, level):
        """Get all the sudokus of the given level.

        Args:
            level: level of sudokus

        Returns:
            A list of sudoku objects if they match the level.
        """

        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM sudokus WHERE level=?", (level,))

        sudokus = cursor.fetchall()

        return [Sudoku(sudoku["name"], sudoku["puzzle"], sudoku["level"]) for sudoku in sudokus]


sudoku_repo = SudokuRepository(get_database_connection())
