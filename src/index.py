from tkinter import Tk
from ui.ui import UI


def main():
    root = Tk()
    root.title("Sudoku app")

    user_interface = UI(root)
    user_interface.start()

    root.mainloop()


if __name__ == "__main__":
    main()
