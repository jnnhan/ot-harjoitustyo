import unittest
import os
from entities.sudoku import Sudoku
from entities.user import User
from repositories.sudoku_repository import sudoku_repo
from repositories.user_repository import user_repo


class TestSudokuRepository(unittest.TestCase):
    def setUp(self):
        sudoku_repo.delete_all_sudokus()
        user_repo.delete_all_users()
        self.sudoku_testi = Sudoku("testinen", "123456789", 1)
        self.vaikea_sudoku = Sudoku("kinkkinen", "000000", 3)
        self.user_kissa = User("kissa", "kisu123")
        self.kopio_sudoku = Sudoku("kopio", "000000", 3)

    def test_create_sudoku_fails_puzzle_exists(self):
        sudoku_repo.create_sudoku(self.vaikea_sudoku)
        sudoku_repo.create_sudoku(self.kopio_sudoku)

        sudokus = sudoku_repo.get_sudokus(3)

        self.assertEqual(len(sudokus), 1)

    def test_save_status_works(self):
        user_repo.create_user(self.user_kissa)
        sudoku_repo.create_sudoku(self.vaikea_sudoku)

        user_id = user_repo.get_user_id(self.user_kissa.username)
        sudoku_id = sudoku_repo.get_sudoku_id(self.vaikea_sudoku.name)

        sudoku_repo.save_status(user_id, sudoku_id)
        stats = sudoku_repo.get_user_sudokus(user_id)[0]

        self.assertEqual(stats[1], self.vaikea_sudoku.name)
        self.assertEqual(stats[4], 1)

        sudoku_repo.save_status(user_id, sudoku_id)
        stats = sudoku_repo.get_user_sudokus(user_id)[0]

        self.assertEqual(stats[4], 2)

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

    def test_read_sudoku_works(self):
        dirname = os.path.dirname(__file__)
        file_path = os.path.join(dirname, "..", "test.txt")

        sudoku_repo.read_sudokus(file_path, 1)

        sudoku = sudoku_repo.get_sudokus(1)[0]

        self.assertEqual(sudoku.name, "testisudoku")
        self.assertEqual(sudoku.puzzle, "12345")
        self.assertEqual(sudoku.level, 1)


