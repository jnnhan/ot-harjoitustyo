from tkinter import constants, Canvas, IntVar
import tkinter as tk
from services.sudoku_service import sudoku_service
from services.user_service import user_service


class SudokuListView:
    """A class responsibe of showing a list of playable sudokus.

        Attributes:
            sudokus: a list of Sudoku objects of a certain level.
            frame: parent tkinter element in which the current view is shown.
            user: currently logged in user.
            counter: a counter for setting a correct amount of space between
                    each sudoku button.
            pages: number of pages needed to show all the sudokus
            current_page: number of currently viewed page. index starts at 0.
            handle_start_game: shows the UI view for playing the sudoku.
    """

    def __init__(self, root, level, handle_return, handle_start_game):
        """Initialize the UI class.

        Args:
            root: tkinter frame in which the current view is shown.
            sudokus: a list of Sudoku objects.
            handle_start_game: shows the view for playing a sudoku.
        """

        self._root = root
        self._frame = None
        self._level = level
        self._delete = []
        self._pages = 0
        self._current_page = 0
        self._handle_return = handle_return
        self._handle_start_game = handle_start_game

        self._initialize()

    def _return_handler(self):
        self._handle_return()

    def _start_sudoku_handler(self, sudoku):
        """Handles the showing of UI view for playing sudokus.
            First converts the string format puzzle to sudoku matrix.

        Args:
            sudoku: a Sudoku object.
        """

        puzzle = sudoku_service.numbers_to_puzzle(sudoku)

        self._handle_start_game(puzzle)

    def _delete_handler(self):
        self._show_checkbuttons(self._current_page)
        self._hide_page_buttons()

    def _save_choice(self, name, checkvar):
        if checkvar.get() == 1:
            self._delete.append(name)
        elif name in self._delete and checkvar.get() == 0:
            self._delete.remove(name)

    def _cancel_submit(self):
        self._hide_checkbuttons(self._current_page)
        self._show_page_buttons()

    def _confirm_delete(self):
        self._delete_sudoku_buttons()
        self._show_page_buttons()

        if len(self._delete) > 0:
            sudoku_service.delete_sudokus(self._delete)
            self._delete = []
            self._initialize_list_view()

    def _delete_sudoku_buttons(self):
        for page in range(self._pages+1):
            self._frame.canvas.delete("check"+str(page))
            self._frame.canvas.delete("sudoku"+str(page))

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

        checkvar = IntVar()
        checkbox = tk.Checkbutton(
            master=self._frame,
            variable=checkvar,
            onvalue=1,
            offvalue=0,
            bg="white",
            command=lambda: self._save_choice(sudoku.name, checkvar),
            activebackground="white",
            highlightthickness=0
        )

        if counter < 3:
            y = 1
        elif counter < 6:
            y = 2
        elif counter < 9:
            y = 3

        self._frame.canvas.create_window(
            ((400/3)*((counter % 3)+1)-25), (y * 100 + 125),
            anchor='s', window=start_sudoku_button, tags="sudoku"+str(page)
        )

        self._frame.canvas.create_window(
            ((400/3)*((counter % 3)+1)), ((y * 100 + 75) + 75),
            anchor='s', window=checkbox, tags=("check"+str(page), sudoku.name)
        )

        user = user_service.get_current_user()
        user_id = user_service.get_user_id(user)
        sudoku_id = sudoku_service.get_sudoku_id(sudoku)

        playtime = user_service.get_playtime(user_id, sudoku_id)

        playtime_label = tk.Label(
            master=self._frame,
            text=playtime,
            bg="white"
        )

        self._frame.canvas.create_window(
            ((400/3)*((counter % 3)+1)-25), ((y * 100 + 75) + 75),
            anchor='s', window=playtime_label, tags="sudoku"+str(page)
        )

        if page != self._current_page:
            self._hide_sudoku_buttons(page)

    def _show_checkbuttons(self, page):
        self._frame.canvas.itemconfig("submit", state="normal")
        self._frame.canvas.itemconfig("check"+str(page), state="normal")

    def _hide_checkbuttons(self, page):
        self._frame.canvas.itemconfig("submit", state="hidden")
        self._frame.canvas.itemconfig("check"+str(page), state="hidden")

    def _hide_page_buttons(self):
        self._frame.canvas.itemconfig("next", state="hidden")
        self._frame.canvas.itemconfig("previous", state="hidden")

    def _show_page_buttons(self):
        """Show page selection buttons."""
        self._hide_page_buttons()

        if self._current_page < self._pages:
            self._frame.canvas.itemconfig("next", state="normal")

        if self._current_page != 0:
            self._frame.canvas.itemconfig("previous", state="normal")

    def _show_sudoku_buttons(self):
        """Show sudoku buttons of current page."""
        self._frame.canvas.itemconfig(
            "sudoku"+str(self._current_page), state="normal")

    def _hide_sudoku_buttons(self, page):
        """Hides sudoku buttons on a given page.

        Args:
            page (int): A page in which the sudoku buttons will be hidden.
        """

        self._frame.canvas.itemconfig("sudoku"+str(page), state="hidden")

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
        """Initialize menu and page selection buttons."""
        next_page_button = tk.Button(
            master=self._frame,
            text="next page",
            command=self._handle_next_page,
            bg="#ffab91",
            activebackground="#ff8a65",
            width=9,
            height=2
        )
        self._frame.canvas.create_window(
            325, 525, anchor='s', window=next_page_button, tags="next")

        previous_page_button = tk.Button(
            master=self._frame,
            text="previous page",
            command=self._handle_previous_page,
            bg="#ffab91",
            activebackground="#ff8a65",
            width=9,
            height=2
        )

        self._frame.canvas.create_window(
            175, 525, anchor='s', window=previous_page_button, tags="previous")

        self._hide_page_buttons()

        return_button = tk.Button(
            master=self._frame,
            text="Return",
            command=self._return_handler,
            bg="#a3e4d7",
            activebackground="#1abc9c"
        )

        self._frame.canvas.create_window(
            250, 20, anchor='n', window=return_button)

        delete_button = tk.Button(
            master=self._frame,
            text="Delete sudokus",
            command=self._delete_handler,
            bg="#a3e4d7",
            activebackground="#1abc9c"
        )

        self._frame.canvas.create_window(
            400, 20, anchor='n', window=delete_button
        )

        submit_button = tk.Button(
            master=self._frame,
            text="Confirm",
            command=self._confirm_delete,
            bg="#f44336",
            activebackground="#CC0000"
        )

        self._frame.canvas.create_window(
            200, 525, anchor='s', window=submit_button, tags="submit"
        )

        cancel_submit_button = tk.Button(
            master=self._frame,
            text="Cancel",
            command=self._cancel_submit,
            bg="#a3e4d7",
            activebackground="#1abc9c"
        )

        self._frame.canvas.create_window(
            300, 525, anchor='s', window=cancel_submit_button, tags="submit"
        )

    def _initialize_list_view(self):
        sudoku_page = 0
        counter = 0
        sudokus = sudoku_service.get_sudokus(self._level)
        self._pages = (
            len(sudokus)//9 if len(sudokus) % 9 != 0 else len(sudokus)//9 - 1)

        for sudoku in sudokus:
            if counter >= 9:
                counter = 0
                sudoku_page += 1
            self._initialize_sudoku(sudoku, counter, sudoku_page)
            counter += 1

        for page in range(self._pages+1):
            self._hide_checkbuttons(page)

        if self._current_page > self._pages:
            self._handle_previous_page()

        if self._pages > 0:
            self._show_page_buttons()

    def _initialize(self):
        """Initialize the selection view.
            Initialize the page select buttons, but only show them if there is more than one page.
        """

        self._frame = tk.Frame(master=self._root)

        self._frame.canvas = Canvas(
            master=self._frame,
            bg="white",
            width=500,
            height=550,
            highlightthickness=0,
            bd=0
        )

        self._frame.canvas.pack(fill=constants.X)

        self._frame.canvas.create_text(
            250, 125, text="Select a sudoku", fill="black", font=('bold', 13))

        self._initialize_buttons()

        self._initialize_list_view()

    def pack(self):
        """Show the view."""
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """Hide the view."""
        self._frame.destroy()
