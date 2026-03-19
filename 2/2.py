import tkinter as tk
import random

class TetrisFalling:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная 2 - Часть 2: Падающие фигуры Тетриса (Вариант 6)")
        
        # Параметры
        self.block_size = 30
        self.grid_width = 10
        self.grid_height = 20
        self.canvas_width = self.grid_width * self.block_size
        self.canvas_height = self.grid_height * self.block_size
        
        # Фигуры Тетриса (координаты относительно центра)
        self.tetrominoes = [
            # I
            [[-1, 0], [0, 0], [1, 0], [2, 0]],
            # O
            [[0, 0], [1, 0], [0, 1], [1, 1]],
            # T
            [[-1, 0], [0, 0], [1, 0], [0, 1]],
            # S
            [[0, 0], [1, 0], [-1, 1], [0, 1]],
            # Z
            [[-1, 0], [0, 0], [0, 1], [1, 1]],
            # J
            [[-1, 0], [0, 0], [1, 0], [-1, 1]],
            # L
            [[-1, 0], [0, 0], [1, 0], [1, 1]]
        ]
        
        self.colors = ['cyan', 'yellow', 'purple', 'green', 'red', 'blue', 'orange']
        
        # Создаем холст
        self.canvas = tk.Canvas(root, width=self.canvas_width, 
                               height=self.canvas_height, bg='black')
        self.canvas.pack()
        
        # Создаем панель управления
        self.create_controls()
        
        # Текущая фигура
        self.current_piece = None
        self.current_color = None
        self.piece_x = self.grid_width // 2
        self.piece_y = 0
        
        # Запущен ли процесс
        self.is_running = False
        
        # Привязка клавиш
        self.root.bind('<Left>', self.move_left)
        self.root.bind('<Right>', self.move_right)
        self.root.bind('<Down>', self.move_down)
        self.root.bind('<Up>', self.rotate_piece)
        self.root.bind('<space>', self.drop_piece)
        
        # Запускаем первую фигуру
        self.new_piece()
        
        # Запускаем анимацию
        self.animate()
    
    def create_controls(self):
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10)
        
        ttk.Label(control_frame, text="Управление:").grid(row=0, column=0, 
                                                          columnspan=2, pady=5)
        ttk.Label(control_frame, text="← → : Перемещение").grid(row=1, column=0, 
                                                                sticky='w')
        ttk.Label(control_frame, text="↑ : Поворот").grid(row=2, column=0, 
                                                          sticky='w')
        ttk.Label(control_frame, text="↓ : Ускорить падение").grid(row=3, column=0, 
                                                                   sticky='w')
        ttk.Label(control_frame, text="Пробел : Быстрое падение").grid(row=4, column=0, 
                                                                       sticky='w')
        
        self.start_btn = ttk.Button(control_frame, text="Старт/Стоп", 
                                    command=self.toggle_start)
        self.start_btn.grid(row=5, column=0, padx=5, pady=5)
        
        self.reset_btn = ttk.Button(control_frame, text="Сброс", 
                                    command=self.reset_game)
        self.reset_btn.grid(row=5, column=1, padx=5, pady=5)
        
        self.status_label = ttk.Label(control_frame, text="Фигур упало: 0")
        self.status_label.grid(row=6, column=0, columnspan=2, pady=5)
        
        self.pieces_dropped = 0
    
    def new_piece(self):
        """Создание новой фигуры"""
        idx = random.randint(0, len(self.tetrominoes) - 1)
        self.current_piece = [coord[:] for coord in self.tetrominoes[idx]]
        self.current_color = self.colors[idx]
        self.piece_x = self.grid_width // 2
        self.piece_y = 0
        
        # Проверка на проигрыш
        if not self.is_valid_position(self.piece_x, self.piece_y, self.current_piece):
            self.is_running = False
            self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2,
                                   text="GAME OVER", fill='red', font=('Arial', 30))
    
    def is_valid_position(self, px, py, piece):
        """Проверка допустимости позиции"""
        for block in piece:
            x = px + block[0]
            y = py + block[1]
            
            # Выход за границы
            if x < 0 or x >= self.grid_width or y >= self.grid_height:
                return False
            # Отрицательный Y (над полем) - разрешаем
            if y < 0:
                continue
        
        return True
    
    def move_left(self, event):
        if self.is_running:
            if self.is_valid_position(self.piece_x - 1, self.piece_y, self.current_piece):
                self.piece_x -= 1
                self.draw()
    
    def move_right(self, event):
        if self.is_running:
            if self.is_valid_position(self.piece_x + 1, self.piece_y, self.current_piece):
                self.piece_x += 1
                self.draw()
    
    def move_down(self, event):
        if self.is_running:
            if self.is_valid_position(self.piece_x, self.piece_y + 1, self.current_piece):
                self.piece_y += 1
                self.draw()
    
    def rotate_piece(self, event):
        if self.is_running and self.current_piece:
            # Поворот на 90 градусов
            rotated = []
            for block in self.current_piece:
                rotated.append([-block[1], block[0]])
            
            if self.is_valid_position(self.piece_x, self.piece_y, rotated):
                self.current_piece = rotated
                self.draw()
    
    def drop_piece(self, event):
        if self.is_running:
            while self.is_valid_position(self.piece_x, self.piece_y + 1, 
                                        self.current_piece):
                self.piece_y += 1
            self.lock_piece()
            self.draw()
    
    def lock_piece(self):
        """Фиксация фигуры на поле"""
        # Здесь можно добавить логику сохранения зафиксированных фигур
        # Для простоты просто создаем новую фигуру
        self.pieces_dropped += 1
        self.status_label.config(text=f"Фигур упало: {self.pieces_dropped}")
        self.new_piece()
    
    def toggle_start(self):
        self.is_running = not self.is_running
        if self.is_running:
            self.start_btn.config(text="Стоп")
        else:
            self.start_btn.config(text="Старт")
    
    def reset_game(self):
        self.pieces_dropped = 0
        self.status_label.config(text="Фигур упало: 0")
        self.canvas.delete("all")
        self.draw_grid()
        self.new_piece()
        self.is_running = True
        self.start_btn.config(text="Стоп")
        self.draw()
    
    def draw_grid(self):
        """Рисование сетки"""
        for i in range(self.grid_width + 1):
            x = i * self.block_size
            self.canvas.create_line(x, 0, x, self.canvas_height, fill='gray')
        for i in range(self.grid_height + 1):
            y = i * self.block_size
            self.canvas.create_line(0, y, self.canvas_width, y, fill='gray')
    
    def draw(self):
        """Отрисовка текущей фигуры"""
        self.canvas.delete("piece")
        
        if self.current_piece:
            for block in self.current_piece:
                x = (self.piece_x + block[0]) * self.block_size
                y = (self.piece_y + block[1]) * self.block_size
                
                if y >= 0:  # Рисуем только видимые блоки
                    self.canvas.create_rectangle(
                        x + 1, y + 1, 
                        x + self.block_size - 1, y + self.block_size - 1,
                        fill=self.current_color, outline='white', tags="piece"
                    )
    
    def animate(self):
        """Анимация падения"""
        if self.is_running:
            if self.is_valid_position(self.piece_x, self.piece_y + 1, 
                                     self.current_piece):
                self.piece_y += 1
                self.draw()
            else:
                self.lock_piece()
                self.draw()
        
        self.root.after(500, self.animate)  # Скорость падения

# Добавляем импорт ttk
import tkinter.ttk as ttk

if __name__ == "__main__":
    root = tk.Tk()
    app = TetrisFalling(root)
    root.mainloop()