import customtkinter


class UI_WindowGraph(customtkinter.CTkFrame):

    def __init__(self, root, **kw):
        super().__init__(master=root,
                         fg_color='#fcfcfc',
                         corner_radius=10,
                         **kw)

        self.root = root

    def stop(self):
        pass

