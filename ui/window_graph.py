from tkinter import *
from tkinter import ttk


class UI_WindowGraph(ttk.Frame):

    def __init__(self, root, **kw):
        super().__init__(**kw)

        self.root = root

    def stop(self):
        pass

