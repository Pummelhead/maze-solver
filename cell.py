from point_line import Line
from point_line import Point

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
