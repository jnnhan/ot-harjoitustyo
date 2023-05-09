import unittest
import os
from entities.sudoku import Sudoku
from repositories.sudoku_repository import sudoku_repo, SudokuExistsError


class TestSudokuRepository(unittest.TestCase):
    def setUp(self):
        self.dirname = os.path.dirname(__file__)
        sudoku_repo.delete_all_sudokus()
        self.sudoku_testi = Sudoku("testinen", "123456789", 1)
        self.vaikea_sudoku = Sudoku("kinkkinen", "000000", 3)
        self.kopio_sudoku = Sudoku("kopio", "000000", 3)
        self.oikea_sudoku = Sudoku("oikea",
                                   "123456789123456789123456789123456789123456789123456789123456789123456789123456789", 1)

    def clear_file(self, file_path):
        with open(file_path, "w", encoding="utf-8") as file:

            file.write("")

    def test_create_sudoku_fails_puzzle_exists(self):
        sudoku_repo.create_sudoku(self.vaikea_sudoku)
        self.assertRaises(
            SudokuExistsError,
            lambda: sudoku_repo.create_sudoku(self.kopio_sudoku)
        )

        sudokus = sudoku_repo.get_sudokus(3)

        self.assertEqual(len(sudokus), 1)

    def test_get_sudoku_id_works(self):
        sudoku_repo.create_sudoku(self.sudoku_testi)
        sudoku_repo.create_sudoku(self.vaikea_sudoku)

        testi_id = sudoku_repo.get_sudoku_id(self.sudoku_testi.name)
        vaikea_id = sudoku_repo.get_sudoku_id(self.vaikea_sudoku.name)

        self.assertEqual(testi_id, 1)
        self.assertEqual(vaikea_id, 2)

    def test_create_sudoku_works(self):
        sudoku_repo.create_sudoku(self.sudoku_testi)

        sudoku = sudoku_repo.get_sudokus(1)[0]

        self.assertEqual(sudoku.name, self.sudoku_testi.name)
        self.assertEqual(sudoku.puzzle, self.sudoku_testi.puzzle)
        self.assertEqual(sudoku.level, self.sudoku_testi.level)

    def test_read_sudoku_works_invalid_sudokus(self):
        file_path = os.path.join(self.dirname, "..", "test.txt")

        sudoku_repo.read_sudokus(file_path, 1)

        sudokus = sudoku_repo.get_sudokus(1)

        self.assertEqual(len(sudokus), 1)

    def test_write_to_file_works(self):
        file_path = os.path.join(self.dirname, "..", "write_test.txt")
        self.clear_file(file_path)

        sudoku_repo.write_in_file(file_path, self.oikea_sudoku)
        sudoku_repo.read_sudokus(file_path, 1)

        sudoku = sudoku_repo.get_sudokus(1)[0]

        self.assertEqual(self.oikea_sudoku.name, sudoku.name)
        self.assertEqual(len(sudoku.puzzle), 81)

    def test_read_sudoku_works(self):
        file_path = os.path.join(self.dirname, "..", "test.txt")

        sudoku_repo.read_sudokus(file_path, 1)

        sudoku = sudoku_repo.get_sudokus(1)[0]

        self.assertEqual(sudoku.name, "testisudoku")
        self.assertEqual(len(sudoku.puzzle), 81)
        self.assertEqual(sudoku.level, 1)
