from tkinter import Tk, BOTH, Canvas
import time


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")

    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)

    def close(self):
        self.__running = False


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(
        self,
        p1,
        p2,
    ):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color="black"):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )
        canvas.pack(fill=BOTH, expand=1)

class Cell:
    def __init__(self, win):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win

    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        if self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line)
        if not self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line, "white")
        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line)
        if not self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line, "white")
        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line)
        if not self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line, "white")
        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line)
        if not self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line, "white")

    def draw_move(self, to_cell, undo=False):
        if not undo:
            fill_color_move = "red"
        else:
            fill_color_move = "gray"
        move_line = Line(
            Point(self._x2 - ((self._x2 - self._x1) * 0.5), self._y2 - ((self._y2 - self._y1) * 0.5)),
            Point(to_cell._x2 - ((to_cell._x2 - to_cell._x1) * 0.5 ), to_cell._y2 - ((to_cell._y2 - self._y1) * 0.5))
            )
        self._win.draw_line(move_line, fill_color_move)

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._create_cells()
        self._break_entrance_and_exit()

    def _create_cells(self):
        self.cols = []
        i = self.x1
        j = self.y1
        for x in range(0, self.num_cols):
            self.cells = []
            for y in range(0, self.num_rows):
                y = Cell(self.win)
                self.cells.append(y)
            self.cols.append(self.cells)
        for col in self.cols:
            for cell in col:
                self._draw_cell(i, j, cell)
                j += self.cell_size_y
            i += self.cell_size_x
            j = self.y1
        

    def _break_entrance_and_exit(self):
        self.cols[0][0].has_top_wall = False
        self.cols[self.num_cols-1][self.num_rows-1].has_bottom_wall = False
        self.cols[0][0].draw(
            self.cols[0][0]._x1,
            self.cols[0][0]._y1,
            self.cols[0][0]._x2,
            self.cols[0][0]._y2
            )
        self._animate()
        self.cols[self.num_cols-1][self.num_rows-1].draw(
            self.cols[self.num_cols-1][self.num_rows-1]._x1,
            self.cols[self.num_cols-1][self.num_rows-1]._y1,
            self.cols[self.num_cols-1][self.num_rows-1]._x2,
            self.cols[self.num_cols-1][self.num_rows-1]._y2
            )
        self._animate()

    def _draw_cell(self, i, j, cell):
        cell.draw(i, j, i + self.cell_size_x, j + self.cell_size_y)
        self._animate()
    
    def _animate(self):
        self.win.redraw()
        time.sleep(0.025)

def main():
    win = Window(800, 800)

    m1 = Maze(50, 50, 4, 4, 50, 50, win)

    win.wait_for_close()


main()
