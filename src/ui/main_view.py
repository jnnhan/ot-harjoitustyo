from tkinter import ttk, constants


class MainView:
    def __init__(self, root, handle_logout, handle_game):
        self._root = root
        self._handle_logout = handle_logout
        self._handle_game = handle_game
        self._frame = None

        self._initialize()

    def _select_game_handler(self, level):
        self._handle_game(level)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        logout_button = ttk.Button(
            master=self._frame,
            text="Log out",
            command=self._handle_logout
        )

        logout_button.grid(columnspan=2, sticky=(
            constants.E, constants.W), padx=5, pady=5)

        for i in range(1, 4):
            leveltxt = ""
            if i == 1:
                leveltxt = "Easy"
            elif i == 2:
                leveltxt = "Medium"
            else:
                leveltxt = "Hard"

            game_button = ttk.Button(
                master=self._frame,
                text=leveltxt,
                command=lambda i=i: self._select_game_handler(i)
            )

            game_button.grid(columnspan=2, sticky=(
                constants.E, constants.W), padx=5, pady=5)

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()
