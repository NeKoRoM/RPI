import tkinter as tk
from serial.tools import list_ports
from pydobot import Dobot

# Підключення до Dobot
port = list_ports.comports()[0].device
device = Dobot(port=port, verbose=True)

# Глобальні змінні для позиції
x, y, z, r = 0, 0, 0, 0
MAX_POSITION = 1999  # Максимальне значення для X, Y, Z

def update_pose():
    """Зчитує поточну позицію Dobot і оновлює мітку."""
    global x, y, z, r
    (x, y, z, r, j1, j2, j3, j4) = device.pose()
    label_pose.config(text=f"Позиція: x:{x:.2f} y:{y:.2f} z:{z:.2f} r:{r:.2f}")

def limit_position(val):
    """Обмежує значення позиції до меж."""
    return max(min(val, MAX_POSITION), -MAX_POSITION)

def move_to_custom():
    """Переміщення до позиції, вказаної вручну."""
    global x, y, z, r
    try:
        coords = entry_coords.get().split()
        if len(coords) != 3:
            label_pose.config(text="Помилка: Введіть 3 значення для X, Y, Z!")
            return
        
        x = limit_position(float(coords[0]))
        y = limit_position(float(coords[1]))
        z = limit_position(float(coords[2]))
        r = limit_position(float(entry_r.get()))
        
        device.move_to(x, y, z, r, wait=True)
        update_pose()
    except ValueError:
        label_pose.config(text="Помилка: Некоректні дані!")

def move_x_plus():
    """Рух робота на 20 мм вперед по осі X."""
    global x
    x = limit_position(x + 20)
    device.move_to(x, y, z, r, wait=True)
    update_pose()

def move_x_minus():
    """Рух робота на 20 мм назад по осі X."""
    global x
    x = limit_position(x - 20)
    device.move_to(x, y, z, r, wait=True)
    update_pose()

def move_y_plus():
    """Рух робота на 20 мм вперед по осі Y."""
    global y
    y = limit_position(y + 20)
    device.move_to(x, y, z, r, wait=True)
    update_pose()

def move_y_minus():
    """Рух робота на 20 мм назад по осі Y."""
    global y
    y = limit_position(y - 20)
    device.move_to(x, y, z, r, wait=True)
    update_pose()

def move_z_plus():
    """Рух робота на 20 мм вгору по осі Z."""
    global z
    z = limit_position(z + 20)
    device.move_to(x, y, z, r, wait=True)
    update_pose()

def move_z_minus():
    """Рух робота на 20 мм вниз по осі Z."""
    global z
    z = limit_position(z - 20)
    device.move_to(x, y, z, r, wait=True)
    update_pose()

def toggle_suction():
    """Включає або вимикає вакуумний насос."""
    if suction_var.get():
        device._set_end_effector_suction_cup(True)
        label_suction.config(text="Сопло: Увімкнено")
    else:
        device._set_end_effector_suction_cup(False)
        label_suction.config(text="Сопло: Вимкнено")

def close_device():
    """Закриває з'єднання з роботом."""
    device.close()
    root.destroy()

# Графічний інтерфейс Tkinter
root = tk.Tk()
root.title("Керування Dobot")

# Мітка для відображення позиції
label_pose = tk.Label(root, text="Позиція: не зчитано")
label_pose.pack()

# Поля для введення координат і кута обертання
frame_custom_move = tk.Frame(root)
frame_custom_move.pack()

tk.Label(frame_custom_move, text="X Y Z:").grid(row=0, column=0)
entry_coords = tk.Entry(frame_custom_move, width=20)
entry_coords.grid(row=0, column=1)

tk.Label(frame_custom_move, text="R:").grid(row=1, column=0)
entry_r = tk.Entry(frame_custom_move, width=10)
entry_r.grid(row=1, column=1)

btn_custom_move = tk.Button(frame_custom_move, text="Перемістити", command=move_to_custom)
btn_custom_move.grid(row=2, column=0, columnspan=2)

# Кнопки для управління рухами
btn_x_plus = tk.Button(root, text="X +20", command=move_x_plus)
btn_x_plus.pack()

btn_x_minus = tk.Button(root, text="X -20", command=move_x_minus)
btn_x_minus.pack()

btn_y_plus = tk.Button(root, text="Y +20", command=move_y_plus)
btn_y_plus.pack()

btn_y_minus = tk.Button(root, text="Y -20", command=move_y_minus)
btn_y_minus.pack()

btn_z_plus = tk.Button(root, text="Z +20", command=move_z_plus)
btn_z_plus.pack()

btn_z_minus = tk.Button(root, text="Z -20", command=move_z_minus)
btn_z_minus.pack()

# Вакуумний насос
suction_var = tk.BooleanVar()
check_suction = tk.Checkbutton(root, text="Включити сопло", variable=suction_var, command=toggle_suction)
check_suction.pack()

label_suction = tk.Label(root, text="Сопло: Вимкнено")
label_suction.pack()

# Кнопка для закриття програми
btn_close = tk.Button(root, text="Вихід", command=close_device)
btn_close.pack()

# Ініціалізація позиції
update_pose()

# Запуск інтерфейсу
root.mainloop()
