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

    def draw_cell(self, cell, fill_color):
        cell.draw(self.c, fill_color)
            

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

class Cell():
    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        
    def draw(self, canvas, fill_color):
        if self.has_left_wall:
            canvas.create_line(self.top_left.x, self.top_left.y, self.top_left.x, self.bottom_right.y, fill=fill_color, width = 1)
        if self.has_right_wall:
            canvas.create_line(self.bottom_right.x, self.top_left.y, self.bottom_right.x, self.bottom_right.y, fill=fill_color, width = 1)
        if self.has_top_wall:
            canvas.create_line(self.top_left.x, self.top_left.y, self.bottom_right.x, self.top_left.y, fill=fill_color, width = 1)
        if self.has_bottom_wall:
            canvas.create_line(self.top_left.x, self.bottom_right.y, self.bottom_right.x, self.bottom_right.y, fill=fill_color, width = 1)
        canvas.pack(fill=BOTH, expand=1)



def main():
    win = Window(800, 600)
    p1 = Point(50, 50)
    p2 = Point(500, 500)
    l1 = Line(p1, p2)
    c1 = Cell(p1, p2)
    win.draw_line(l1, "red")
    win.draw_cell(c1, "black")
    win.wait_for_close()

main()
