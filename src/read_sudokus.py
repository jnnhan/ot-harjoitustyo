from repositories.sudoku_repository import sudoku_repo
from config import (
    EASY_FILE_PATH,
    MEDIUM_FILE_PATH,
    HARD_FILE_PATH
)


def read_sudokus():
    sudoku_repo.read_sudokus(EASY_FILE_PATH, level=1)
    sudoku_repo.read_sudokus(MEDIUM_FILE_PATH, level=2)
    sudoku_repo.read_sudokus(HARD_FILE_PATH, level=3)


if __name__ == "__main__":
    read_sudokus()
