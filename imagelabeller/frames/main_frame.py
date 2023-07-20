import tkinter as tk
import tkinter.filedialog as filedialog
import os
from imagelabeller.DataStore import DataStore
from PIL import ImageTk, Image
import pandas as pd

class MainFrame(tk.Frame):
    def __init__(self, parent: tk.Frame, controller: tk.Tk, store: DataStore = None):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.store = store

        # Labels
        self.index_label = tk.Label(self, text="")
        self.index_label.grid(row = 2, column = 3, padx = 10, pady = 10)

        self.label_label = tk.Label(self, text="")
        self.label_label.grid(row = 2, column = 4, padx = 10, pady = 10)

        self.image_label = tk.Label(self, image=None)
        self.image_label.grid(row = 1, column = 3, padx = 10, pady = 10, columnspan=2)

        # Buttons
        self.open_dir_button = tk.Button(self, text ="Open directory", command = self._open_dir)
        self.open_dir_button.grid(row = 0, column = 3, padx = 10, pady = 10)

        self.export_button = tk.Button(self, text ="Export", command = self._export)
        self.export_button.grid(row = 0, column = 4, padx = 10, pady = 10)

        controller.bind("<Right>", lambda e: self._change_image(e, 1))
        controller.bind("<Left>", lambda e: self._change_image(e, -1))
        for i in range(10):
            controller.bind(str(i), self._add_label)

    def _open_dir(self):
        path = filedialog.askdirectory()
        self.store.path = path
        images = os.listdir(path)
        self.store.images = images
        self.store.labels = [0 for img in images]
        self._show_image()

    def _update_labels(self):
        index = self.store.index
        self.index_label.configure(text="Index: " + str(index))
        self.label_label.configure(text="Label: " + str(self.store.labels[index]))

    def _show_image(self):
        path = self.store.path
        images = self.store.images
        index = self.store.index
        current_image = Image.open(path + "/" + images[index])
        photo_image = ImageTk.PhotoImage(current_image)
        self.image_label.configure(image=photo_image)
        self.image_label.image = photo_image
        self._update_labels()

    def _change_image(self, event, direction):
        index = self.store.index + direction
        self.store.index = min(max(index, 0), len(self.store.images) - 1)
        self._show_image()

    def _add_label(self, event):
        self.store.labels[self.store.index] = int(event.char)
        self.store.index += 1
        self._show_image()
        self._export()

    def _export(self):
        df = pd.DataFrame(data={"image_url": self.store.images, "label": self.store.labels})
        df.to_csv("./data-collector/export.csv", index=False)