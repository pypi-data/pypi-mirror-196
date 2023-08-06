import curses


class Cbreak:
    def __enter__(self):
        curses.cbreak()

    def __exit__(self, *args):
        curses.nocbreak


class Window:
    def __init__(self, row, col, height, width):
        self.row = row
        self.col = col
        self.height = height
        self.width = width
        self.win = curses.newwin(height, width, row, col)
