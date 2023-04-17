from tkinter import ttk, constants


class MainView:
    def __init__(self, root, handle_logout, handle_game):
        self._root = root
        self._handle_logout = handle_logout
        self._handle_game = handle_game
        self._frame = None

        self._initialize()

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
            level = i
            leveltxt = ""
            if level == 1:
                leveltxt = "Easy"
            elif level == 2:
                leveltxt = "Medium"
            elif level == 3:
                leveltxt = "Hard"

            game_button = ttk.Button(
                master=self._frame,
                text=leveltxt,
                command=lambda: self._handle_game(level)
            )

            game_button.grid(columnspan=2, sticky=(
                constants.E, constants.W), padx=5, pady=5)

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()
