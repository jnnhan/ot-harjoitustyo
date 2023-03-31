from entities.user import User

from repositories.user_repository import user_repo

class SudokuService:
    def __init__(self):
        self._user = None
        self._user_repository = user_repo

    def login(self, username, password):
        user = self._user_repository.find_user(username)

        if user and user.password==password:
            self._user = user
        
        return user

    def create_user(self, username, password):
        user = self._user_repository.create_user(User(username, password))

        return user
    
sudoku_service = SudokuService()