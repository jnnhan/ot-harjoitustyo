from tkinter import ttk, Canvas, Frame, TOP, BOTTOM, BOTH, constants
import copy
import sudokus

MARGIN = 25
CELL = 50
WIDTH = HEIGHT = MARGIN * 2 + CELL * 9


class GameView:
    def __init__(self, root, sudoku, handle_return):
        self._root = root
        self._handle_return = handle_return
        self._frame = None
        self._sudoku = sudoku

        self.row = 0
        self.col = 0
        self.start()
        self._initialize()

    def _return_handler(self):
        self._handle_return()

    def _initialize(self):
        self._frame = Frame(master=self._root)
        _frame2 = Frame(master=self._frame)

        self._root.title("Sudoku")
        self._frame.pack(fill=BOTH, expand=1)
        _frame2.pack(fill=BOTH, side=BOTTOM)
        self._frame.canvas = Canvas(
            master=self._frame,
            bg="white",
            width=WIDTH,
            height=HEIGHT
        )
        self._frame.canvas.pack(fill=constants.X, side=TOP)
        self._draw_grid()
        self._draw_numbers()

        self._frame.canvas.bind("<1>", self._mouse_click)
        self._frame.canvas.focus_set()
        self._frame.canvas.bind("<Key>", self._key_press)

        return_button = ttk.Button(
            master=_frame2,
            text="Return",
            command=self._return_handler
        )

        return_button.grid(columnspan=2, sticky=(constants.E, constants.W), padx=5, pady=5)

    def start(self):
        self.puzzle = copy.deepcopy(self._sudoku)
        self.original = copy.deepcopy(self._sudoku)

    def _draw_square(self):
        self._frame.canvas.delete("square")
        if self.col >= 0 and self.row >= 0:
            x0 = MARGIN + CELL * (self.col) - 1
            y0 = MARGIN + CELL * (self.row + 1) + 1
            x1 = MARGIN + CELL * (self.col + 1) + 1
            y1 = MARGIN + CELL * self.row - 1

            self._frame.canvas.create_rectangle(x0, y0, x1, y1, tags="square", outline="brown1")

    def _mouse_click(self, event):
        x = event.x
        y = event.y

        if MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN:
            col = (x - MARGIN) // CELL
            row = (y - MARGIN) // CELL

            if self.col >= 0 or self.row >= 0:
                self.col = -1
                self.row = -1
            elif self.original[row][col][0] == 0:
                self.col = col
                self.row = row
        else:
            self.col = -1
            self.row = -1

        self._draw_square()

    def _key_press(self, event):
        key = event.char
        if self.col >= 0 and self.row >= 0 and key in "123456789":
            if len(self.puzzle[self.row][self.col]) == 0:
                self.puzzle[self.row][self.col].append(0)
            if self.puzzle[self.row][self.col][0] == 0:
                self.puzzle[self.row][self.col].pop()
                self.puzzle[self.row][self.col].append(int(key))
            elif int(key) not in self.puzzle[self.row][self.col]:
                self.puzzle[self.row][self.col].append(int(key))
            else:
                self.puzzle[self.row][self.col].remove(int(key))
            self._draw_numbers()
            self._draw_square()

    def _draw_numbers(self):
        self._frame.canvas.delete("numbers")
        for i in range(0,9):
            for j in range(0,9):
                numbers = self.puzzle[i][j]
                if len(numbers) == 1:
                    if numbers[0] != 0:
                        if numbers[0] == self.original[i][j][0]:
                            color = "gray9"
                        else:
                            color = "brown1"
                            
                        x = MARGIN + (j+0.5) * CELL
                        y = MARGIN + (i+0.5) * CELL
                        self._frame.canvas.create_text(x, y, text=numbers[0], tags="numbers", fill=color, font=('bold'))

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
                        self._frame.canvas.create_text(x, y, text=numbers[z], tags="numbers", fill=color, font=('Helvetica','10'))

    def _draw_grid(self):
        for i in range(0,10):
            color = "grey" if i % 3 == 0 else "pink"

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
