import time
import random
from cell import Cell

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
        self.line_path_stack = []

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
        self._draw_cell(self.cols[0][0]._x1,self.cols[0][0]._y1, self.cols[0][0])
        self._draw_cell(
            self.cols[self.num_cols-1][self.num_rows-1]._x1,
            self.cols[self.num_cols-1][self.num_rows-1]._y1,
            self.cols[self.num_cols-1][self.num_rows-1],
            )

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
                self._draw_cell(self.current_cell._x1,self.current_cell._y1, self.current_cell)
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
                    self._draw_cell(self.current_cell._x1,self.current_cell._y1, self.current_cell)
                    self._break_walls_r(i-1,j, i, j)
                if direction == "right":
                    self.current_cell.has_right_wall = False
                    self.going.has_left_wall = False
                    self._draw_cell(self.current_cell._x1,self.current_cell._y1, self.current_cell)
                    self._break_walls_r(i+1,j, i, j)
                if direction == "up":
                    self.current_cell.has_top_wall = False
                    self.going.has_bottom_wall = False
                    self._draw_cell(self.current_cell._x1,self.current_cell._y1, self.current_cell)
                    self._break_walls_r(i,j-1, i, j)
                if direction == "down":
                    self.current_cell.has_bottom_wall = False
                    self.going.has_top_wall = False
                    self._draw_cell(self.current_cell._x1,self.current_cell._y1, self.current_cell)
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
        self.line_path_stack.append(self.current_cell)
        if self.current_cell == self.cols[self.num_cols-1][self.num_rows-1]:
            return True
        if i > 0 and self.current_cell.has_left_wall == False and self.cols[i-1][j].visited == False: #Cell to Left
            self.cell_to_left = self.cols[i-1][j]
            self.current_cell.draw_move(self.cell_to_left)
            if self._solve_r(i-1, j) == True:
                return True
            else:
                self.line_path_stack[-1].draw_move(self.line_path_stack[-2], True)
                self._animate()
                self.line_path_stack.pop()
                self.current_cell = self.line_path_stack[-1]
        if i < self.num_cols - 1 and self.current_cell.has_right_wall == False and self.cols[i+1][j].visited == False: #Cell to Right
            self.cell_to_right = self.cols[i+1][j]
            self.current_cell.draw_move(self.cell_to_right)
            if self._solve_r(i+1, j) == True:
                return True
            else:
                self.line_path_stack[-1].draw_move(self.line_path_stack[-2], True)
                self._animate()
                self.line_path_stack.pop()
                self.current_cell = self.line_path_stack[-1]
        if j > 0 and self.current_cell.has_top_wall == False and self.cols[i][j-1].visited == False: #Cell Above
            self.cell_above = self.cols[i][j-1]
            self.current_cell.draw_move(self.cell_above)
            if self._solve_r(i, j-1) == True:
                return True
            else:
                self.line_path_stack[-1].draw_move(self.line_path_stack[-2], True)
                self._animate()
                self.line_path_stack.pop()
                self.current_cell = self.line_path_stack[-1]
        if j < self.num_rows - 1 and self.current_cell.has_bottom_wall == False and self.cols[i][j+1].visited == False: #Cell Below
            self.cell_below = self.cols[i][j+1]
            self.current_cell.draw_move(self.cell_below)
            if self._solve_r(i, j+1) == True:
                return True
            else:
                self.line_path_stack[-1].draw_move(self.line_path_stack[-2], True)
                self._animate()
                self.line_path_stack.pop()
                self.current_cell = self.line_path_stack[-1]
        return False
    
    def _animate(self):
        self.win.redraw()
        time.sleep(0.005)