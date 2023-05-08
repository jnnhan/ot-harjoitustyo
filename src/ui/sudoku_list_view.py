from tkinter import constants, Canvas
import tkinter as tk
from collections import defaultdict
from services.sudoku_service import sudoku_service
from services.user_service import user_service


class SudokuListView:
    """A class responsibe of showing a list of playable sudokus.

        Attributes:
            sudokus: a list of sudoku Objects of a certain level.
            frame: parent tkinter element in which the current view is shown.
            user: currently logged in user.
            counter: a counter for setting a correct amount of space between
                    each sudoku button.
            pages: number of pages needed to show all the sudokus
            current_page: number of currently viewed page. index starts at 0.
            buttons: a dictionary for buttons
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
        self._user = user_service.get_current_user()
        self._counter = 0
        self._pages = (
            len(self._sudokus)//9 if len(self._sudokus) % 9 != 0 else len(self._sudokus)//9 - 1)
        self._current_page = 0
        self._buttons = defaultdict(list)
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

    def _initialize_sudoku(self, sudoku, counter, page):
        """Initialize each sudoku button and add them to list of buttons of 
            correct page using tkinter widgets.
            Shows also the amount of times each sudoku has been solved.

        Args:
            sudoku: a Sudoku object.
            counter: helps keep track of sudokus and their positions on the page.
            page: add sudoku buttons to correct page.
        """

        start_sudoku_button = tk.Button(
            master=self._frame,
            text=sudoku.name,
            command=lambda: self._start_sudoku_handler(sudoku),
            bg="#f5b041",
            activebackground="#f39c12",
            width=9,
            height=2
        )

        if counter < 3:
            y = 1
        elif counter < 6:
            y = 2
        elif counter < 9:
            y = 3

        button = self._frame.canvas.create_window(
            ((400/3)*((counter % 3)+1)-25), (y * 100 + 75), anchor='s', window=start_sudoku_button
        )

        user_id = user_service.get_user_id(self._user)
        sudoku_id = sudoku_service.get_sudoku_id(sudoku)

        playtime = user_service.get_playtime(user_id, sudoku_id)

        playtime_label = tk.Label(
            master=self._frame,
            text=playtime,
            bg="white"
        )

        label = self._frame.canvas.create_window(
            ((400/3)*((self._counter % 3)+1)-25), ((y * 100 + 75) + 25), anchor='s', window=playtime_label
        )

        self._buttons[page].append(button)
        self._buttons[page].append(label)

        if page != self._current_page:
            self._hide_sudoku_buttons(page)

    def _hide_page_buttons(self):
        self._frame.canvas.itemconfig(self._buttons["next"], state="hidden")
        self._frame.canvas.itemconfig(
            self._buttons["previous"], state="hidden")

    def _show_page_buttons(self):
        """Show page selection buttons."""
        self._hide_page_buttons()

        if self._current_page < self._pages:
            self._frame.canvas.itemconfig(
                self._buttons["next"], state="normal")

        if self._current_page >= self._pages:
            self._frame.canvas.itemconfig(
                self._buttons["previous"], state="normal")

    def _show_sudoku_buttons(self):
        """Show sudoku buttons of current page."""
        for button in self._buttons[self._current_page]:
            self._frame.canvas.itemconfig(button, state="normal")

    def _hide_sudoku_buttons(self, page):
        """Hides sudoku buttons on a given page.

        Args:
            page (int): A page in which the sudoku buttons will be hidden.
        """

        for button in self._buttons[page]:
            self._frame.canvas.itemconfig(button, state="hidden")

    def _handle_next_page(self):
        """Shows the view for next page."""
        self._hide_sudoku_buttons(self._current_page)
        self._current_page += 1
        self._show_sudoku_buttons()
        self._show_page_buttons()

    def _handle_previous_page(self):
        """Shows the view for previous page."""
        self._hide_sudoku_buttons(self._current_page)
        self._current_page -= 1
        self._show_sudoku_buttons()
        self._show_page_buttons()

    def _initialize_buttons(self):
        """Initialize page select buttons and save them to list of buttons.
        """
        next_page_button = tk.Button(
            master=self._frame,
            text="next page",
            command=self._handle_next_page,
            bg="#f5b041",
            activebackground="#f39c12",
            width=9,
            height=2
        )
        next = self._frame.canvas.create_window(
            325, 475, anchor='s', window=next_page_button)

        previous_page_button = tk.Button(
            master=self._frame,
            text="previous page",
            command=self._handle_previous_page,
            bg="#f5b041",
            activebackground="#f39c12",
            width=9,
            height=2
        )
        previous = self._frame.canvas.create_window(
            175, 475, anchor='s', window=previous_page_button)

        self._buttons["next"] = next
        self._buttons["previous"] = previous

        self._hide_page_buttons()

    def _initialize(self):
        """Initialize the selection view.
            Initialize the page select buttons, but only show them if there is more than one page.
        """

        self._frame.canvas = Canvas(
            master=self._frame,
            bg="white",
            width=500,
            height=500,
            highlightthickness=0,
            bd=0
        )

        self._frame.canvas.pack(fill=constants.X)

        self._frame.canvas.create_text(
            250, 75, text="Select a sudoku", fill="black", font=('bold', 13))

        self._initialize_buttons()

        if self._current_page != self._pages:
            self._show_page_buttons()

        sudoku_page = 0
        for sudoku in self._sudokus:
            if self._counter >= 9:
                self._counter = 0
                sudoku_page += 1
            self._initialize_sudoku(sudoku, self._counter, sudoku_page)
            self._counter += 1

    def destroy(self):
        """Hide the view."""
        self._frame.destroy()
