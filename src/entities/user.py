class User:
    """Class for a single user.

        Attributes:
            username: Username for the user
            password: Password for the user
    """

    def __init__(self, username, password):
        """Initialize the class for creating a new user.

        Args:
            username: Username for the user
            password: password for the user
        """
        self.username = username
        self.password = password
