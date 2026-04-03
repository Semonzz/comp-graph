import tkinter as tk
from tkinter import simpledialog
import math


# Матричные операции (3x3)

def mat_mult(A, B):
    """Умножение двух матриц 3x3 (A * B)."""
    result = [[0, 0, 0] for _ in range(3)]

    for i in range(3):  # строка результата
        for j in range(3):  # столбец результата
            total = 0
            for k in range(3):  # общий индекс суммирования
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
    return [
        [1, 0, 0],
        [0, 1, 0],
        [dx, dy, 1]
    ]

def reflection_ox_matrix():
    """Отражение относительно оси OX (y -> -y)."""
    return [
        [1, 0, 0],
        [0, -1, 0],
        [0, 0, 1]
    ]

def reflection_oy_matrix():
    """Отражение относительно оси OY (x -> -x)."""
    return [
        [-1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]

def reflection_yx_matrix():
    """Отражение относительно прямой y=x."""
    return [
        [0, 1, 0],
        [1, 0, 0],
        [0, 0, 1]
    ]

def scaling_matrix(sx, sy):
    """Масштабирование по осям (независимо)."""
    return [
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ]

def rotation_matrix(angle_deg):
    """Поворот вокруг начала координат на угол angle_deg градусов."""
    theta = math.radians(angle_deg)
    c = math.cos(theta)
    s = math.sin(theta)
    return [
        [c, s, 0],
        [-s, c, 0],
        [0, 0, 1]
    ]

def rotation_around_point_matrix(angle_deg, cx, cy):
    """Поворот на угол angle_deg вокруг точки (cx, cy)."""
    T_inv = translation_matrix(-cx, -cy)
    R = rotation_matrix(angle_deg)
    T = translation_matrix(cx, cy)
    return mat_mult(mat_mult(T_inv, R), T)


# Основное приложение

class TransformApp:
    def __init__(self, root):
        self.star_points = None
        self.star_original = None
        self.root = root
        self.root.title("Преобразования фигур")

        self.width = 1000
        self.height = 800
        self.center_x = self.width // 2
        self.center_y = self.height // 2

        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg='white')
        self.canvas.pack(side=tk.LEFT, padx=5, pady=5)

        self.control_frame = tk.Frame(root)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        self.init_shapes()
        self.redraw()
        self.create_buttons()

    def init_shapes(self):
        """Задание вершин четырехконечной звезды (центр в (0,0))."""
        R = 150.0   # внешний радиус
        r = 60.0    # внутренний радиус
        
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

    def redraw(self):
        self.canvas.delete("all")
        self.canvas.create_line(0, self.center_y, self.width, self.center_y, fill='light gray')
        self.canvas.create_line(self.center_x, 0, self.center_x, self.height, fill='light gray')

        def world_to_window(x, y):
            wx = self.center_x + x
            wy = self.center_y - y
            return wx, wy

        star_win = [world_to_window(x, y) for (x, y) in self.star_points]
        
        if len(star_win) >= 7:
            rhomb_points = [
                star_win[0],
                star_win[2],
                star_win[4],
                star_win[6],
            ]
            self.canvas.create_polygon(rhomb_points, fill='', outline='black', width=2)
        
        if len(star_win) >= 7:
            self.canvas.create_line(
                star_win[0], star_win[4],
                fill='black', width=1
            )
            self.canvas.create_line(
                star_win[2], star_win[6],
                fill='black', width=1
            )
        
        if len(star_win) > 2:
            star_line = star_win + [star_win[0]]
            for i in range(len(star_win)):
                self.canvas.create_line(
                    star_line[i], star_line[i+1],
                    fill='black', width=1
                )

    def apply_transform(self, matrix):
        self.star_points = [transform_point(p, matrix) for p in self.star_points]
        self.redraw()

    def reset(self):
        self.star_points = self.star_original[:]
        self.redraw()

    # Обработчики кнопок
    def move_ox(self):
        d = simpledialog.askfloat("Перенос OX", "Введите величину переноса по OX:", minvalue=-1000, maxvalue=1000)
        if d is not None:
            self.apply_transform(translation_matrix(d, 0))

    def move_oy(self):
        d = simpledialog.askfloat("Перенос OY", "Введите величину переноса по OY:", minvalue=-1000, maxvalue=1000)
        if d is not None:
            self.apply_transform(translation_matrix(0, d))

    def reflect_ox(self):
        self.apply_transform(reflection_ox_matrix())

    def reflect_oy(self):
        self.apply_transform(reflection_oy_matrix())

    def reflect_yx(self):
        self.apply_transform(reflection_yx_matrix())

    def scale(self):
        sx = simpledialog.askfloat("Масштаб OX", "Коэффициент масштабирования по OX:", minvalue=0.1, maxvalue=10)
        if sx is None:
            return
        sy = simpledialog.askfloat("Масштаб OY", "Коэффициент масштабирования по OY:", minvalue=0.1, maxvalue=10)
        if sy is not None:
            self.apply_transform(scaling_matrix(sx, sy))

    def rotate_origin(self):
        angle = simpledialog.askfloat("Поворот вокруг центра", "Угол поворота (градусы):", minvalue=-360, maxvalue=360)
        if angle is not None:
            self.apply_transform(rotation_matrix(angle))

    def rotate_around_point(self):
        cx = simpledialog.askfloat("Точка поворота", "Координата X центра поворота:", minvalue=-1000, maxvalue=1000)
        if cx is None:
            return
        cy = simpledialog.askfloat("Точка поворота", "Координата Y центра поворота:", minvalue=-1000, maxvalue=1000)
        if cy is None:
            return
        angle = simpledialog.askfloat("Поворот вокруг точки", "Угол поворота (градусы):", minvalue=-360, maxvalue=360)
        if angle is not None:
            self.apply_transform(rotation_around_point_matrix(angle, cx, cy))

    def create_buttons(self):
        buttons = [
            ("Перенос OX", self.move_ox),
            ("Перенос OY", self.move_oy),
            ("Отражение OX", self.reflect_ox),
            ("Отражение OY", self.reflect_oy),
            ("Отражение Y=X", self.reflect_yx),
            ("Масштабирование", self.scale),
            ("Поворот вокруг центра", self.rotate_origin),
            ("Поворот вокруг точки", self.rotate_around_point),
            ("Восстановить", self.reset),
        ]
        for text, command in buttons:
            btn = tk.Button(self.control_frame, text=text, width=20, command=command)
            btn.pack(pady=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = TransformApp(root)
    root.mainloop()
