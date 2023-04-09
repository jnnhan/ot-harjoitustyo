from tkinter import ttk, constants

class EasyView():
    def __init__(self, root, handle_return, handle_start_game):
        self._root = root
        self._frame = None
        self._handle_return = handle_return
        self._handle_start_game = handle_start_game
        self._initialize()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        self._root.title("Sudoku - Easy")
        self._frame.pack(fill=constants.X, expand=1)

        # TODO: get_easy_games()

        game_button = ttk.Button(
            master=self._frame,
            text="SUDOKU1",
            command=self._handle_start_game
        )

        game_button.grid(columnspan=2, sticky=(constants.E, constants.W), padx=5, pady=5)

        return_button = ttk.Button(
            master=self._frame,
            text="Return",
            command=self._handle_return
        )

        return_button.grid(columnspan=2, sticky=(constants.E, constants.W), padx=5, pady=5)

    def destroy(self):
        self._frame.destroy()

