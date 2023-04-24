from tkinter import ttk, constants
from services.sudoku_service import sudoku_service
from ui.sudoku_list_view import SudokuListView


class EasyView():
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
            self._sudoku_list_frame,
            sudokus,
            self._handle_start_game
        )

        self._sudoku_list_view.pack()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        self._sudoku_list_frame = ttk.Frame(master=self._frame)

        return_button = ttk.Button(
            master=self._frame,
            text="Main menu",
            command=self._return_handler
        )

        return_button.grid(columnspan=2, sticky=(
            constants.E, constants.W), padx=5, pady=5)

        self._initialize_sudoku_list()

        self._sudoku_list_frame.grid(
            row=1, column=0, columnspan=3, sticky=constants.EW)

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()
