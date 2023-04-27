from tkinter import ttk, constants, Canvas
import tkinter as tk
from services.sudoku_service import SudokuService


class RegisterView:
    """ A view for registering a new username."""

    def __init__(self, root, handle_show_login_view):
        """ A class constructor that creates the view for registration.

        Args:
            root:
                Tkinter element in which the view is shown.
            handle_register_user:
                An object which is called when a new user is created. Gets a username and a password as arguments.
            handle_show_login_view:
                An object which is called when login view is showed.
        """

        self._root = root
        self._frame = None
        self._username_entry = None
        self._password_entry = None
        self._handle_register_user = handle_show_login_view
        self._handle_show_login_view = handle_show_login_view

        self._initialize()

    def _register_handler(self):
        username = self._username_entry.get()
        password = self._password_entry.get()

        if len(username) > 2 and len(password) > 3:
            service = SudokuService()
            service.create_user(username, password)

            self._handle_register_user()

    def _initialize_username(self):
        username_label = tk.Label(master=self._frame, text="Username", bg="white")
        
        self._username_entry = tk.Entry(master=self._frame, bg="#fdedec")

        self._frame.canvas.create_window(75, 75, window=username_label)
        self._frame.canvas.create_window(225, 75, window=self._username_entry)

    def _initialize_password(self):
        password_label = tk.Label(master=self._frame, text="Password", bg="white")

        self._password_entry = tk.Entry(master=self._frame, show="*", bg="#fdedec")

        self._frame.canvas.create_window(75, 100, window=password_label)
        self._frame.canvas.create_window(225, 100, window=self._password_entry)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        self._frame.canvas = Canvas(
            master=self._frame,
            bg="white",
            width=400,
            height=200
        )
        self._frame.canvas.pack(fill=constants.X)

        self._frame.canvas.create_text(200, 25, text="Create a new username", 
                                       font=("Arial", 12), fill="black")

        self._initialize_username()
        self._initialize_password()

        register_button = tk.Button(
            master=self._frame,
            text="Register",
            command=self._register_handler,
            bg="#f7dc6f"
        )

        login_button = tk.Button(
            master=self._frame,
            text="Login",
            command=self._handle_show_login_view,
            bg="#a3e4d7"
        )

        self._frame.canvas.create_window(
            200, 190, anchor='s', window=login_button)

        self._frame.canvas.create_window(
            200, 150, anchor='s', window=register_button)

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()
