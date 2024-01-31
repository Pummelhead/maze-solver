from window import Window
from maze import Maze

def main():
    win = Window(800, 800)

    m1 = Maze(50, 50, 30, 30, 10, 10, win)
    m1.solve()

    win.wait_for_close()


main()
