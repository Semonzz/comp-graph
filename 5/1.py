import tkinter as tk
from PIL import Image, ImageTk

WIDTH = 800
HEIGHT = 600
X_PARTITION = 420

buffer = [[False] * WIDTH for _ in range(HEIGHT)]

vertices = [
    (300, 100), (500, 150), (550, 300), (400, 400), (250, 350)
]

current_edge = 0
finished = False

def process(i):
    global current_edge, finished
    p1 = vertices[i]
    p2 = vertices[(i + 1) % len(vertices)]
    
    if p1[1] == p2[1]:
        return

    y1, y2 = p1[1], p2[1]
    x1, x2 = p1[0], p2[0]
    
    if y1 > y2:
        y1, y2 = y2, y1
        x1, x2 = x2, x1
        
    dy = y2 - y1
    dx = x2 - x1

    for y in range(y1, y2):
        if y < 0 or y >= HEIGHT:
            continue
            
        t = 0.0 if dy == 0 else (y - y1) / dy
        x_edge_double = x1 + dx * t
        x_edge = round(x_edge_double)

        left = min(x_edge, X_PARTITION)
        right = max(x_edge, X_PARTITION)
        
        for x in range(left, right + 1):
            if 0 <= x < WIDTH:
                buffer[y][x] = not buffer[y][x]

def clear():
    global current_edge, finished
    global buffer
    buffer = [[False] * WIDTH for _ in range(HEIGHT)]
    current_edge = 0
    finished = False
    render()

def step():
    global current_edge, finished
    if finished or not vertices:
        return False
    if current_edge >= len(vertices):
        finished = True
        return False
        
    process(current_edge)
    print(f"Processed edge {current_edge + 1} of {len(vertices)}")
    current_edge += 1
    
    if current_edge >= len(vertices):
        finished = True
        print("Fill complete.")
        
    render()
    return True

def fill_all():
    while step():
        pass

def render():
    canvas.delete("all")

    img = Image.new("RGB", (WIDTH, HEIGHT), "black")
    pixels = img.load()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if buffer[y][x]:
                pixels[x, HEIGHT - 1 - y] = (0, 0, 255)
                
    img_tk = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, image=img_tk, anchor="nw")
    canvas.image = img_tk

    
    if len(vertices) >= 3:
        coords = []
        for p in vertices:
            coords.extend([p[0], HEIGHT - 1 - p[1]])
        coords.extend([vertices[0][0], HEIGHT - 1 - vertices[0][1]])
        canvas.create_line(coords, fill="red", width=2)

    canvas.create_line(X_PARTITION, 0, X_PARTITION, HEIGHT, fill="green", width=3)

def main():
    global canvas
    root = tk.Tk()
    root.title("XOR-2 with partition (Tkinter)")
    root.resizable(False, False)

    root.bind("<space>", lambda e: step())
    root.bind("<r>", lambda e: clear())
    root.bind("<R>", lambda e: clear())
    root.bind("<f>", lambda e: fill_all())
    root.bind("<F>", lambda e: fill_all())

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
    canvas.pack()

    render()
    root.mainloop()

if __name__ == "__main__":
    main()
