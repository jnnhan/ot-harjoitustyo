from tkinter import Canvas, Frame, TOP, BOTH, constants
import tkinter as tk
import copy
from services.sudoku_service import sudoku_service

MARGIN = 25
CELL = 50
WIDTH = HEIGHT = MARGIN * 2 + CELL * 9


class GameView:
    """UI view for playing a sudoku game.

        Attributes:
            root: parent element in which the current view is shown.
            frame: current Tkinter element.
            handle_return: UI view for selecting a new sudoku game of a certain level.
            game_over: a flag to tell if game is over or not.
            original: original sudoku to show which cells and numbers can't be emptied or altered.
            puzzle: current playable sudoku.
            row: a row user has clicked.
            col: a column user has clicked.
    """

    def __init__(self, root, puzzle, handle_return):
        """Initialize the UI class.

        Args:
            root: parent element for current view.
            puzzle: a sudoku puzzle, 9x9 matrix where empty cells are 0's.
            handle_return: UI view for selecting a new sudoku game of a certain level.
        """

        self._root = root
        self._frame = None
        self._handle_return = handle_return
        self._game_over = False
        self._original = puzzle
        self._puzzle = copy.deepcopy(puzzle)

        self.row = 0
        self.col = 0
        self._initialize()

    def _return_handler(self):
        """Handle the return to the view of selecting a sudoku.
            First removes the knowledge of recently played sudoku.
        """

        sudoku = sudoku_service.get_current_sudoku()
        sudoku_service.remove_current_sudoku()
        self._handle_return(sudoku.level)

    def _start_sudoku(self, puzzle):
        """Start sudoku by copying the original sudoku.

        Args:
            puzzle: 9x9 sudoku matrix
        """

        self._puzzle = copy.deepcopy(puzzle)

    def _clear_sudoku(self):
        """Clear current sudoku if user wants to start over."""
        self._start_sudoku(self._original)
        self._frame.canvas.delete("win")
        self._game_over = False
        self._display_buttons()
        self._draw_numbers()

    def _clear_cell(self):
        """Clear a single cell."""
        if len(self._frame.canvas.gettags("square")) != 0:
            self._puzzle[self.row][self.col].clear()
            self._puzzle[self.row][self.col].append(0)

        self._draw_numbers()
        self._draw_square()

    def _display_buttons(self):
        """Display menu buttons.
            Show different buttons if the game was solved.
        """

        if self._game_over:
            self._frame.canvas.delete("start")

            clear_button = tk.Button(
                master=self._frame.canvas,
                text="Play again",
                command=self._clear_sudoku,
                bg="#f5b041",
                activebackground="#f39c12"
            )

            self._frame.canvas.create_window(
                100, (HEIGHT+25), tags="again", anchor='s', window=clear_button)

        else:
            self._frame.canvas.delete("again")

            clear_button = tk.Button(
                master=self._frame.canvas,
                text="Clear sudoku",
                command=self._clear_sudoku,
                bg="#f5b041",
                activebackground="#f39c12"
            )

            self._frame.canvas.create_window(
                100, (HEIGHT+25), tags="start", anchor='s', window=clear_button)

            clear_cell_button = tk.Button(
                master=self._frame.canvas,
                text="Clear cell",
                command=self._clear_cell,
                bg="#f5b041",
                activebackground="#f39c12"
            )

            self._frame.canvas.create_window(
                250, (HEIGHT+25), tags="start", anchor='s', window=clear_cell_button)

    def _initialize(self):
        """Initialize the game view."""
        self._frame = Frame(master=self._root)
        self._frame.pack(fill=BOTH, expand=1)

        self._frame.canvas = Canvas(
            master=self._frame,
            bg="white",
            width=WIDTH,
            height=(HEIGHT + 50)
        )
        self._frame.canvas.pack(fill=constants.X, side=TOP)
        self._frame.canvas.create_rectangle(
            25, 25, (WIDTH-25), (HEIGHT-25), fill="#fdebd0")

        self._draw_grid()
        self._draw_numbers()

        self._frame.canvas.bind("<1>", self._mouse_click)
        self._frame.canvas.bind("<Key>", self._key_press)

        return_button = tk.Button(
            master=self._frame.canvas,
            text="Return",
            command=self._return_handler,
            bg="#f5b041",
            activebackground="#f39c12"
        )

        self._frame.canvas.create_window(
            400, (HEIGHT+25), anchor='s', window=return_button
        )

        self._display_buttons()

    def _draw_square(self):
        """Draw a square which highlights the cell user has clicked. 
            A new click of the same cell removes the square.
            If sudoku was solved on the last move square isn't drawn.
        """

        if self._game_over:
            return

        self._frame.canvas.delete("square")
        if self.col >= 0 and self.row >= 0:
            x0 = MARGIN + CELL * (self.col) - 1
            y0 = MARGIN + CELL * (self.row + 1) + 1
            x1 = MARGIN + CELL * (self.col + 1) + 1
            y1 = MARGIN + CELL * self.row - 1

            self._frame.canvas.create_rectangle(
                x0, y0, x1, y1, tags="square", outline="#c62828", width=3)

    def _mouse_click(self, event):
        """Handle the tkinter event of mouse click.
            If user clicked inside the grid draw a square to correspongind cell.

        Args:
            event: Tkinter event for mouse click.
        """

        if self._game_over:
            return

        x = event.x
        y = event.y

        if MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN:
            col = (x - MARGIN) // CELL
            row = (y - MARGIN) // CELL

            if self.col == col and self.row == row:
                self.col = -1
                self.row = -1
            elif self._original[row][col][0] == 0:
                self.col = col
                self.row = row
        else:
            self.col = -1
            self.row = -1

        self._draw_square()

    def _draw_win(self):
        self._frame.canvas.delete("square")
        """Show a victory message if sudoku was solved correctly."""
        x = WIDTH / 2
        y = HEIGHT / 2
        self._frame.canvas.create_rectangle(
            100, 200, 400, 300, fill="#e74c3c", tags="win")
        self._frame.canvas.create_text(
            x, y, text="YOU WIN", tags="win", fill="white", font=('bold'))

    def _key_press(self, event):
        """A tkinter event for handling a key press.
            Only register key presses of numbers 1-9.
            If latest key press filled the board check if sudoku was solved correctly.

        Args:
            event: tkinter event for key press.
        """

        if self._game_over:
            return

        key = event.char
        if self.col >= 0 and self.row >= 0 and key in "123456789":
            if len(self._puzzle[self.row][self.col]) == 0:
                self._puzzle[self.row][self.col].append(0)
            if self._puzzle[self.row][self.col][0] == 0:
                self._puzzle[self.row][self.col].pop()
                self._puzzle[self.row][self.col].append(int(key))
            elif int(key) not in self._puzzle[self.row][self.col]:
                self._puzzle[self.row][self.col].append(int(key))
            else:
                self._puzzle[self.row][self.col].remove(int(key))
            self._draw_numbers()
            self._draw_square()

            if sudoku_service.check_sudoku_win(self._puzzle):
                self._game_over = True
                self._draw_win()
                self._display_buttons()
                sudoku_service.save_status()

    def _draw_numbers(self):
        """Draw numbers to the grid."""
        self._frame.canvas.focus_set()
        self._frame.canvas.delete("numbers")
        for i in range(0, 9):
            for j in range(0, 9):
                numbers = self._puzzle[i][j]
                if len(numbers) == 1:
                    if numbers[0] != 0:
                        if numbers[0] == self._original[i][j][0]:
                            color = "gray9"
                        else:
                            color = "#e74c3c"

                        x = MARGIN + (j+0.5) * CELL
                        y = MARGIN + (i+0.5) * CELL
                        self._frame.canvas.create_text(
                            x, y, text=numbers[0], tags="numbers", fill=color, font=('bold'))

                else:
                    holders = len(numbers)
                    for z in range(0, holders):
                        if 0 <= z < 3:
                            b = 0.25
                        elif 3 <= z < 6:
                            b = 0.5
                        else:
                            b = 0.75
                        if z % 3 == 0:
                            a = 0.25
                        elif z == 1 or z == 4 or z == 7:
                            a = 0.5
                        else:
                            a = 0.75
                        x = MARGIN + (j+a) * CELL
                        y = MARGIN + (i+b) * CELL
                        color = "wheat4"
                        self._frame.canvas.create_text(
                            x, y, text=numbers[z], tags="numbers", fill=color, font=('Helvetica', '10'))

    def _draw_grid(self):
        """Draw sudoku grid."""
        self._frame.canvas.create_rectangle(175, 25, 325, 175, fill="#f7dc6f")
        self._frame.canvas.create_rectangle(25, 175, 175, 325, fill="#f7dc6f")
        self._frame.canvas.create_rectangle(
            325, 175, (WIDTH-25), 325, fill="#f7dc6f")
        self._frame.canvas.create_rectangle(
            175, 325, 325, (HEIGHT-25), fill="#f7dc6f")

        for i in range(0, 10):
            color = "black" if i % 3 == 0 else "grey"

            v0 = MARGIN + i * CELL
            v1 = MARGIN
            v2 = MARGIN + i * CELL
            v3 = HEIGHT - MARGIN
            self._frame.canvas.create_line(v0, v1, v2, v3, fill=color)

            h0 = MARGIN
            h1 = MARGIN + i * CELL
            h2 = WIDTH - MARGIN
            h3 = MARGIN + i * CELL
            self._frame.canvas.create_line(h0, h1, h2, h3, fill=color)

    def destroy(self):
        """Hide view."""
        self._frame.destroy()

    def pack(self):
        """Show view."""
        self._frame.pack(fill=constants.X)
