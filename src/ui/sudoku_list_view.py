from tkinter import constants, Canvas
import tkinter as tk
from services.sudoku_service import sudoku_service


class SudokuListView:
    """A class responsibe of showing a list of playable sudokus.

        Attributes:
            sudokus: a list of sudoku Objects of a certain level.
            frame: parent tkinter element in which the current view is shown.
            user: currently logged in user.
            counter: a counter for setting a correct amount of space between
                    each sudoku button.
            handle_start_game: shows the UI view for playing the sudoku.
    """

    def __init__(self, root, sudokus, handle_start_game):
        """Initialize the UI class.

        Args:
            root: tkinter frame in which the current view is shown.
            sudokus: a list of Sudoku objects.
            handle_start_game: shows the view for playing a sudoku.
        """
        self._sudokus = sudokus
        self._frame = root
        self._user = sudoku_service.get_current_user()
        self._counter = 1
        self._handle_start_game = handle_start_game

        self._initialize()

    def _start_sudoku_handler(self, sudoku):
        """Handles the showing of UI view for playing sudokus.
            First converts the string format puzzle to sudoku matrix.

        Args:
            sudoku: a Sudoku object.
        """

        puzzle = sudoku_service.numbers_to_puzzle(sudoku)

        self._handle_start_game(puzzle)

    def _initialize_sudoku(self, sudoku, counter):
        """Initialize each sudoku button.
            Shows also the amount of times each sudoku has been solved.

        Args:
            sudoku: a Sudoku object.
            counter: a counter to set a space between buttons. The more existing buttons
                    have been created the higher the counter and thus the new button is 
                    shown lower in the screen.
        """

        start_sudoku_button = tk.Button(
            master=self._frame,
            text=sudoku.name,
            command=lambda: self._start_sudoku_handler(sudoku),
            bg = "#f5b041",
            activebackground="#f39c12",
            width=15
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
            190, ((counter - 1) * 45 + 50), anchor='s', window=playtime_label
        )

    def _initialize(self):
        """Initialize the selection view."""
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
        """Hide the view."""
        self._frame.destroy()
