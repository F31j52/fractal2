import tkinter as tk
import math
import random

# ================= CONFIG =================
WIDTH, HEIGHT = 900, 650
BG = "#0b1020"
MAX_DEPTH = 12
ANGLE = 22
INITIAL_LEN = 110
RATIO = 0.76
JITTER = 4
ANIM_DELAY = 180  # ms entre gerações

# ================= SETUP =================
root = tk.Tk()
root.title("Fractal Tree")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG, highlightthickness=0)
canvas.pack()

current_depth = [1]
anim_running = [False]
after_id = [None]

# ================= DESENHO =================
def branch(x, y, length, angle_deg, depth, max_depth):
    if depth == 0:
        r = random.randint(80, 140)
        g = random.randint(200, 255)
        b = random.randint(80, 140)
        size = random.randint(2, 5)
        color = f"#{r:02x}{g:02x}{b:02x}"
        canvas.create_oval(x - size, y - size, x + size, y + size, fill=color, outline="")
        return

    ratio = depth / max_depth
    r = int(90 + (1 - ratio) * 40)
    g = int(50 + (1 - ratio) * 30)
    trunk_color = f"#{r:02x}{g:02x}14"
    width = max(1, int(depth * 0.55))

    rad = math.radians(angle_deg)
    ex = x + math.cos(rad) * length
    ey = y - math.sin(rad) * length

    canvas.create_line(x, y, ex, ey, fill=trunk_color, width=width)

    jitter = random.uniform(-JITTER, JITTER)
    a = ANGLE + jitter

    branch(ex, ey, length * RATIO, angle_deg + a, depth - 1, max_depth)
    branch(ex, ey, length * RATIO, angle_deg - a, depth - 1, max_depth)

def redraw(depth=None):
    canvas.delete("all")
    d = depth if depth is not None else current_depth[0]
    branch(WIDTH // 2, HEIGHT - 40, INITIAL_LEN, 90, d, MAX_DEPTH)

# ================= ANIMAÇÃO =================
def run_anim():
    if not anim_running[0]:
        return
    redraw(current_depth[0])
    if current_depth[0] < MAX_DEPTH:
        current_depth[0] += 1
        after_id[0] = root.after(ANIM_DELAY, run_anim)
    else:
        anim_running[0] = False
        btn_anim.config(text="▶ Animar")

def toggle_anim():
    if anim_running[0]:
        anim_running[0] = False
        if after_id[0]:
            root.after_cancel(after_id[0])
        btn_anim.config(text="▶ Animar")
    else:
        anim_running[0] = True
        current_depth[0] = 1
        btn_anim.config(text="⏹ Parar")
        run_anim()

# ================= CONTROLES =================
controls = tk.Frame(root, bg="#1a2040", pady=6)
controls.pack(fill=tk.X)

def make_slider(parent, label, var, from_, to, resolution, col):
    tk.Label(parent, text=label, bg="#1a2040", fg="#aab", font=("Courier", 9)).grid(
        row=0, column=col, padx=(12, 2))
    tk.Scale(parent, variable=var, from_=from_, to=to, resolution=resolution,
             orient=tk.HORIZONTAL, bg="#1a2040", fg="white", troughcolor="#0b1020",
             highlightthickness=0, length=110).grid(row=0, column=col+1, padx=(0, 8))

depth_var   = tk.IntVar(value=MAX_DEPTH)
angle_var   = tk.DoubleVar(value=ANGLE)
len_var     = tk.IntVar(value=INITIAL_LEN)
ratio_var   = tk.DoubleVar(value=RATIO)
jitter_var  = tk.DoubleVar(value=JITTER)

make_slider(controls, "Profundidade", depth_var,  1,  16, 1,    0)
make_slider(controls, "Ângulo °",     angle_var,  5,  60, 1,    2)
make_slider(controls, "Comprimento",  len_var,   40, 160, 1,    4)
make_slider(controls, "Proporção",    ratio_var, 0.5, 0.9, 0.01, 6)
make_slider(controls, "Variação",     jitter_var,  0,  15, 1,    8)

def on_slider_change(*_):
    global ANGLE, INITIAL_LEN, RATIO, JITTER, MAX_DEPTH
    MAX_DEPTH   = depth_var.get()
    ANGLE       = angle_var.get()
    INITIAL_LEN = len_var.get()
    RATIO       = ratio_var.get()
    JITTER      = jitter_var.get()
    if not anim_running[0]:
        redraw(MAX_DEPTH)

for v in (depth_var, angle_var, len_var, ratio_var, jitter_var):
    v.trace_add("write", on_slider_change)

btn_frame = tk.Frame(controls, bg="#1a2040")
btn_frame.grid(row=0, column=10, padx=12)

btn_anim = tk.Button(btn_frame, text="▶ Animar", command=toggle_anim,
                     bg="#263060", fg="white", relief=tk.FLAT, padx=10)
btn_anim.pack(side=tk.LEFT, padx=4)

tk.Button(btn_frame, text="↺ Redesenhar", command=lambda: redraw(MAX_DEPTH),
          bg="#263060", fg="white", relief=tk.FLAT, padx=10).pack(side=tk.LEFT)

# ================= START =================
redraw(MAX_DEPTH)
root.mainloop()