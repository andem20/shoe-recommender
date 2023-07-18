import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import os
import pandas as pd

images = []
labels = []
path = ""
index = 0

def open_directory():
    global path, images, labels
    path = filedialog.askdirectory()
    images = os.listdir(path)
    labels = [0 for img in images]
    show_image()

def update_labels():
    index_label.configure(text="Index: " + str(index))
    label_label.configure(text="Label: " + str(labels[index]))

def show_image():
    global image_label, index_label
    current_image = Image.open(path + "/" + images[index])
    photo_image = ImageTk.PhotoImage(current_image)
    image_label.configure(image=photo_image)
    image_label.image = photo_image
    update_labels()

def change_image(event, direction):
    global index
    index += direction
    show_image()

def add_label(event):
    global label_label, index
    labels[index] = int(event.char)
    index += 1
    show_image()
    update_labels()
    export()

def export():
    df = pd.DataFrame(data={"image_url": images, "label": labels})
    df.to_csv("./data-collector/export.csv", index=False)

window = tk.Tk()
window.geometry("800x800")

B = tk.Button(window, text ="Open directory", command = open_directory)
B.pack()

index_label = tk.Label(window, text="")
index_label.pack()

label_label = tk.Label(window, text="")
label_label.pack()

image_label = tk.Label(window, image=None)
image_label.place(x=0, y=40)
image_label.pack()

window.bind("<Right>", lambda e: change_image(e, 1))
window.bind("<Left>", lambda e: change_image(e, -1))
for i in range(10):
    window.bind(str(i), add_label)

B = tk.Button(window, text ="Export", command = export)
B.pack()

window.mainloop()