from tkinter import Tk, BOTH, Canvas
import time
import random


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
        self.name = None
        self._win = win

    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        if not hasattr(self, 'initial_drawn') or self.initial_drawn is False:
            if self.has_left_wall:
                line = Line(Point(x1, y1), Point(x1, y2))
                self._win.draw_line(line)
            if self.has_top_wall:
                line = Line(Point(x1, y1), Point(x2, y1))
                self._win.draw_line(line)
            if self.has_right_wall:
                line = Line(Point(x2, y1), Point(x2, y2))
                self._win.draw_line(line)
            if self.has_bottom_wall:
                line = Line(Point(x1, y2), Point(x2, y2))
                self._win.draw_line(line)
            self.initial_drawn = True
        else:
            if not self.has_left_wall:
                line = Line(Point(x1, y1), Point(x1, y2))
                self._win.draw_line(line, "white")
            if not self.has_top_wall:
                line = Line(Point(x1, y1), Point(x2, y1))
                self._win.draw_line(line, "white")
            if not self.has_right_wall:
                line = Line(Point(x2, y1), Point(x2, y2))
                self._win.draw_line(line, "white")
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
            Point(to_cell._x2 - ((to_cell._x2 - to_cell._x1) * 0.5 ), to_cell._y2 - ((to_cell._y2 - to_cell._y1) * 0.5))
            )
        self._win.draw_line(move_line, fill_color_move)


class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win, seed = None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._break_path_stack = []
        self._create_cells()
        self._break_entrance_and_exit()
        if seed:
            self.seed = random.seed(seed)
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        self.path_stack = []

    def _create_cells(self):
        self.cols = []
        i = self.x1
        j = self.y1
        k = 0
        l = 0
        for x in range(0, self.num_cols):
            self.cells = []
            for y in range(0, self.num_rows):
                y = Cell(self.win)
                self.cells.append(y)
            self.cols.append(self.cells)
        for col in self.cols:
            for cell in col:
                cell.name = f"{k}, {l}"
                l += 1
            k += 1
            l = 0
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

    def _break_walls_r(self, i, j, k = None, l = None):
        self.current_cell = self.cols[i][j]
        self.current_cell.visited = True
        if k != None and l != None:
            self._break_path_stack.append((k,l))
        while True:
            to_visit= []
            if i > 0:
                if self.cols[i-1][j].visited == False: #Cell to Left
                    to_visit.append((self.cols[i-1][j], "left"))
            if i < self.num_cols - 1:
                if self.cols[i+1][j].visited == False: #Cell to Right
                    to_visit.append((self.cols[i+1][j], "right")) 
            if j > 0:
                if self.cols[i][j-1].visited == False: #Cell Above
                    to_visit.append((self.cols[i][j-1], "up"))
            if j < self.num_rows - 1:
                if self.cols[i][j+1].visited == False: #Cell Below
                    to_visit.append((self.cols[i][j+1], "down"))
            if not to_visit:
                self.current_cell.draw(
                self.current_cell._x1,
                self.current_cell._y1,
                self.current_cell._x2,
                self.current_cell._y2
                )
                self._animate()
                if self._break_path_stack:
                    k, l = self._break_path_stack.pop()
                    self.current_cell = self.cols[k][l]
                return
            else:
                self.going, direction = to_visit.pop(random.randrange(len(to_visit)))
                self.going.visited = True
                if direction == "left":
                    self.current_cell.has_left_wall = False
                    self.going.has_right_wall = False
                    self.current_cell.draw(
                    self.current_cell._x1,
                    self.current_cell._y1,
                    self.current_cell._x2,
                    self.current_cell._y2
                    )
                    self._animate()
                    self._break_walls_r(i-1,j, i, j)
                if direction == "right":
                    self.current_cell.has_right_wall = False
                    self.going.has_left_wall = False
                    self.current_cell.draw(
                    self.current_cell._x1,
                    self.current_cell._y1,
                    self.current_cell._x2,
                    self.current_cell._y2
                    )
                    self._animate()
                    self._break_walls_r(i+1,j, i, j)
                if direction == "up":
                    self.current_cell.has_top_wall = False
                    self.going.has_bottom_wall = False
                    self.current_cell.draw(
                    self.current_cell._x1,
                    self.current_cell._y1,
                    self.current_cell._x2,
                    self.current_cell._y2
                    )
                    self._animate()
                    self._break_walls_r(i,j-1, i, j)
                if direction == "down":
                    self.current_cell.has_bottom_wall = False
                    self.going.has_top_wall = False
                    self.current_cell.draw(
                    self.current_cell._x1,
                    self.current_cell._y1,
                    self.current_cell._x2,
                    self.current_cell._y2
                    )
                    self._animate()
                    self._break_walls_r(i,j+1, i, j)

                    
    def _reset_cells_visited(self):
        for col in self.cols:
            for cell in col:
                cell.visited = False

    def _draw_cell(self, i, j, cell):
        cell.draw(i, j, i + self.cell_size_x, j + self.cell_size_y)
        self._animate()

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        self.current_cell = self.cols[i][j]
        self.current_cell.visited = True
        self.path_stack.append(self.current_cell)
        if self.current_cell == self.cols[self.num_cols-1][self.num_rows-1]:
            return True
        if i > 0 and self.current_cell.has_left_wall == False and self.cols[i-1][j].visited == False: #Cell to Left
            self.cell_to_left = self.cols[i-1][j]
            self.current_cell.draw_move(self.cell_to_left)
            if self._solve_r(i-1, j) == True:
                return True
            else:
                self.path_stack[-1].draw_move(self.path_stack[-2], True)
                self._animate()
                self.path_stack.pop()
                self.current_cell = self.path_stack[-1]
        if i < self.num_cols - 1 and self.current_cell.has_right_wall == False and self.cols[i+1][j].visited == False: #Cell to Right
            self.cell_to_right = self.cols[i+1][j]
            self.current_cell.draw_move(self.cell_to_right)
            if self._solve_r(i+1, j) == True:
                return True
            else:
                self.path_stack[-1].draw_move(self.path_stack[-2], True)
                self._animate()
                self.path_stack.pop()
                self.current_cell = self.path_stack[-1]
        if j > 0 and self.current_cell.has_top_wall == False and self.cols[i][j-1].visited == False: #Cell Above
            self.cell_above = self.cols[i][j-1]
            self.current_cell.draw_move(self.cell_above)
            if self._solve_r(i, j-1) == True:
                return True
            else:
                self.path_stack[-1].draw_move(self.path_stack[-2], True)
                self._animate()
                self.path_stack.pop()
                self.current_cell = self.path_stack[-1]
        if j < self.num_rows - 1 and self.current_cell.has_bottom_wall == False and self.cols[i][j+1].visited == False: #Cell Below
            self.cell_below = self.cols[i][j+1]
            self.current_cell.draw_move(self.cell_below)
            if self._solve_r(i, j+1) == True:
                return True
            else:
                self.path_stack[-1].draw_move(self.path_stack[-2], True)
                self._animate()
                self.path_stack.pop()
                self.current_cell = self.path_stack[-1]
        return False

    
    def _animate(self):
        self.win.redraw()
        time.sleep(0.01)

def main():
    win = Window(800, 800)

    m1 = Maze(50, 50, 25, 25, 25, 25, win)
    m1.solve()

    win.wait_for_close()


main()
