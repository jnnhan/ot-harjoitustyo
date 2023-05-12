import unittest
from entities.sudoku import Sudoku
from services.sudoku_service import (
    SudokuService,
    InvalidSudokuInputError
)


class FakeSudokuRepository:
    def __init__(self):
        self.sudokus = []
        self.create_sudoku(Sudoku("vaikea", 123456789, 3))
        self.create_sudoku(Sudoku("hurja", 123, 3))

    def get_sudoku_id(self, name):
        for sudoku in self.sudokus:
            if sudoku[1] == name:
                return sudoku[0]
        return None

    def get_sudokus(self, level):
        sudokus = []
        for sudoku in self.sudokus:
            if sudoku[3] == level:
                sudokus.append(sudoku)
        return sudokus if sudokus else None

    def create_sudoku(self, sudoku):
        id = len(self.sudokus) + 1
        self.sudokus.append((id, sudoku.name, sudoku.puzzle, sudoku.level))


class TestSudokuService(unittest.TestCase):
    def setUp(self):
        self.sudoku_service = SudokuService(
            FakeSudokuRepository()
        )

        self.sudoku_huono = Sudoku(
            "huonosudoku",
            "123456789123456789123456789123456789123456789123456789123456789123456789123456789", 1)
        self.sudoku_oikea = Sudoku(
            "oikeasudoku",
            "094000000000000465300072000172040090008000000009000300060100050200300006000080007", 1
        )
        self.sudoku_ratkaistu = Sudoku(
            "kiva",
            "319425768256837914478619532724986153631752849985143276547268391192374685863591427", 1
        )

    def test_check_sudoku_win_works(self):
        puzzle = self.sudoku_service.numbers_to_puzzle(self.sudoku_ratkaistu)

        check_win = self.sudoku_service.check_sudoku(puzzle)

        self.assertEqual(True, check_win)

        puzzle2 = self.sudoku_service.numbers_to_puzzle(self.sudoku_huono)

        check_win2 = self.sudoku_service.check_sudoku(puzzle2)

        self.assertEqual(False, check_win2)

    def test_get_current_sudoku_works(self):
        self.sudoku_service.numbers_to_puzzle(self.sudoku_oikea)

        current_sudoku = self.sudoku_service.get_current_sudoku()

        self.assertEqual(current_sudoku.name, self.sudoku_oikea.name)

        self.sudoku_service.remove_current_sudoku()

        current_sudoku = self.sudoku_service.get_current_sudoku()

        self.assertEqual(current_sudoku, None)

    def test_save_sudoku_works_valid_sudoku(self):
        self.sudoku_service.save_sudoku(
            self.sudoku_oikea.name, str(self.sudoku_oikea.level), self.sudoku_oikea.puzzle)

        sudoku = self.sudoku_service.get_sudokus(self.sudoku_oikea.level)[0]

        self.assertEqual(sudoku[1], self.sudoku_oikea.name)

    def test_save_sudoku_works_invalid_sudoku(self):
        self.assertRaises(
            InvalidSudokuInputError,
            lambda: self.sudoku_service.save_sudoku(
                self.sudoku_oikea.name, str(self.sudoku_oikea.level), "23442"))

        self.assertRaises(
            InvalidSudokuInputError,
            lambda: self.sudoku_service.save_sudoku(
                self.sudoku_oikea.name, "5", self.sudoku_oikea.puzzle))

        self.assertRaises(
            InvalidSudokuInputError,
            lambda: self.sudoku_service.save_sudoku(
                "", str(self.sudoku_oikea.level), self.sudoku_oikea.puzzle))

    def test_get_sudoku_id_works(self):
        sudoku_id = self.sudoku_service.get_sudoku_id(
            Sudoku("vaikea", 123456789, 3))
        toinen_id = self.sudoku_service.get_sudoku_id(Sudoku("hurja", 123, 3))

        self.assertEqual(sudoku_id, 1)
        self.assertEqual(toinen_id, 2)

    def test_get_sudokus_works(self):
        sudokus = self.sudoku_service.get_sudokus(3)
        self.assertEqual(len(sudokus), 2)
        self.assertEqual(sudokus[0][1], "vaikea")
        self.assertEqual(sudokus[1][2], 123)

    def test_numbers_to_puzzle_works(self):
        puzzle = self.sudoku_service.numbers_to_puzzle(self.sudoku_oikea)

        self.assertEqual(len(puzzle), 9)
        self.assertEqual(puzzle[0][0][0], 0)
        self.assertEqual(puzzle[8][8][0], 7)
