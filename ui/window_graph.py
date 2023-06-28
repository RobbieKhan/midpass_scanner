import customtkinter
from ui.diagram import Diagram
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class UI_WindowGraph(customtkinter.CTkFrame):

    def __init__(self, root, **kw):
        super().__init__(master=root,
                         fg_color='#fcfcfc',
                         corner_radius=10,
                         **kw)
        self.diagram = Diagram()
        canvas = FigureCanvasTkAgg(self.diagram.fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill='both', expand=True)

    def get_diagram_instance(self) -> Diagram:
        return self.diagram
