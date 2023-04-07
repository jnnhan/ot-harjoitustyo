from tkinter import ttk, constants

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
            service.sudoku_service.create_user(username, password)

            self._handle_register_user()

    def _initialize_username(self):
        username_label = ttk.Label(master=self._frame, text="Username")
        
        self._username_entry = ttk.Entry(master=self._frame)

        username_label.grid(padx=5, pady=5)
        self._username_entry.grid(row=1, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)

    def _initialize_password(self):
        password_label = ttk.Label(master=self._frame, text="Password")

        self._password_entry = ttk.Entry(master=self._frame, show="*")

        password_label.grid(padx=5, pady=5)
        self._password_entry.grid(row=2, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        self._initialize_username()
        self._initialize_password()

        register_button = ttk.Button(
            master=self._frame,
            text="Register",
            command=self._register_handler
        )

        login_button = ttk.Button(
            master=self._frame,
            text="Login",
            command=self._handle_show_login_view
        )

        self._frame.grid_columnconfigure(1, weight=1, minsize=300)
        register_button.grid(columnspan=2, sticky=(constants.E, constants.W), padx=5, pady=5)
        login_button.grid(columnspan=2, sticky=(constants.E, constants.W), padx=5, pady=5)

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()