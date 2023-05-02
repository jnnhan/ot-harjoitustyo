from tkinter import ttk, constants, Canvas
import tkinter as tk
from services.sudoku_service import sudoku_service
from ui.sudoku_list_view import SudokuListView


class SudokuSelectView():
    def __init__(self, root, handle_return, handle_start_game, level):
        self._root = root
        self._frame = None
        self._handle_return = handle_return
        self._handle_start_game = handle_start_game
        self._level = level
        self._sudoku_list_frame = None
        self._sudoku_list_view = None
        self._initialize()

    def _return_handler(self):
        self._handle_return()

    def _initialize_sudoku_list(self):
        if self._sudoku_list_view:
            self._sudoku_list_view.destroy()

        sudokus = sudoku_service.get_sudokus(self._level)

        self._sudoku_list_view = SudokuListView(
            self._frame,
            sudokus,
            self._handle_start_game
        )

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        self._frame.canvas = Canvas(
            master=self._frame,
            bg="white",
            width=200,
            height=50,
            highlightthickness=0,
            bd=0
        )
        self._frame.canvas.pack(fill=constants.Y)

        return_button = tk.Button(
            master=self._frame,
            text="Return",
            command=self._return_handler,
            bg="#a3e4d7",
            activebackground="#1abc9c"
        )

        self._frame.canvas.create_window(
            100, 20, anchor='n', window=return_button)

        self._initialize_sudoku_list()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()
