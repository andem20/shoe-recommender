import tkinter as tk
from imagelabeller.frames.main_frame import MainFrame
from imagelabeller.DataStore import DataStore

class ImageLabellerApp(tk.Tk):
    def __init__(self, title: str, window_size: tuple[int, int]):
        super().__init__()

        self.title(title)
        self.geometry(f"{window_size[0]}x{window_size[1]}")
        self.container = tk.Frame(self) 
        self.container.pack(side = "top", fill = "both", expand = True)
  
        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)

        self.store = DataStore()

        self.frames = {}

        frame = MainFrame(self.container, self, self.store)
        frame.grid(row = 0, column = 0, columnspan=4, rowspan=4)
        self.frames[frame.__class__] = frame

        self.show_frame(MainFrame)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def run(self):
        self.mainloop()