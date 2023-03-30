from tkinter import Tk, ttk, Canvas, Frame, Button, TOP, BOTTOM, BOTH, constants

MARGIN = 25
CELL = 50
WIDTH = HEIGHT = MARGIN * 2 + CELL * 9


class SudokuView:
    def __init__(self, root, handle_logout):
        self._root = root
        self._handle_logout = handle_logout
        self._frame = None

        self.row = 0
        self.col = 0
        self._initialize()

    def _initialize(self):
        self._frame = Frame(master=self._root)

        self._root.title("Sudoku")
        self._frame.pack(fill=BOTH, expand=1)
        self._frame.canvas = Canvas(
            master=self._frame,
            bg="white",
            width=WIDTH,
            height=HEIGHT
        )
        self._frame.canvas.pack(fill=BOTH, side=TOP)
        self._draw_grid()

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