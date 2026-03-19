import tkinter as tk
from tkinter import ttk
import math

class GeometricTransformations:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная 2 - Часть 1: Геометрические преобразования")
        
        # Исходные фигуры (квадрат и треугольник)
        self.original_figures = [
            # Квадрат (4 вершины)
            [[-50, -50, 1], [50, -50, 1], [50, 50, 1], [-50, 50, 1]],
            # Треугольник (3 вершины)
            [[0, -80, 1], [60, 40, 1], [-60, 40, 1]]
        ]
        
        # Текущие фигуры
        self.figures = [self.copy_figure(f) for f in self.original_figures]
        
        # Создаем холст
        self.canvas = tk.Canvas(root, width=600, height=600, bg='white')
        self.canvas.pack()
        
        # Рисуем оси
        self.draw_axes()
        
        # Создаем панель управления
        self.create_controls()
        
        # Рисуем фигуры
        self.draw_figures()
    
    def copy_figure(self, figure):
        return [[p[0], p[1], p[2]] for p in figure]
    
    def draw_axes(self):
        center_x, center_y = 300, 300
        # Ось X
        self.canvas.create_line(50, center_y, 550, center_y, fill='black', width=2)
        # Ось Y
        self.canvas.create_line(center_x, 50, center_x, 550, fill='black', width=2)
        # Подписи
        self.canvas.create_text(540, center_y + 15, text='X')
        self.canvas.create_text(center_x + 15, 60, text='Y')
    
    def create_controls(self):
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10)
        
        # Кнопки преобразований
        buttons = [
            ("Перенос OX (+50)", self.translate_ox),
            ("Перенос OY (+50)", self.translate_oy),
            ("Отражение OX", self.reflect_ox),
            ("Отражение OY", self.reflect_oy),
            ("Отражение Y=X", self.reflect_yx),
            ("Масштабирование (1.5)", self.scale_figures),
            ("Поворот (30°)", self.rotate_origin),
            ("Поворот вокруг точки", self.rotate_point),
            ("Восстановить", self.restore),
            ("Очистить холст", self.clear_canvas)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(control_frame, text=text, command=command)
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
        
        # Поле для угла поворота
        ttk.Label(control_frame, text="Угол (градусы):").grid(row=3, column=0, padx=5)
        self.angle_entry = ttk.Entry(control_frame, width=10)
        self.angle_entry.insert(0, "30")
        self.angle_entry.grid(row=3, column=1, padx=5)
        
        # Поле для точки поворота
        ttk.Label(control_frame, text="Точка (x,y):").grid(row=3, column=2, padx=5)
        self.point_entry = ttk.Entry(control_frame, width=10)
        self.point_entry.insert(0, "100,100")
        self.point_entry.grid(row=4, column=2, padx=5)
    
    def matrix_multiply(self, point, matrix):
        """Умножение матрицы 1×3 на матрицу 3×3"""
        result = [0, 0, 0]
        for i in range(3):
            for j in range(3):
                result[i] += point[j] * matrix[j][i]
        return result
    
    def apply_transformation(self, matrix):
        """Применение матрицы преобразования ко всем фигурам"""
        for i, figure in enumerate(self.figures):
            for j, point in enumerate(figure):
                self.figures[i][j] = self.matrix_multiply(point, matrix)
        self.draw_figures()
    
    def translate_ox(self):
        """Перенос вдоль оси OX"""
        dx = 50
        matrix = [
            [1, 0, 0],
            [0, 1, 0],
            [dx, 0, 1]
        ]
        self.apply_transformation(matrix)
    
    def translate_oy(self):
        """Перенос вдоль оси OY"""
        dy = 50
        matrix = [
            [1, 0, 0],
            [0, 1, 0],
            [0, dy, 1]
        ]
        self.apply_transformation(matrix)
    
    def reflect_ox(self):
        """Отражение относительно оси OX"""
        matrix = [
            [1, 0, 0],
            [0, -1, 0],
            [0, 0, 1]
        ]
        self.apply_transformation(matrix)
    
    def reflect_oy(self):
        """Отражение относительно оси OY"""
        matrix = [
            [-1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]
        self.apply_transformation(matrix)
    
    def reflect_yx(self):
        """Отражение относительно прямой Y=X"""
        matrix = [
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, 1]
        ]
        self.apply_transformation(matrix)
    
    def scale_figures(self):
        """Масштабирование независимо по осям"""
        sx, sy = 1.5, 1.5
        matrix = [
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1]
        ]
        self.apply_transformation(matrix)
    
    def rotate_origin(self):
        """Поворот относительно центра координат"""
        try:
            angle = float(self.angle_entry.get())
        except:
            angle = 30
        
        rad = math.radians(angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        
        matrix = [
            [cos_a, sin_a, 0],
            [-sin_a, cos_a, 0],
            [0, 0, 1]
        ]
        self.apply_transformation(matrix)
    
    def rotate_point(self):
        """Поворот относительно произвольной точки"""
        try:
            angle = float(self.angle_entry.get())
            point_str = self.point_entry.get().split(',')
            px, py = float(point_str[0]), float(point_str[1])
        except:
            angle = 30
            px, py = 100, 100
        
        rad = math.radians(angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        
        # Матрица поворота вокруг произвольной точки
        matrix = [
            [cos_a, sin_a, 0],
            [-sin_a, cos_a, 0],
            [px - px*cos_a + py*sin_a, py - px*sin_a - py*cos_a, 1]
        ]
        self.apply_transformation(matrix)
    
    def restore(self):
        """Восстановление исходной позиции"""
        self.figures = [self.copy_figure(f) for f in self.original_figures]
        self.draw_figures()
    
    def clear_canvas(self):
        """Очистка холста"""
        self.canvas.delete("all")
        self.draw_axes()
        self.restore()
    
    def draw_figures(self):
        """Отрисовка фигур"""
        # Очищаем только фигуры (не оси)
        self.canvas.delete("figure")
        
        colors = ['red', 'blue']
        for i, figure in enumerate(self.figures):
            points = []
            for point in figure:
                # Преобразование координат (центр окна = 0,0)
                x = 300 + point[0]
                y = 300 - point[1]  # Инвертируем Y для экранной системы
                points.extend([x, y])
            
            self.canvas.create_polygon(points, outline=colors[i], 
                                       fill='', width=2, tags="figure")
            
            # Рисуем вершины
            for point in figure:
                x = 300 + point[0]
                y = 300 - point[1]
                self.canvas.create_oval(x-3, y-3, x+3, y+3, 
                                       fill=colors[i], tags="figure")

if __name__ == "__main__":
    root = tk.Tk()
    app = GeometricTransformations(root)
    root.mainloop()