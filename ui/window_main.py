import customtkinter
from network.scanner import Scanner
from ui.constants import *
from ui.window_leftbar import UI_WindowLeftBar
from ui.window_graph import UI_WindowGraph


class UI_WindowMain:

    def __init__(self, root):
        self.root = root
        self.root.protocol('WM_DELETE_WINDOW', self.__ui_quit)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.scanner = Scanner()

        self.window_left_bar = UI_WindowLeftBar(self.root, width=GUI_LEFT_BAR_WIDTH, height=GUI_HEIGHT)
        self.window_left_bar.set_cb_button_scan(self.__start_scanning)
        self.window_graph = UI_WindowGraph(self.root, width=GUI_RIGHT_BAR_WIDTH, height=GUI_HEIGHT)

        self.window_left_bar.grid(row=0, column=0, sticky=customtkinter.NSEW)
        self.window_graph.grid(row=0, column=1, sticky=customtkinter.NSEW)

    def ui_start_mainloop(self):
        # self.root.config(menu=self.menu_bar)
        # Start mainloop
        self.root.mainloop()

    def __ui_quit(self):
        self.root.quit()

    def __start_scanning(self):
        if self.window_left_bar.is_application_number_valid():
            self.scanner.set_consulate_code(self.window_left_bar.get_consulate_code())
            self.scanner.set_application_date(self.window_left_bar.get_application_date_str())
            self.scanner.set_application_number(self.window_left_bar.get_short_application_number())
            self.scanner.set_scanning_depth(applications=571, days=73)
            self.scanner.start_scanning()
        print('Application number is invalid')
