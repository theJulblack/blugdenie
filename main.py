import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation

class RandomWalkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Симуляция случайного блуждания")
        
        # Создание элементов управления
        control_frame = ttk.Frame(root)
        control_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)
        
        ttk.Label(control_frame, text="Общее количество шагов:").pack()
        self.steps_var = tk.IntVar(value=100)
        self.steps_entry = ttk.Entry(control_frame, textvariable=self.steps_var)
        self.steps_entry.pack()
        
        ttk.Label(control_frame, text="Максимальная длина шага:").pack()
        self.step_length_var = tk.DoubleVar(value=1.0)
        self.step_length_entry = ttk.Entry(control_frame, textvariable=self.step_length_var)
        self.step_length_entry.pack()
        
        self.vis_type_var = tk.StringVar(value="trajectory")
        ttk.Label(control_frame, text="Тип визуализации:").pack()
        self.vis_menu = ttk.Combobox(control_frame, textvariable=self.vis_type_var, values=["trajectory", "distribution"])
        self.vis_menu.pack()
        
        self.start_button = ttk.Button(control_frame, text="Запустить симуляцию", command=self.start_simulation)
        self.start_button.pack(pady=5)
        
        self.reset_button = ttk.Button(control_frame, text="Сбросить", command=self.reset_simulation)
        self.reset_button.pack()
        
        self.status_label = ttk.Label(control_frame, text="Ожидание запуска...", foreground="blue")
        self.status_label.pack(pady=5)
        
        self.step_status_label = ttk.Label(control_frame, text="Текущий шаг: 0")
        self.step_status_label.pack(pady=5)
        
        # Создание области для графика
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.ani = None
        self.x_data = [0]
        self.y_data = [0]
        self.hist_data = []
        self.current_step = 0
    
    def random_walk(self):
        steps = self.steps_var.get()
        max_length = self.step_length_var.get()
        
        for i in range(steps):
            self.current_step = i + 1
            self.step_status_label.config(text=f"Текущий шаг: {self.current_step}")
            angle = np.random.uniform(0, 2 * np.pi)
            length = np.random.uniform(0, max_length)
            self.x_data.append(self.x_data[-1] + length * np.cos(angle))
            self.y_data.append(self.y_data[-1] + length * np.sin(angle))
            yield
    
    def update_plot(self, _):
        self.ax.clear()
        vis_type = self.vis_type_var.get()
        if vis_type == "trajectory":
            self.ax.plot(self.x_data, self.y_data, marker="$❤$", linestyle='-')
        elif vis_type == "distribution":
            self.hist_data = np.sqrt(np.array(self.x_data)**2 + np.array(self.y_data)**2)
            self.ax.cla()
            self.ax.hist(self.hist_data, bins=20, color='blue', edgecolor='black')
            self.ax.set_xlabel("Расстояние")
            self.ax.set_ylabel("Частота")
        self.ax.set_title("Случайное блуждание")
        self.canvas.draw()
    
    def start_simulation(self):
        self.status_label.config(text="Идет симуляция...", foreground="green")
        self.x_data, self.y_data = [0], [0]
        self.hist_data = []
        self.current_step = 0
        self.step_status_label.config(text="Текущий шаг: 0")
        
        if self.ani:
            self.ani.event_source.stop()
        
        self.ani = animation.FuncAnimation(self.figure, self.update_plot, frames=self.random_walk, repeat=False)
        self.canvas.draw()
    
    def reset_simulation(self):
        if self.ani is not None and self.ani.event_source is not None:
            self.ani.event_source.stop()
        
        self.ani = None  # Сбрасываем переменную анимации
        self.x_data, self.y_data = [0], [0]
        self.hist_data = []
        self.current_step = 0
        self.ax.clear()
        self.ax.set_title("Случайное блуждание")
        self.canvas.draw()
        self.status_label.config(text="Ожидание запуска...", foreground="blue")
        self.step_status_label.config(text="Текущий шаг: 0")
        
if __name__ == "__main__":
    root = tk.Tk()
    app = RandomWalkApp(root)
    root.mainloop()
