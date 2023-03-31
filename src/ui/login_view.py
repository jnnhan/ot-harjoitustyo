from tkinter import ttk, constants

class LoginView:
    def __init__(self, root, handle_login, handle_show_register_view):
        self._root = root
        self._handle_login = handle_login
        self._handle_show_register_view = handle_show_register_view
        self._frame = None
        self._username_entry = None
        self._password_entry = None

        self._initialize()

    def _login_handler(self):
        self._handle_login()

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

        login_button = ttk.Button(
            master=self._frame,
            text="Login",
            command=self._login_handler
        )

        register_button = ttk.Button(
            master=self._frame,
            text="Register",
            command=self._handle_show_register_view
        )

        self._frame.grid_columnconfigure(1, weight=1, minsize=300)

        login_button.grid(columnspan=2, sticky=(constants.E, constants.W), padx=5, pady=5)
        register_button.grid(columnspan=2, sticky=(constants.E, constants.W), padx=5, pady=5)

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()