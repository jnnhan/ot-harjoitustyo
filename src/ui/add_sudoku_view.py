import tkinter as tk
from tkinter import Canvas, constants, Frame, StringVar, Text, END
from services.sudoku_service import sudoku_service, InvalidSudokuInputError, SudokuExistsError


class AddSudokuView:
    """UI class responsible of showing the view for adding new sudokus.

        Attributes:
            root: parent element for current view.
            frame: frame for current view.
            handle_main_view: UI view for the main view.
            name_entry: name of new sudoku, given by user.
            puzzle_entry: new sudoku, given by user.
            level_entry: level of new sudoku, given by user.
    """

    def __init__(self, root, handle_main_view):
        """Initialize the UI class.

        Args:
            root: parent element for current view.
            handle_main_view: view for main view of the app.
        """

        self._root = root
        self._frame = None
        self._handle_main_view = handle_main_view
        self._name_entry = None
        self._puzzle_entry = None
        self._level_entry = None
        self._error = None
        self._error_label = None

        self._initialize()

    def _show_error(self, message):
        """Show error message"""
        self._error.set(message)
        self._frame.canvas.create_window(
            250, 220, tags="error", window=self._error_label)

    def _hide_error(self):
        """Hide error message"""
        self._frame.canvas.delete("error")

    def _hide_inputs(self):
        """Hide user inputs."""
        self._name_entry.delete(0, END)
        self._level_entry.delete(0, END)
        self._puzzle_entry.delete("1.0", END)
        self._frame.canvas.delete("success")
        self._frame.canvas.itemconfig(self._submit_button, state="normal")
        self._frame.canvas.itemconfig(
            self._submit_again_button, state="hidden")

    def _return_handler(self):
        """"Show the main view."""
        self._handle_main_view()

    def _submit_handler(self):
        """Handle the user inputs by calling SudokuService method and
            trying to create new sudoku.
            Catch and handle errors if inputs were incorrect.
        """

        name = self._name_entry.get()
        level = self._level_entry.get()
        puzzle = self._puzzle_entry.get("1.0", "end-1c")

        try:
            sudoku_service.save_sudoku(name, level, puzzle)
            self._frame.canvas.create_text(
                400, 380, tags="success",
                text=f"Sudoku '{name}' was \n added succesfully!",
                font=('bold', 10), fill="red"
            )
            self._frame.canvas.itemconfig(self._submit_button, state="hidden")

            submit_again = tk.Button(
                master=self._frame,
                text="Add another sudoku",
                command=self._hide_inputs,
                bg="#a3e4d7",
                activebackground="#1abc9c"
            )

            self._submit_again_button = self._frame.canvas.create_window(
                250, 480, anchor='n', window=submit_again)

        except InvalidSudokuInputError as error:
            self._show_error(error)
        except InterruptedError as error:
            self._show_error(error)
        except SudokuExistsError as error:
            self._show_error(error)

    def _initialize_sudoku_name(self):
        """Initialize label and entry for sudoku name."""
        name_label = tk.Label(
            master=self._frame, text="Name \n(1-12 characters):", bg="white")

        self._name_entry = tk.Entry(master=self._frame, bg="#fdedec")

        self._frame.canvas.create_window(150, 100, window=name_label)
        self._frame.canvas.create_window(320, 100, window=self._name_entry)

    def _initialize_sudoku_level(self):
        """Initialize label and entry for sudoku level."""
        level_label = tk.Label(
            master=self._frame, text="Level (1-3):", bg="white")

        self._level_entry = tk.Entry(master=self._frame, bg="#fdedec")

        self._frame.canvas.create_window(150, 150, window=level_label)
        self._frame.canvas.create_window(320, 150, window=self._level_entry)

    def _initialize_sudoku_puzzle(self):
        """Initialize textbox and label for sudoku entry."""
        puzzle_label = tk.Label(
            master=self._frame, text="Type all 9 sudoku rows: \n(type empty cells as 0's)", bg="white")

        self._puzzle_entry = Text(
            master=self._frame.canvas,
            font=('Andale mono', 16),
            width=9,
            height=9
        )

        self._frame.canvas.create_window(250, 350, window=self._puzzle_entry)
        self._frame.canvas.create_window(260, 200, window=puzzle_label)

    def _initialize_buttons(self):
        """Initialize submit and return buttons."""
        submit = tk.Button(
            master=self._frame.canvas,
            text="Submit",
            command=self._submit_handler,
            bg="#f7dc6f",
            activebackground="#f1c40f",
        )

        return_button = tk.Button(
            master=self._frame.canvas,
            text="Return",
            command=self._return_handler,
            bg="#a3e4d7",
            activebackground="#1abc9c"
        )

        self._frame.canvas.create_window(
            450, 20, anchor='n', window=return_button)

        self._submit_button = self._frame.canvas.create_window(
            250, 490, anchor='n', tags="submit", window=submit)

    def _initialize(self):
        """Initialize the view."""
        self._frame = Frame(master=self._root)

        self._frame.canvas = Canvas(
            master=self._frame,
            bg="white",
            width=500,
            height=550,
            highlightthickness=0,
            bd=0
        )
        self._frame.canvas.pack(fill=constants.Y)

        self._frame.canvas.create_text(
            250, 40, text="Add new sudoku", fill="black", font=('bold', 13)
        )

        self._initialize_sudoku_name()
        self._initialize_sudoku_puzzle()
        self._initialize_sudoku_level()

        self._initialize_buttons()

        self._error = StringVar(self._frame)

        self._error_label = tk.Label(
            master=self._frame,
            textvariable=self._error,
            bg="white",
            fg="red",
            font=('bold', 11)
        )

        self._hide_error()

    def pack(self):
        """Show the view."""
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """Hide the view."""
        self._frame.destroy()
