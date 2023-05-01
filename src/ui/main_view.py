from tkinter import ttk, constants, Canvas
import tkinter as tk
from services.sudoku_service import sudoku_service


class MainView:
    def __init__(self, root, handle_logout, handle_game):
        self._root = root
        self._handle_logout = handle_logout
        self._handle_game = handle_game
        self._frame = None
        self._user = sudoku_service.get_current_user()

        self._initialize()

    def _select_game_handler(self, level):
        self._handle_game(level)

    def _logout_handler(self):
        sudoku_service.logout()
        self._handle_logout()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        self._frame.canvas = Canvas(
            master=self._frame,
            bg="white",
            width=250,
            height=200
        )

        self._frame.canvas.pack(fill=constants.X)

        logout_button = tk.Button(
            master=self._frame,
            text="Log out",
            command=self._logout_handler,
            bg="#a3e4d7"
        )

        user_label = tk.Label(
            master=self._frame,
            text=f"Logged in as {self._user.username}",
            bg="white",
            fg="#1abc9c"
        )

        self._frame.canvas.create_window(
            200, 10, anchor='n', window=logout_button)

        self._frame.canvas.create_window(
            80, 35, anchor='s', window=user_label)

        for i in range(1, 4):
            leveltxt = ""
            bg = ""
            if i == 1:
                leveltxt = "Easy"
                bg = "#c8e6c9"
            elif i == 2:
                leveltxt = "Medium"
                bg = "#ffecb3"
            else:
                leveltxt = "Hard"
                bg = "#ffccbc"

            game_button = tk.Button(
                master=self._frame,
                text=leveltxt,
                command=lambda i=i: self._select_game_handler(i),
                bg=bg
            )

            self._frame.canvas.create_window(
                125, (i * 50 + 25), window=game_button
            )

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()
