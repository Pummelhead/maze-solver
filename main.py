from tkinter import Tk, BOTH, Canvas

class Window():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root = Tk()
        self.root.title("Maze Solver")
        self.c = Canvas(self.root, width=self.width, height=self.height)
        self.c.pack(fill=BOTH, expand=1)
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.running = True
        while self.running == True:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self, line, fill_color):
        line.draw(self.c, fill_color)
            

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
class Line():
    def __init__(self, point_one, point_two):
        self.point_one = point_one
        self.point_two = point_two
        
    def draw(self, canvas, fill_color):
        canvas.create_line(self.point_one.x, self.point_one.y, self.point_two.x, self.point_two.y, fill=fill_color, width = 2)
        canvas.pack(fill=BOTH, expand=1)


def main():
    win = Window(800, 600)
    p1 = Point(50, 50)
    p2 = Point(500, 500)
    l1 = Line(p1, p2)
    win.draw_line(l1, "red")
    win.wait_for_close()

main()
