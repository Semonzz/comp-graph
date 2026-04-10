import tkinter as tk
from tkinter import simpledialog
import math


# Матричные операции (3x3)

def mat_mult(A, B):
    """Умножение двух матриц 3x3 (A * B)."""
    result = [[0, 0, 0] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            total = 0
            for k in range(3):
                total += A[i][k] * B[k][j]
            result[i][j] = total
    return result

def transform_point(point, matrix):
    """Умножение вектора-строки (x, y, 1) на матрицу 3x3."""
    x, y = point
    x_new = x * matrix[0][0] + y * matrix[1][0] + 1 * matrix[2][0]
    y_new = x * matrix[0][1] + y * matrix[1][1] + 1 * matrix[2][1]
    return x_new, y_new


# Матрицы элементарных преобразований

def translation_matrix(dx, dy):
    """Матрица переноса на (dx, dy)."""
    return [[1, 0, 0],
            [0, 1, 0],
            [dx, dy, 1]]

def reflection_ox_matrix():
    """Отражение относительно оси OX (y -> -y)."""
    return [[1, 0, 0],
            [0, -1, 0],
            [0, 0, 1]]

def reflection_oy_matrix():
    """Отражение относительно оси OY (x -> -x)."""
    return [[-1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]]

def reflection_yx_matrix():
    """Отражение относительно прямой y=x."""
    return [[0, 1, 0],
            [1, 0, 0],
            [0, 0, 1]]

def scaling_matrix(sx, sy):
    """Масштабирование по осям."""
    return [[sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1]]

def rotation_matrix(angle_deg):
    """Поворот вокруг начала координат."""
    theta = math.radians(angle_deg)
    c, s = math.cos(theta), math.sin(theta)
    return [[c, s, 0],
            [-s, c, 0],
            [0, 0, 1]]

def rotation_around_point_matrix(angle_deg, cx, cy):
    """Поворот вокруг точки (cx, cy)."""
    T_inv = translation_matrix(-cx, -cy)
    R = rotation_matrix(angle_deg)
    T = translation_matrix(cx, cy)
    return mat_mult(mat_mult(T_inv, R), T)


class TransformApp:
    def __init__(self, root):
        self.star_points = None
        self.star_original = None
        self.root = root
        self.root.title("Преобразования фигур")

        self.width, self.height = 1000, 800
        self.center_x, self.center_y = self.width // 2, self.height // 2
        self.scale = 100
        self.view_range = 4

        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg='white')
        self.canvas.pack(side=tk.LEFT, padx=5, pady=5)

        self.control_frame = tk.Frame(root)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        self.init_shapes()
        self.redraw()
        self.create_buttons()

    def init_shapes(self):
        
        R, r = 1.5, 0.5
        self.star_original = []
        
        self.star_original.append((0, R))
        angle = math.radians(45)
        self.star_original.append((r * math.cos(angle), r * math.sin(angle)))
        self.star_original.append((R, 0))
        angle = math.radians(-45)
        self.star_original.append((r * math.cos(angle), r * math.sin(angle)))
        self.star_original.append((0, -R))
        angle = math.radians(-135)
        self.star_original.append((r * math.cos(angle), r * math.sin(angle)))
        self.star_original.append((-R, 0))
        angle = math.radians(135)
        self.star_original.append((r * math.cos(angle), r * math.sin(angle)))
        
        self.star_points = self.star_original[:]

    def world_to_window(self, x, y):
        """Преобразование мировых координат в экранные"""
        return self.center_x + x * self.scale, self.center_y - y * self.scale

    def draw_grid(self):
        """Cеткa"""
        for x in range(-self.view_range, self.view_range + 1):
            wx1, wy1 = self.world_to_window(x, -self.view_range)
            wx2, wy2 = self.world_to_window(x, self.view_range)
            color, width = ('black', 2) if x == 0 else ('lightgray', 1)
            self.canvas.create_line(wx1, wy1, wx2, wy2, fill=color, width=width)
            if x != 0:
                lx, ly = self.world_to_window(x, -self.view_range + 0.25)
                self.canvas.create_text(lx, ly, text=str(x), fill='gray', font=('Arial', 8), anchor='n')
        
        for y in range(-self.view_range, self.view_range + 1):
            wx1, wy1 = self.world_to_window(-self.view_range, y)
            wx2, wy2 = self.world_to_window(self.view_range, y)
            color, width = ('black', 2) if y == 0 else ('lightgray', 1)
            self.canvas.create_line(wx1, wy1, wx2, wy2, fill=color, width=width)
            if y != 0:
                lx, ly = self.world_to_window(-self.view_range + 0.3, y)
                self.canvas.create_text(lx, ly, text=str(y), fill='gray', font=('Arial', 8), anchor='e')

    def redraw(self):
        self.canvas.delete("all")
        self.draw_grid()
        
        star_win = [self.world_to_window(x, y) for x, y in self.star_points]
        
        # Ромб (внешние вершины)
        if len(star_win) >= 7:
            rhomb = [star_win[i] for i in [0, 2, 4, 6]]
            self.canvas.create_polygon(rhomb, fill='', outline='blue', width=2)
            self.canvas.create_line(star_win[0], star_win[4], fill='blue', width=1)
            self.canvas.create_line(star_win[2], star_win[6], fill='blue', width=1)
        
        # Контур звезды
        if len(star_win) > 2:
            closed = star_win + [star_win[0]]
            for i in range(len(star_win)):
                self.canvas.create_line(closed[i], closed[i+1], fill='red', width=2)

    def apply_transform(self, matrix):
        self.star_points = [transform_point(p, matrix) for p in self.star_points]
        self.redraw()

    def reset(self):
        self.star_points = self.star_original[:]
        self.redraw()

    def move_ox(self):
        d = simpledialog.askfloat("Перенос OX", "Величина переноса по OX:", minvalue=-2, maxvalue=2, parent=self.root)
        if d is not None:
            self.apply_transform(translation_matrix(d, 0))

    def move_oy(self):
        d = simpledialog.askfloat("Перенос OY", "Величина переноса по OY:", minvalue=-2, maxvalue=2, parent=self.root)
        if d is not None:
            self.apply_transform(translation_matrix(0, d))

    def reflect_ox(self): self.apply_transform(reflection_ox_matrix())
    def reflect_oy(self): self.apply_transform(reflection_oy_matrix())
    def reflect_yx(self): self.apply_transform(reflection_yx_matrix())

    def do_scale(self):
        sx = simpledialog.askfloat("Масштаб OX", "Коэффициент по OX:", minvalue=0.1, maxvalue=5, parent=self.root)
        if sx is None: return
        sy = simpledialog.askfloat("Масштаб OY", "Коэффициент по OY:", minvalue=0.1, maxvalue=5, parent=self.root)
        if sy is not None:
            self.apply_transform(scaling_matrix(sx, sy))

    def rotate_origin(self):
        angle = simpledialog.askfloat("Поворот", "Угол (градусы):", minvalue=-360, maxvalue=360, parent=self.root)
        if angle is not None:
            self.apply_transform(rotation_matrix(angle))

    def rotate_around_point(self):
        cx = simpledialog.askfloat("Центр поворота", "Координата X:", minvalue=-100, maxvalue=100, parent=self.root)
        if cx is None: return
        cy = simpledialog.askfloat("Центр поворота", "Координата Y:", minvalue=-100, maxvalue=100, parent=self.root)
        if cy is None: return
        angle = simpledialog.askfloat("Поворот", "Угол (градусы):", minvalue=-360, maxvalue=360, parent=self.root)
        if angle is not None:
            self.apply_transform(rotation_around_point_matrix(angle, cx, cy))

    def create_buttons(self):
        buttons = [
            ("Перенос OX", self.move_ox),
            ("Перенос OY", self.move_oy),
            ("Отражение OX", self.reflect_ox),
            ("Отражение OY", self.reflect_oy),
            ("Отражение Y=X", self.reflect_yx),
            ("Масштабирование", self.do_scale),
            ("Поворот вокруг центра", self.rotate_origin),
            ("Поворот вокруг точки", self.rotate_around_point),
            ("Восстановить", self.reset),
        ]
        for text, cmd in buttons:
            tk.Button(self.control_frame, text=text, width=20, command=cmd).pack(pady=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = TransformApp(root)
    root.mainloop()
