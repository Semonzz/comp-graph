import tkinter as tk
import random
import math
import time

# ==========================================
# МАТРИЧНЫЕ ОПЕРАЦИИ (из Части 1)
# ==========================================

def mat_mult(A, B):
    result = [[0, 0, 0] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            total = 0
            for k in range(3):
                total += A[i][k] * B[k][j]
            result[i][j] = total
    return result

def transform_point(point, matrix):
    x, y = point
    x_new = x * matrix[0][0] + y * matrix[1][0] + 1 * matrix[2][0]
    y_new = x * matrix[0][1] + y * matrix[1][1] + 1 * matrix[2][1]
    return x_new, y_new

def translation_matrix(dx, dy):
    return [[1, 0, 0],
            [0, 1, 0],
            [dx, dy, 1]]

def rotation_matrix(angle_deg):
    theta = math.radians(angle_deg)
    c = math.cos(theta)
    s = math.sin(theta)
    return [[c, s, 0],
            [-s, c, 0],
            [0, 0, 1]]

def rotation_around_point_matrix(angle_deg, cx, cy):
    T_inv = translation_matrix(-cx, -cy)
    R = rotation_matrix(angle_deg)
    T = translation_matrix(cx, cy)
    return mat_mult(mat_mult(T_inv, R), T)

# ==========================================
# ПАДАЮЩИЕ ФИГУРЫ
# ==========================================

BLOCK_SIZE = 30
COLS = 10
ROWS = 20
WIDTH = COLS * BLOCK_SIZE
HEIGHT = ROWS * BLOCK_SIZE

# Фигуры: список блоков относительно "начала" фигуры
SHAPES = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],  # I
    [(0, 0), (1, 0), (0, 1), (1, 1)],  # O
    [(0, 0), (1, 0), (2, 0), (1, 1)],  # T
    [(0, 0), (1, 0), (1, 1), (2, 1)],  # S
    [(0, 1), (1, 1), (1, 0), (2, 0)],  # Z
    [(0, 0), (0, 1), (1, 1), (2, 1)],  # L
    [(0, 1), (1, 1), (2, 1), (2, 0)],  # J
]
COLORS = ['cyan', 'yellow', 'purple', 'green', 'red', 'orange', 'blue']


class FallingShapes:
    def __init__(self, root):
        self.root = root
        self.root.title("Task2")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='black')
        self.canvas.pack()

        self.current_shape = None
        self.current_color = None
        self.pos = (0, 0)  # Позиция фигуры на поле
        self.fallen = False  # Флаг: фигура достигла дна

        self.spawn_shape()

        # Управление
        self.root.bind("<Left>", lambda e: self.move(-1, 0))
        self.root.bind("<Right>", lambda e: self.move(1, 0))
        self.root.bind("<Down>", lambda e: self.move(0, 1))
        self.root.bind("<Up>", lambda e: self.rotate())
        self.root.bind("<space>", lambda e: self.instant_drop())

        # Игровой цикл
        self.last_time = time.time()
        self.fall_speed = 0.4
        self.game_loop()

    def spawn_shape(self):
        """Создаёт новую случайную фигуру вверху экрана"""
        idx = random.randint(0, len(SHAPES) - 1)
        self.current_shape = SHAPES[idx][:]  # Копия списка
        self.current_color = COLORS[idx]
        self.pos = (COLS // 2 - 1, -2)  # Старт сверху по центру
        self.fallen = False

    def get_center(self):
        """Вычисляет центр масс фигуры для поворота"""
        n = len(self.current_shape)
        cx = sum(b[0] for b in self.current_shape) / n
        cy = sum(b[1] for b in self.current_shape) / n
        return cx, cy

    def move(self, dx, dy):
        """Сдвиг фигуры на (dx, dy) клеток"""
        self.pos = (self.pos[0] + dx, self.pos[1] + dy)

    def rotate(self):
        """Поворот через матрицу, но с целочисленным pivot"""
        if not self.current_shape:
            return
        
        # Pivot — первый блок (целые координаты!)
        pivot_x, pivot_y = self.current_shape[1]
        
        # Матрица поворота на 90°
        rot_mat = rotation_matrix(90)
        
        new_blocks = []
        for bx, by in self.current_shape:
            # Сдвигаем к pivot
            rel_x, rel_y = bx - pivot_x, by - pivot_y
            
            # Применяем матрицу к относительным координатам
            rx, ry = transform_point((rel_x, rel_y), rot_mat)
            
            # Округляем и возвращаем к pivot
            new_blocks.append((round(rx) + pivot_x, round(ry) + pivot_y))
        
        self.current_shape = new_blocks

    def instant_drop(self):
        """Мгновенное падение на дно"""
        while not self.fallen:
            self.pos = (self.pos[0], self.pos[1] + 1)
            self.check_landed()

    def check_landed(self):
        """Проверяет, достигла ли фигура дна"""
        # Находим самую нижнюю точку фигуры
        max_y = max(by for _, by in self.current_shape)
        bottom_y = self.pos[1] + max_y
        
        if bottom_y >= ROWS - 1:
            self.fallen = True
            # Через один тик очистим экран
            self.root.after(200, self.reset_screen)

    def reset_screen(self):
        """Очистка экрана и спавн новой фигуры"""
        self.spawn_shape()

    def draw(self):
        self.canvas.delete("all")
        
        # Сетка (для красоты)
        for i in range(COLS + 1):
            self.canvas.create_line(i * BLOCK_SIZE, 0, i * BLOCK_SIZE, HEIGHT, fill='#222')
        for i in range(ROWS + 1):
            self.canvas.create_line(0, i * BLOCK_SIZE, WIDTH, i * BLOCK_SIZE, fill='#222')
        
        # Рисуем текущую фигуру
        if self.current_shape:
            for bx, by in self.current_shape:
                x = (self.pos[0] + bx) * BLOCK_SIZE
                y = (self.pos[1] + by) * BLOCK_SIZE
                # Рисуем только если блок в пределах экрана
                if -BLOCK_SIZE < x < WIDTH and -BLOCK_SIZE < y < HEIGHT:
                    self.canvas.create_rectangle(
                        x + 2, y + 2, x + BLOCK_SIZE - 2, y + BLOCK_SIZE - 2,
                        fill=self.current_color, outline='white'
                    )

    def game_loop(self):
        if not self.fallen:
            now = time.time()
            if now - self.last_time > self.fall_speed:
                self.pos = (self.pos[0], self.pos[1] + 1)
                self.check_landed()
                self.last_time = now
            
            self.draw()
            self.root.after(30, self.game_loop)
        else:
            self.draw()
            self.root.after(30, self.game_loop)


if __name__ == "__main__":
    root = tk.Tk()
    app = FallingShapes(root)
    root.mainloop()
