from ui.register_view import RegisterView
from ui.login_view import LoginView
from ui.main_view import MainView
from ui.game_view import GameView
from ui.easy_view import EasyView


class UI:
    def __init__(self, root):
        self._root = root
        self._current_view = None

    def start(self):
        self._show_login_view()

    def _show_game_view(self, puzzle=None):
        self._hide_current_view()

        self._current_view = GameView(
            self._root,
            puzzle,
            self._show_game_select
        )

        self._current_view.pack()

    def _show_main_view(self):
        self._hide_current_view()

        self._current_view = MainView(
            self._root,
            self._show_login_view,
            self._show_game_select
        )

        self._current_view.pack()

    def _show_game_select(self, level=None):
        self._hide_current_view()

        self._current_view = EasyView(
            self._root,
            self._show_main_view,
            self._show_game_view,
            level
        )

        self._current_view.pack()

    def _show_login_view(self):
        self._hide_current_view()
        self._current_view = LoginView(
            self._root,
            self._show_main_view,
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
