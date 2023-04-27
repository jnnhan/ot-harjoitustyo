from tkinter import ttk, constants, Canvas
import tkinter as tk
from services.sudoku_service import sudoku_service


class SudokuListView:
    def __init__(self, root, sudokus, handle_start_game):
        self._sudokus = sudokus
        self._sudoku_frame = None
        self._user = sudoku_service.get_current_user()
        self._frame = root
        self._counter = 1
        self._handle_start_game = handle_start_game

        self._initialize()

    def _start_sudoku_handler(self, sudoku):
        puzzle = sudoku_service.numbers_to_puzzle(sudoku)

        self._handle_start_game(puzzle)

    def _initialize_sudoku(self, sudoku, counter):
        start_sudoku_button = tk.Button(
            master=self._frame,
            text=sudoku.name,
            command=lambda: self._start_sudoku_handler(sudoku),
            bg="#d1f2eb"
        )

        self._frame.canvas.create_window(
            100, ((counter - 1) * 45 + 50), anchor='s', window=start_sudoku_button
        )

        user_id = sudoku_service.get_user_id(self._user)
        sudoku_id = sudoku_service.get_sudoku_id(sudoku)

        playtime = sudoku_service.get_playtime(user_id, sudoku_id)

        playtime_label = tk.Label(
            master=self._frame,
            text=playtime,
            bg="white"
        )

        self._frame.canvas.create_window(
            180, ((counter - 1) * 45 + 50), anchor='s', window=playtime_label
        )
        
    def _initialize(self):
        self._frame.canvas = Canvas(
            master=self._frame,
            bg="white",
            width=200,
            height=200,
            highlightthickness=0,
            bd=0
        )

        self._frame.canvas.pack(fill=constants.X)

        for sudoku in self._sudokus:
            self._initialize_sudoku(sudoku, self._counter)
            self._counter += 1

    def destroy(self):
        self._frame.destroy()
