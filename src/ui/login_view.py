from tkinter import ttk, constants, StringVar, Canvas
import tkinter as tk
from services.sudoku_service import sudoku_service, InvalidCredentialsError


class LoginView:
    def __init__(self, root, handle_login, handle_show_register_view):
        self._root = root
        self._handle_login = handle_login
        self._handle_show_register_view = handle_show_register_view
        self._frame = None
        self._username_entry = None
        self._password_entry = None
        self._error_label = None
        self._error = None

        self._initialize()

    def _show_error(self, message):
        self._error.set(message)
        self._frame.canvas.create_window(200, 140, tags="error", window=self._error_label)

    def _hide_error(self):
        self._frame.canvas.delete("error")

    def _login_handler(self):
        username = self._username_entry.get()
        password = self._password_entry.get()

        try:
            sudoku_service.login(username, password)
            self._handle_login()
        except InvalidCredentialsError as error:
            self._show_error(error)

    def _initialize_username(self):
        username_label = tk.Label(master=self._frame, text="Username", bg="white")
        
        self._username_entry = tk.Entry(master=self._frame, bg="#fdedec")

        self._frame.canvas.create_window(90, 150, window=username_label)
        self._frame.canvas.create_window(250, 150, window=self._username_entry)

    def _initialize_password(self):
        password_label = tk.Label(master=self._frame, text="Password", bg="white")

        self._password_entry = tk.Entry(master=self._frame, show="*", bg="#fdedec")

        self._frame.canvas.create_window(90, 175, window=password_label)
        self._frame.canvas.create_window(250, 175, window=self._password_entry)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        self._frame.canvas = Canvas(
            master=self._frame,
            bg="white",
            width=400,
            height=300
        )
        self._frame.canvas.pack(fill=constants.X)

        self._frame.canvas.create_text(200, 80, text="SUDOKU", font=("Georgia", 35), fill="#1abc9c")

        self._initialize_username()
        self._initialize_password()

        register_button = tk.Button(
            master=self._frame,
            text="Create a new user",
            command=self._handle_show_register_view,
            bg="#a3e4d7"
        )

        login_button = tk.Button(
            master=self._frame,
            text="Login",
            command=self._login_handler,
            bg="#f7dc6f"
        )
        self._frame.canvas.create_window(
            200, 250, anchor='s', window=login_button)

        self._frame.canvas.create_window(
            200, 290, anchor='s', window=register_button)

        self._error = StringVar(self._frame)

        self._error_label = tk.Label(
            master=self._frame,
            textvariable=self._error,
            bg="#ff8a65",
            fg="red",
            font=('bold', 14)
        )

        self._hide_error()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()
