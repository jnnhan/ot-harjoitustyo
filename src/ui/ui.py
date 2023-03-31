from ui.register_view import RegisterView
from ui.login_view import LoginView
from ui.sudoku_view import SudokuView

class UI:
    def __init__(self, root):
        self._root = root
        self._current_view = None

    def start(self):
        self._show_login_view()

    def _show_sudoku_view(self):
        self._hide_current_view()

        self._current_view = SudokuView(
            self._root,
            self._show_login_view
        )

        self._current_view.pack()

    def _show_login_view(self):
        self._hide_current_view()
        self._current_view = LoginView(
            self._root,
            self._show_sudoku_view,
            self._show_register_user_view
        )

        self._current_view.pack()

    def _show_register_user_view(self):
        self._hide_current_view()

        self._current_view = RegisterView(
            self._root,
            self._show_login_view
        )

        self._current_view.pack()

    def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()

        self._current_view = None