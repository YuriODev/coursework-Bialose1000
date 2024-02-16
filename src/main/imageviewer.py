import os
import tkinter as tk
from PIL import Image, ImageTk

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

