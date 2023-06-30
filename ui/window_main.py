import customtkinter
from network.scanner import Scanner
from ui.constants import *
from ui.window_leftbar import UI_WindowLeftBar
from ui.window_graph import UI_WindowGraph
from icons.icons import Icons
from typing import Optional
from time import sleep


class UI_WindowMain:

    def __init__(self, root):
        self.root = root
        self.root.protocol('WM_DELETE_WINDOW', self.__ui_quit)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.window_left_bar = UI_WindowLeftBar(self.root, width=GUI_LEFT_BAR_WIDTH, height=GUI_HEIGHT)
        self.window_left_bar.set_cb_button_scan(self.__start_scanning)
        self.window_graph = UI_WindowGraph(self.root, width=GUI_RIGHT_BAR_WIDTH, height=GUI_HEIGHT)

        self.window_left_bar.grid(row=0, column=0, sticky=customtkinter.NSEW)
        self.window_graph.grid(row=0, column=1, sticky=customtkinter.NSEW)

        self.scanner = Scanner()
        self.scanner.set_diagram_instance(self.window_graph.get_diagram_instance())
        self.scanner.set_cb_finished_scan(self.__cb_scan_finished)

        self.spinner_task: Optional = None
        self.spinner_angle = 0

    def ui_start_mainloop(self):
        # self.root.config(menu=self.menu_bar)
        # Start mainloop
        self.root.mainloop()

    def __ui_quit(self):
        # Stop scanner thread
        self.scanner.is_scan_in_progress = False
        # Stop spinner if running
        self.__stop_spinner()
        self.root.quit()

    def __start_scanning(self):
        if not self.scanner.is_scan_in_progress:
            if self.window_left_bar.is_application_number_valid():
                self.goal_days: Optional[int] = self.window_left_bar.get_goal_days()
                self.goal_apps: Optional[int] = self.window_left_bar.get_goal_apps()
                if self.goal_apps is None and self.goal_days is None:
                    print('Goal is not set')
                else:
                    self.scanner.set_consulate_code(self.window_left_bar.get_consulate_code())
                    self.scanner.set_application_date(self.window_left_bar.get_application_date_str())
                    self.scanner.set_application_number(self.window_left_bar.get_short_application_number())
                    self.scanner.set_scanning_depth(applications=self.goal_apps, days=self.goal_days)
                    self.scanner.start_scanning()
                    # Reconfigure scan button - change its text on opposite
                    self.window_left_bar.reconfigure_button_scan()
                    # Clear an old graph
                    self.window_graph.get_diagram_instance().clear()
                    # Start spinner animation
                    self.is_spinner_stopped = False
                    self.__start_spinner()
            else:
                print('Application number is invalid')
        else:
            # We are requested so stop scanning (button was pressed again)
            self.scanner.is_scan_in_progress = False

    def __cb_scan_finished(self):
        self.window_left_bar.reconfigure_button_scan()
        self.__stop_spinner()
        self.window_left_bar.update_status(image=Icons.icon_idle,
                                           status='Сканирование завершено')

    def __start_spinner(self):
        self.window_left_bar.update_status(image=Icons.get_rotated_image(ICON_SCANNING, angle=self.spinner_angle),
                                           status='Идет сканирование...')
        self.spinner_angle -= 360 / 8
        self.spinner_angle %= 360
        if self.scanner.is_scan_in_progress:
            self.spinner_task = self.root.after(100, self.__start_spinner)

    def __stop_spinner(self):
        if self.spinner_task is not None:
            self.root.after_cancel(self.spinner_task)
