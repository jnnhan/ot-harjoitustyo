import unittest
from entities.sudoku import Sudoku
from repositories.sudoku_repository import sudoku_repo, SudokuExistsError


class TestSudokuRepository(unittest.TestCase):
    def setUp(self):
        sudoku_repo.delete_all_sudokus()
        self.sudoku_testi = Sudoku("testinen", "123456789", 1)
        self.vaikea_sudoku = Sudoku("kinkkinen", "000000", 3)
        self.kopio_sudoku = Sudoku("kopio", "000000", 3)

    def test_delete_sudoku_by_id_works(self):
        sudoku_repo.create_sudoku(self.sudoku_testi)
        sudoku_repo.create_sudoku(self.vaikea_sudoku)

        testi_id = sudoku_repo.get_sudoku_id(self.sudoku_testi.name)
        vaikea_id = sudoku_repo.get_sudoku_id(self.vaikea_sudoku.name)

        sudoku_repo.delete_sudokus_from_db([testi_id])

        sudokus = sudoku_repo.get_all_sudokus()

        self.assertEqual(len(sudokus), 1)
        self.assertEqual(sudokus[0][0], vaikea_id)

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
