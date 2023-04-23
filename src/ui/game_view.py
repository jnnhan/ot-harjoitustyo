from tkinter import ttk, Canvas, Frame, TOP, BOTTOM, BOTH, constants
import copy
from services.sudoku_service import SudokuService

MARGIN = 25
CELL = 50
WIDTH = HEIGHT = MARGIN * 2 + CELL * 9


class GameView:
    def __init__(self, root, level, sudoku, handle_return):
        self._root = root
        self._handle_return = handle_return
        self._frame = None
        self._level = level
        self._sudoku = sudoku
        self._puzzle = copy.deepcopy(sudoku)
        self._service = SudokuService()

        self.row = 0
        self.col = 0
        self._initialize()

    def _return_handler(self):
        self._handle_return(self._level)

    def _start_sudoku(self, sudoku):
        self._puzzle = copy.deepcopy(sudoku)

    def _clear_sudoku(self):
        self._start_sudoku(self._sudoku)
        self._frame.canvas.delete("win")
        self._draw_numbers()

    def _clear_cell(self):
        if len(self._frame.canvas.gettags("square")) != 0:
            self._puzzle[self.row][self.col].clear()
            self._puzzle[self.row][self.col].append(0)

        self._draw_numbers()
        self._draw_square()

    def _initialize(self):
        self._frame = Frame(master=self._root)
        _frame2 = Frame(master=self._frame)

        self._root.title("Sudoku")
        self._frame.pack(fill=BOTH, expand=1)
        _frame2.pack(fill=BOTH, side=BOTTOM)

        self._frame.canvas = Canvas(
            master=self._frame,
            bg="brown1",
            width=WIDTH,
            height=(HEIGHT + 50)
        )
        self._frame.canvas.pack(fill=constants.X, side=TOP)
        self._frame.canvas.create_rectangle(
            25, 25, (WIDTH-25), (HEIGHT-25), fill="white")

        self._draw_grid()
        self._draw_numbers()

        self._frame.canvas.bind("<1>", self._mouse_click)
        self._frame.canvas.bind("<Key>", self._key_press)

        return_button = ttk.Button(
            master=self._frame.canvas,
            text="Return",
            command=self._return_handler
        )

        self._frame.canvas.create_window(
            400, (HEIGHT+25), anchor='s', window=return_button
        )

        clear_button = ttk.Button(
            master=self._frame.canvas,
            text="Clear sudoku",
            command=self._clear_sudoku
        )

        self._frame.canvas.create_window(
            100, (HEIGHT+25), anchor='s', window=clear_button)

        clear_cell_button = ttk.Button(
            master=self._frame.canvas,
            text="Clear cell",
            command=self._clear_cell
        )

        self._frame.canvas.create_window(
            250, (HEIGHT+25), anchor='s', window=clear_cell_button)

    def _draw_square(self):
        self._frame.canvas.delete("square")
        if self.col >= 0 and self.row >= 0:
            x0 = MARGIN + CELL * (self.col) - 1
            y0 = MARGIN + CELL * (self.row + 1) + 1
            x1 = MARGIN + CELL * (self.col + 1) + 1
            y1 = MARGIN + CELL * self.row - 1

            self._frame.canvas.create_rectangle(
                x0, y0, x1, y1, tags="square", outline="brown1")

    def _mouse_click(self, event):
        x = event.x
        y = event.y

        if MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN:
            col = (x - MARGIN) // CELL
            row = (y - MARGIN) // CELL

            if self.col == col and self.row == row:
                self.col = -1
                self.row = -1
            elif self._sudoku[row][col][0] == 0:
                self.col = col
                self.row = row
        else:
            self.col = -1
            self.row = -1

        self._draw_square()

    def _draw_win(self):
        x = WIDTH / 2
        y = HEIGHT / 2
        self._frame.canvas.create_rectangle(
            100, 200, 400, 300, fill="pink", tags="win")
        self._frame.canvas.create_text(
            x, y, text="voitit pelin :-)", tags="win", fill="red", font=('bold'))

    def _key_press(self, event):
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

            if self._service.check_sudoku_win(self._puzzle):
                self._draw_win()

    def _draw_numbers(self):
        self._frame.canvas.focus_set()
        self._frame.canvas.delete("numbers")
        for i in range(0, 9):
            for j in range(0, 9):
                numbers = self._puzzle[i][j]
                if len(numbers) == 1:
                    if numbers[0] != 0:
                        if numbers[0] == self._sudoku[i][j][0]:
                            color = "gray9"
                        else:
                            color = "brown1"

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
        self._frame.canvas.create_rectangle(175, 25, 325, 175, fill="#fadbd8")
        self._frame.canvas.create_rectangle(25, 175, 175, 325, fill="#fadbd8")
        self._frame.canvas.create_rectangle(
            325, 175, (WIDTH-25), 325, fill="#fadbd8")
        self._frame.canvas.create_rectangle(
            175, 325, 325, (HEIGHT-25), fill="#fadbd8")

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
        self._frame.destroy()

    def pack(self):
        self._frame.pack(fill=constants.X)
