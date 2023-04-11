from tkinter import ttk, constants
from ui.game_view import GameView
from services.sudoku_service import SudokuService

class SudokuListView:
    def __init__(self, root, sudokus, handle_start_game):
        self._root = root
        self._sudokus = sudokus
        self._sudoku_frame = None
        self._frame = None
        self._handle_start_game = handle_start_game

        self._initialize()

    def _start_sudoku_handler(self, sudoku_string):
        puzzle = SudokuService().numbers_to_puzzle(sudoku_string)

        self._handle_start_game(puzzle)

    def _initialize_sudoku(self, sudoku):
        sudoku_frame = ttk.Frame(master=self._frame)
        
        start_sudoku_button = ttk.Button(
            master=sudoku_frame,
            text=sudoku.name,
            command=lambda: self._start_sudoku_handler(sudoku.puzzle)
        )

        start_sudoku_button.grid(columnspan=2, sticky=(constants.E, constants.W), padx=5, pady=5)

        sudoku_frame.pack(fill=constants.X)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        for sudoku in self._sudokus:
            self._initialize_sudoku(sudoku)

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()
        