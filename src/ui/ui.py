from ui.register_view import RegisterView
from ui.login_view import LoginView
from ui.main_view import MainView
from ui.game_view import GameView
from ui.sudoku_list_view import SudokuListView
from ui.add_sudoku_view import AddSudokuView


class UI:
    """Class resposible for the user interface.

        Attributes:
            root: Tkinter element in which all the views are shown.
            current_view: shows and keeps track of current view.
    """

    def __init__(self, root):
        """A class constructor for the UI.

        Args:
            root: Tkinter element in which all the views are shown.
        """

        self._root = root
        self._current_view = None

    def start(self):
        """Starts the user interface."""
        self._show_login_view()

    def _show_game_view(self, puzzle=None):
        """Show the view for playing sudokus.
            View returns to the sudoku selection.

        Args:
            puzzle: A sudoku matrix. Defaults to None.
        """

        self._hide_current_view()

        self._current_view = GameView(
            self._root,
            puzzle,
            self._show_select_view
        )

        self._current_view.pack()

    def _show_add_sudoku(self):
        """Show the view for adding new sudokus.
            Return to the main view.
        """

        self._hide_current_view()

        self._current_view = AddSudokuView(
            self._root,
            self._show_main_view
        )

        self._current_view.pack()

    def _show_main_view(self):
        """Show the main view of the app.
            Returns to the login screen.
        """

        self._hide_current_view()

        self._current_view = MainView(
            self._root,
            self._show_login_view,
            self._show_select_view,
            self._show_add_sudoku
        )

        self._current_view.pack()

    def _show_select_view(self, level=None):
        """Show the view for selecting a sudoku of certain level.
            Returns to the main view.

        Args:
            level: A level for sudoku. Defaults to None.
        """

        self._hide_current_view()

        self._current_view = SudokuListView(
            self._root,
            level,
            self._show_main_view,
            self._show_game_view
        )

        self._current_view.pack()

    def _show_login_view(self):
        """Show the login view."""
        self._hide_current_view()
        self._current_view = LoginView(
            self._root,
            self._show_main_view,
            self._show_register_user_view
        )

        self._current_view.pack()

    def _show_register_user_view(self):
        """Show the register view."""
        self._hide_current_view()

        self._current_view = RegisterView(
            self._root,
            self._show_login_view
        )

        self._current_view.pack()

    def _hide_current_view(self):
        """Hides the current view."""
        if self._current_view:
            self._current_view.destroy()

        self._current_view = None
