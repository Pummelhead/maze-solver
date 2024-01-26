from tkinter import Tk, BOTH, Canvas

class Window():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root = Tk()
        self.root.title("Maze Solver")
        self.c = Canvas()
        self.c.pack()
        self.running = False

        def redraw():
            self.update_idletasks()
            self.update()

        def wait_for_close():
            self.running = True
            while self.running == True:
                self.redraw()

        def close():
            self.running = False
            self.__root = Tk()
            ...
            self.__root.protocol("WM_DELETE_WINDOW", self.close)

def main():
    win = Window(800, 600)
    win.wait_for_close()

main()
