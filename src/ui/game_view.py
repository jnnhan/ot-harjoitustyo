from tkinter import Tk, ttk, Canvas, Frame, Button, TOP, BOTTOM, BOTH, constants
import sudokus

MARGIN = 25
CELL = 50
WIDTH = HEIGHT = MARGIN * 2 + CELL * 9


class GameView:
    def __init__(self, root, handle_return):
        self._root = root
        self._handle_return= handle_return
        self._frame = None

        self.row = 0
        self.col = 0
        self._initialize()

    def _initialize(self):
        self._frame = Frame(master=self._root)
        frame2 = Frame(master=self._frame)

        self._root.title("Sudoku")
        self._frame.pack(fill=BOTH, expand=1)
        frame2.pack(fill=BOTH, side=BOTTOM)
        self._frame.canvas = Canvas(
            master=self._frame,
            bg="white",
            width=WIDTH,
            height=HEIGHT
        )
        self._frame.canvas.pack(fill=constants.X, side=TOP)
        self._draw_grid()
        self._draw_numbers()

        return_button = ttk.Button(
            master=frame2,
            text="Return",
            command=self._handle_return
        )

        return_button.grid(columnspan=2, sticky=(constants.E, constants.W), padx=5, pady=5)

    def _draw_numbers(self):
        puzzle = sudokus.easy_one
        for i in range(9):
            for j in range(9):
                number = puzzle[i][j]
                if number != 0:
                    x = MARGIN + (j+0.5) * CELL
                    y = MARGIN + (i+0.5) * CELL
                    color = "gray9"
                    self._frame.canvas.create_text(x, y, text=number, fill=color, font=('bold'))

                else:
                    x = MARGIN + (j+0.5) * CELL
                    y = MARGIN + (i+0.25) * CELL
                    color = "wheat4"
                    self._frame.canvas.create_text(x, y, text="0", fill=color, font=('Helvetica','10'))

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
