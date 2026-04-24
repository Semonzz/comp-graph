import tkinter as tk
from tkinter import ttk

class RasterizationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная работа 3")
        self.root.geometry("850x700")

        self.width = 800
        self.height = 650
        self.grid_size = 20
        

        self.create_ui()

        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="white")
        self.canvas.pack(pady=10)

        self.draw_grid()

    def create_ui(self):
        frame = ttk.Frame(self.root)
        frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(frame, text="Отрезок (x1, y1, x2, y2):").grid(row=0, column=0, sticky="w")
        self.line_entries = []
        defaults = ["-5", "5", "15", "-5"] 
        for i, val in enumerate(defaults):
            e = ttk.Entry(frame, width=5)
            e.grid(row=0, column=i+1, padx=2)
            e.insert(0, val)
            self.line_entries.append(e)
        
        ttk.Button(frame, text="Отрезок", command=self.draw_line_ui).grid(row=0, column=5, padx=5)

        ttk.Label(frame, text="Окружность (cx, cy, r):").grid(row=1, column=0, sticky="w")
        self.circle_entries = []
        defaults = ["5", "5", "10"]
        for i, val in enumerate(defaults):
            e = ttk.Entry(frame, width=5)
            e.grid(row=1, column=i+1, padx=2)
            e.insert(0, val)
            self.circle_entries.append(e)

        ttk.Button(frame, text="Окружность", command=self.draw_circle_ui).grid(row=1, column=4, padx=5)
        ttk.Button(frame, text="Очистить", command=self.clear_canvas).grid(row=1, column=5, padx=5)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.draw_grid()

    def to_screen(self, x, y):
        center_x = self.width / 2
        center_y = self.height / 2
        sx = center_x + (x * self.grid_size)
        sy = center_y - (y * self.grid_size)
        return sx, sy

    def draw_grid(self):
        center_x = self.width / 2
        center_y = self.height / 2
        
        for i in range(-100, 100):
            x = center_x + i * self.grid_size
            color = "gray" if i != 0 else "black"
            width = 1 if i != 0 else 2
            self.canvas.create_line(x, 0, x, self.height, fill=color, width=width)

        for i in range(-100, 100):
            y = center_y + i * self.grid_size
            color = "gray" if i != 0 else "black"
            width = 1 if i != 0 else 2
            self.canvas.create_line(0, y, self.width, y, fill=color, width=width)

    def bresenham_line(self, x0, y0, x1, y1):
        points = []
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        points.append((x0, y0))

        if dx>=dy:
            d = 2*dy-dx
            while(x!=x1):
                if d<0:
                    d +=2*dy
                else:
                    y+=sy
                    d+=2*(dy-dx)
                x+=sx
                points.append((x, y))
        else:
            d = 2*dx-dy
            while(y!=y1):
                if d<0:
                    d +=2*dx
                else:
                    x+=sx
                    d+=2*(dx-dy)
                y+=sy
                points.append((x, y))
        return points

    def draw_line_ui(self):
        self.clear_canvas()
        try:
            x1, y1, x2, y2 = [int(e.get()) for e in self.line_entries]
        except ValueError:
            return

        sx1, sy1 = self.to_screen(x1, y1)
        sx2, sy2 = self.to_screen(x2, y2)
        self.canvas.create_line(sx1, sy1, sx2, sy2, fill="red", width=2)

        pixels = self.bresenham_line(x1, y1, x2, y2)
        for px, py in pixels:
            sx, sy = self.to_screen(px, py)
            self.canvas.create_oval(sx-2, sy-2, sx+2, sy+2, fill="black", outline="")

    def bresenham_circle(self, cx, cy, r):
        points = []
        x, y = 0, r
        d = 1 - r 

        def add_symmetric(x, y):
            points.extend([
                (cx + x, cy + y), (cx - x, cy + y),
                (cx + x, cy - y), (cx - x, cy - y),
                (cx + y, cy + x), (cx - y, cy + x),
                (cx + y, cy - x), (cx - y, cy - x)
            ])

        while x <= y:
            add_symmetric(x, y)
            if d < 0:
                d += 2 * x + 3
            else:
                y -= 1
                d += 2 * (x - y) + 5
            x += 1
        return points

    def draw_circle_ui(self):
        self.clear_canvas()
        try:
            cx = int(self.circle_entries[0].get())
            cy = int(self.circle_entries[1].get())
            r = int(self.circle_entries[2].get())
        except ValueError:
            return
        
        tl_x, tl_y = self.to_screen(cx - r, cy + r) 
        br_x, br_y = self.to_screen(cx + r, cy - r)

        self.canvas.create_oval(tl_x, tl_y, br_x, br_y, outline="red", width=2)

        pixels = self.bresenham_circle(cx, cy, r)
        for px, py in pixels:
            sx, sy = self.to_screen(px, py)
            self.canvas.create_oval(sx-2, sy-2, sx+2, sy+2, fill="black", outline="")

if __name__ == "__main__":
    root = tk.Tk()
    app = RasterizationApp(root)
    root.mainloop()
