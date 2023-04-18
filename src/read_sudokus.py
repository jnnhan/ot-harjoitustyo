from services.sudoku_service import SudokuService
from config import (
    EASY_FILE_PATH,
    MEDIUM_FILE_PATH,
    HARD_FILE_PATH
)


def read_sudokus():
    service = SudokuService()
    service.read_sudokus(EASY_FILE_PATH, level=1)
    service.read_sudokus(MEDIUM_FILE_PATH, level=2)
    service.read_sudokus(HARD_FILE_PATH, level=3)


if __name__ == "__main__":
    read_sudokus()
