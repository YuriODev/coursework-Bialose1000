import tkinter as tk
from dijkstra import completion_check
from maze import Maze
from rat import Rat
from tkinter import simpledialog, messagebox
from matplotlib.widgets import Button
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image, ImageTk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Menu")
        self.master.configure(bg='red')
        self.pack(fill=tk.BOTH, expand=1)  # fill the entire window
        self.create_widgets()

    def create_widgets(self):
        self.dijkstra = tk.Button(self, height=2, width=20, font=('Helvetica', '20'))  # larger button and text
        self.dijkstra["text"] = "Dijkstra’s Algorithm"
        self.dijkstra["command"] = self.run_dijkstra
        self.dijkstra["bg"] = 'blue'
        self.dijkstra["fg"] = 'white'
        self.dijkstra.pack(side="top")

        self.ml = tk.Button(self, height=2, width=20, font=('Helvetica', '20'))  # larger button and text
        self.ml["text"] = "Machine Learning"
        self.ml["command"] = self.run_ml
        self.ml["bg"] = 'blue'
        self.ml["fg"] = 'white'
        self.ml.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def run_dijkstra(self):
        print("You chose Dijkstra’s.")
        create_buttons(self.master)
        

    def run_ml(self):
        print("You chose Machine Learning.")
        create_buttonsm(self.master)
        

class InteractiveMaze:
    def __init__(self, maze, start=(0, 0), end=None):
        self.maze = maze
        self.start = start
        self.end = maze.shape[0] - 1, maze.shape[1] - 1 if end is None else end
        self.fig, self.ax = plt.subplots()
        self.img = self.ax.imshow(self.maze, cmap='viridis_r', origin='upper', vmin=0, vmax=1)
        self.ax.axis('off')
        plt.subplots_adjust(bottom=0.2)

        # Plot start and end points with unique colors
        self.plot_start_end_points()

        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.maze = maze.copy()
        self.maze_history = [self.maze.copy()]
        self.history_index = 0

        # Add buttons for undo, redo, and clear
        self.add_buttons()

    def plot_start_end_points(self):
        # Clear any existing start/end markers before plotting new ones
        self.ax.plot(self.start[1], self.start[0], 'go')  # Start point in green
        self.ax.plot(self.end[1], self.end[0], 'ro')  # End point in red

    def add_buttons(self):
        undo_button_ax = plt.axes([0.7, 0.05, 0.1, 0.075])
        self.undo_button = Button(undo_button_ax, 'Undo')
        self.undo_button.on_clicked(self.undo)

        redo_button_ax = plt.axes([0.81, 0.05, 0.1, 0.075])
        self.redo_button = Button(redo_button_ax, 'Redo')
        self.redo_button.on_clicked(self.redo)

        clear_button_ax = plt.axes([0.59, 0.05, 0.1, 0.075])
        self.clear_button = Button(clear_button_ax, 'Clear')
        self.clear_button.on_clicked(self.clear)

    def on_click(self, event):
        x, y = int(round(event.xdata)), int(round(event.ydata))
        size = self.maze.shape[0] - 1
        x, y = max(0, min(size, x)), max(0, min(size, y))
        if (x, y) not in [self.start, self.end]:
            self.toggle_cell_state(x, y)
            self.update_maze_display()

    def toggle_cell_state(self, x, y):
        self.maze[y, x] = 0 if self.maze[y, x] == 1 else 1

    def update_maze_display(self):
        self.img.set_data(self.maze)
        self.plot_start_end_points()  # Re-plot start and end points to keep them on top
        self.fig.canvas.draw()

    # Modify show, undo, redo, and clear methods to call update_maze_display()
    # to ensure start and end points are correctly colored after any update.

    def show(self):
        plt.show()

    def undo(self, event=None):
        if self.history_index > 0:
            self.history_index -= 1
            self.maze = self.maze_history[self.history_index].copy()
            self.update_maze_display()

    def redo(self, event=None):
        if self.history_index < len(self.maze_history) - 1:
            self.history_index += 1
            self.maze = self.maze_history[self.history_index].copy()
            self.update_maze_display()

    def clear(self, event=None):
        self.maze = np.ones_like(self.maze)  # Reset the maze to the initial state
        # Ensure start and end points are marked as open paths
        self.maze[self.start[0], self.start[1]] = 1
        self.maze[self.end[0], self.end[1]] = 1
        self.maze_history = [self.maze.copy()]  # Reset the history
        self.history_index = 0
        self.update_maze_display()


def select_sizeDIJ(size, root):
    maze = np.ones((size, size))
    imaze = InteractiveMaze(maze)
    imaze.show()
    updated_maze = imaze.maze
    rat = Rat((0,0), size)
    maze = Maze(updated_maze, rat)
    root.destroy()
    completion_check(maze)

def select_sizeML(size, root):
    from ML import MachineLearning
    root.destroy()
    MachineLearning(size)

def create_buttons(root):
    for i in range(4, 11):
        btn = tk.Button(root, text=f"{i}x{i}", command=lambda size=i: select_sizeDIJ(size, root), bg='blue', fg='white', font='Helvetica 14 bold')
        btn.pack(pady=10)
    
def create_buttonsm(root):
    for i in range(4, 11):
        btn = tk.Button(root, text=f"{i}x{i}", command=lambda size=i: select_sizeML(size, root), bg='blue', fg='white', font='Helvetica 14 bold')
        btn.pack(pady=10)

def create_image_viewer(directory):
    # Create the main window
    root = tk.Tk()
    root.title("Image Viewer")

    # Get a list of all the image files in the directory
    image_files = [f for f in os.listdir(directory) if f.endswith(('.png', '.jpg', '.jpeg'))]

    # Create a StringVar to hold the name of the current image file
    current_image = tk.StringVar()
    if image_files:
        current_image.set(image_files[0])

    # Create a Label to display the image
    image_label = tk.Label(root)
    image_label.pack()

    # Function to update the image displayed by the label
    def update_image():
        image_file = current_image.get()
        image_path = os.path.join(directory, image_file)
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo  # Keep a reference to the image to prevent it from being garbage collected

    # Create a Listbox to list all the image files
    listbox = tk.Listbox(root, listvariable=tk.Variable(value=image_files))
    listbox.pack()

    # Function to update current_image when a new item is selected in the listbox
    def on_select(event):
        current_image.set(listbox.get(listbox.curselection()))
        update_image()

    # Bind the <<ListboxSelect>> event to the on_select function
    listbox.bind('<<ListboxSelect>>', on_select)

    # Display the first image
    update_image()

    # Start the main loop
    root.mainloop()