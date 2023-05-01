from tkinter import ttk, constants, Canvas, StringVar
import tkinter as tk
from services.sudoku_service import SudokuService, InvalidCredentialsError, UsernameExistsError


class RegisterView:
    """UI view for registering a new username.
    
        Attributes:
            root: parent element in which the current view is shown.
            frame: current Tkinter element.
            username_entry: new username given by the user trying to register.
            password_entry: password for the new user.
            handle_register_user: UI view for logging in which is called when creation of new user is complete.
            handle_show_login_view: UI view for logging in if user cancels creating new username.
    """

    def __init__(self, root, handle_show_login_view):
        """Initialize the UI class for registering a new user.

        Args:
            root: parent Tkinter element in which the current view is shown.
            handle_show_login_view: UI object that shows the log in view.
        """

        self._root = root
        self._frame = None
        self._username_entry = None
        self._password_entry = None
        self._handle_register_user = handle_show_login_view
        self._handle_show_login_view = handle_show_login_view
        self._error = None
        self._error_label = None

        self._initialize()

    def _show_error(self, message):
        """Show error message"""
        self._error.set(message)
        self._frame.canvas.create_window(200, 50, tags="error", window=self._error_label)

    def _hide_error(self):
        """Hide error message"""
        self._frame.canvas.delete("error")

    def _register_handler(self):
        """Handle the attempt to register a new user.
            Show error if username already exists or username or password is not valid.
        """

        username = self._username_entry.get()
        password = self._password_entry.get()

        try:
            service = SudokuService()
            service.create_user(username, password)

            self._handle_register_user()
        except InvalidCredentialsError as error:
            self._show_error(error)
        except UsernameExistsError as error:
            self._show_error(error)

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
        """Initialize the view for creating a new user."""
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
        
        self._error = StringVar(self._frame)

        self._error_label = tk.Label(
            master=self._frame,
            textvariable=self._error,
            bg="white",
            fg="red",
            font=('bold', 11)
        )

        self._hide_error()

    def pack(self):
        """Show the view"""
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """Hide the view"""
        self._frame.destroy()
