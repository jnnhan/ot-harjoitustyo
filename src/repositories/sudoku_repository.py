from sqlite3 import IntegrityError
from entities.sudoku import Sudoku
from database_connection import get_database_connection


class SudokuRepository:
    def __init__(self, connection):
        self._connection = connection

    def delete_all_sudokus(self):
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM sudokus")

        self._connection.commit()

    def get_playtime(self, user_id, sudoku_id):
        cursor = self._connection.cursor()

        cursor.execute("SELECT playtime FROM stats WHERE user_id=? AND sudoku_id=?", (user_id, sudoku_id))

        playtime = cursor.fetchone()

        return playtime[0] if playtime else None

    def save_status(self, user_id, sudoku_id):
        cursor = self._connection.cursor()

        playtime = self.get_playtime(user_id, sudoku_id)

        if playtime == None:
            cursor.execute(
                "INSERT INTO stats (user_id, sudoku_id, playtime) values (?, ?, ?)", (
                    user_id, sudoku_id, 1)
            )
        else:
            cursor.execute(
                "UPDATE stats SET playtime=? WHERE user_id=? AND sudoku_id=?", ((playtime+1), user_id, sudoku_id)
            )
        self._connection.commit()

    def get_user_sudokus(self, user_id):
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT sudokus.id, name, puzzle, level, playtime FROM stats, sudokus WHERE stats.user_id=?", (
                user_id,)
        )

        sudokus = cursor.fetchall()

        return sudokus

    def get_sudoku_id(self, name):
        cursor = self._connection.cursor()

        cursor.execute("SELECT * FROM sudokus WHERE name=?", (name,))

        return cursor.fetchone()[0]

    def read_sudokus(self, file_path, level):
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
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM sudokus WHERE level=?", (level,))

        sudokus = cursor.fetchall()

        return [Sudoku(sudoku["name"], sudoku["puzzle"], sudoku["level"]) for sudoku in sudokus]


sudoku_repo = SudokuRepository(get_database_connection())
