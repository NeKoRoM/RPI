import tkinter as tk
import random
import asyncio


# 2 cm miara
LINE_WIDTH = 1440
LINE_HEIGHT = 100
BOX_SIZE = 15
SPEED = 5
INTERVAL = 250  # jak często jest aktualizowana symulacja

MACHINE_POSITION_REVERSED = [215, 210, 160, 165, 225, 160, 160]
MACHINE_POSITION = [160, 160, 255, 165, 160, 210, 210]

WAIT_BOX = [ 0,0,0,0,0,0,0,0]

class ProductionLineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Symulacja")

        # pole do rysowania
        self.canvas = tk.Canvas(root, width=LINE_WIDTH, height=LINE_HEIGHT, bg="white")
        self.canvas.pack()

        # lista box i text do manipulacji
        self.boxes = []
        self.texts = []
#
        self.create_buttons()

#
        self.update_line()
        

    def create_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack()

        for i in range(8):
            button = tk.Button(button_frame, text=f"dodać pudełko {i+1}", command=lambda i=i: self.add_box(i, 0))
            button.grid(row=0, column=i)
        button = tk.Button(button_frame, text=f"random", command=lambda: self.random_box())
        button.grid(row=0, column=8)

    def add_box(self, position, count):
#
        y_position = 1 * (LINE_HEIGHT // 8)  
        x_position = sum(MACHINE_POSITION[:position+1])
        
        y = x_position - 1
        y1= x_position  + BOX_SIZE + 1
        # Check if there's already a box at this position
        box_exists = any(self.canvas.coords(b) for b in self.boxes if ( (self.canvas.coords(b)[0]+BOX_SIZE <y1 and self.canvas.coords(b)[0]+BOX_SIZE >y) or(self.canvas.coords(b)[0]<y1 and self.canvas.coords(b)[0]>y))  )
        numOfBox =   WAIT_BOX[position] 

        if not box_exists:
            box = self.canvas.create_rectangle(x_position, y_position, x_position + BOX_SIZE, y_position + BOX_SIZE, outline='blue', width=4)
            text = self.canvas.create_text(x_position + BOX_SIZE / 2, y_position + BOX_SIZE / 2, fill="darkblue", font="Times 20 italic bold", text=position)
            
            self.boxes.append(box)
            self.texts.append(text)
            print(f"{WAIT_BOX}")
            if WAIT_BOX[position]<=1:
                del WAIT_BOX[position]
                WAIT_BOX.insert(position, 0 )
            else:
                del WAIT_BOX[position]
                WAIT_BOX.insert(position,numOfBox-1)
        else:
            print(f"{WAIT_BOX}")
            next_position = position
            if count== 0 :
                self.root.after(INTERVAL, self.add_box, next_position, 1)
                del WAIT_BOX[position]
                WAIT_BOX.insert(position,numOfBox+1)

            else:
                self.root.after(INTERVAL, self.add_box, next_position, 1)



    def update_line(self):
        # Обновляем положение каждой коробки
        for box in self.boxes:
            self.canvas.move(box, -SPEED, 0)
            x1, y1, x2, y2 = self.canvas.coords(box)
            
            # Удаляем коробку, если она вышла за пределы линии
            if x2 < 0:
                self.canvas.delete(box)
                self.boxes.remove(box)

        for text in self.texts:
            self.canvas.move(text, -SPEED, 0)
            x1, y1 = self.canvas.coords(text)
            
            # Удаляем текст, если он вышел за пределы линии
            if x1 < 0:
                self.canvas.delete(text)
                self.texts.remove(text)

        # Запускаем снова обновление линии через указанный интервал времени
        self.root.after(INTERVAL, self.update_line)
        
        
    def random_box(self):
           self.add_box(random.randint(0,7), 0)
           self.root.after(5000, self.random_box)


# Основная функция для запуска приложения
def main():
    root = tk.Tk()
    app = ProductionLineApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
