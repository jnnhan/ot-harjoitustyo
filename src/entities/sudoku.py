class Sudoku:
    """Class for a single sudoku.

    Attributes:
        name: (string) Sudoku's name 
        puzzle: (String) Sudoku's numbers in a string format
        level: (Int) Sudoku's level   
    """

    def __init__(self, name=None, puzzle=None, level=None):
        """Initialize the class for making a new sudoku.

        Args:
            name: Sudoku's name. Defaults to None.
            puzzle: Sudoku's numbers. Defaults to None.
            level: Level of the sudoku. Defaults to None.
        """
        self.name = name
        self.puzzle = puzzle
        self.level = level
