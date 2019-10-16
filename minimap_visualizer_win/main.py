import tkinter as tk
from tkinter.constants import *
from tkinter.ttk import Notebook
from controller import ControllerOptionMenu, DataViewer
from visualizer import VisualizerCanvas

class VisualizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        #self.state("zoomed")
        #self.resizable(0,0)
        self.iconbitmap("res/icon.ico")
        self.title("Adoration Visualizer")

    def draw_widgets(self):
        self.render_frame = tk.Frame(self, borderwidth=1, relief=SOLID)
        self.render_frame.pack(expand=YES, fill=BOTH, side=RIGHT)

        self.visualizer = VisualizerCanvas(self.render_frame)
        self.visualizer.pack(anchor=CENTER)

        self.panel_notebook = Notebook(self)

        self.data_viewer = DataViewer(self.panel_notebook)

        self.option_menu = ControllerOptionMenu(self.panel_notebook, self.visualizer, self.data_viewer)
        self.option_menu.draw_widgets()


        self.panel_notebook.add(self.option_menu, text="Control")

        self.panel_notebook.add(self.data_viewer, text="Data")

        self.panel_notebook.pack(side=LEFT, fill=Y)

        self.bind("<Left>", self.onLeft)
        self.bind("<Right>", self.onRight)
        self.bind("<space>", self.onSpace)

    def onLeft(self, event):
        self.option_menu.onPreviousFrame()

    def onRight(self, event):
        self.option_menu.onNextFrame()

    def onSpace(self, event):
        self.option_menu.onTogglePlayback()


if __name__ == '__main__':
    app = VisualizerApp()
    app.draw_widgets()
    app.after(100, app.visualizer.draw_background_image)
    app.mainloop()
