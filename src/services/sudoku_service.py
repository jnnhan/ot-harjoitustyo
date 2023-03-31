from entities.user import User
from repositories.user_repository import user_repo
from werkzeug.security import check_password_hash

class InvalidCredentialsError(Exception):
    pass

class SudokuService:
    def __init__(self):
        self._user = None
        self._user_repository = user_repo

    def login(self, username, password):
        user = self._user_repository.find_user(username)
        hash_password = self._user_repository.check_password(username)

        if not user:
            raise InvalidCredentialsError("Wrong username")
        else:
            if check_password_hash(hash_password, password):
                self._user = user
            else:
                raise InvalidCredentialsError("Wrong password")

        return user

    def create_user(self, username, password):
        user = self._user_repository.create_user(User(username, password))

        return user
    
sudoku_service = SudokuService()