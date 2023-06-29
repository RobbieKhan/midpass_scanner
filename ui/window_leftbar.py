from ui.constants import GUI_LEFT_BAR_WIDTH, GUI_HEIGHT
from typing import Callable, Optional
import customtkinter

BUTTON_LABEL_START_SCAN = 'Начать сканирование'
BUTTON_LABEL_STOP_SCAN = 'Остановить сканирование'


class UI_WindowLeftBar(customtkinter.CTkFrame):

    def __init__(self, root, **kw):
        super().__init__(master=root,
                         fg_color='#fcfcfc',
                         corner_radius=10,
                         **kw)
        self.label_app_num = customtkinter.CTkLabel(master=self,
                                                    text='Номер заявления',
                                                    font=(None, 18, 'bold'),
                                                    fg_color='transparent')
        self.entry_app_num = customtkinter.CTkEntry(master=self,
                                                    width=GUI_LEFT_BAR_WIDTH,
                                                    placeholder_text='Введите 25-значный номер',
                                                    justify=customtkinter.CENTER)
        self.radio_var_scan_goal = customtkinter.StringVar(value='days')
        self.radiobutton_goal_days = customtkinter.CTkRadioButton(master=self,
                                                                  text='число дней',
                                                                  command=lambda: print('Days are chosen'),
                                                                  variable=self.radio_var_scan_goal, value='days')
        self.label_scan_goal = customtkinter.CTkLabel(master=self,
                                                      text='Условие завершения\nсканирования',
                                                      font=(None, 18, 'bold'),
                                                      fg_color='transparent')
        self.radiobutton_goal_apps = customtkinter.CTkRadioButton(master=self,
                                                                  text='число анкет',
                                                                  command=lambda: print('Apps are chosen'),
                                                                  variable=self.radio_var_scan_goal, value='apps')
        self.entry_scan_days = customtkinter.CTkEntry(master=self,
                                                      width=75,
                                                      placeholder_text='xxx',
                                                      justify=customtkinter.CENTER)
        self.entry_scan_apps = customtkinter.CTkEntry(master=self,
                                                      width=75,
                                                      placeholder_text='xxx',
                                                      justify=customtkinter.CENTER)
        self.button_scan = customtkinter.CTkButton(master=self,
                                                   text=BUTTON_LABEL_START_SCAN,
                                                   command=self.__event_scan)

        self.label_app_num.grid(row=0, column=0, columnspan=2, pady=(15, 0))
        self.entry_app_num.grid(row=1, column=0, columnspan=2, padx=10, pady=(10, 0))
        self.label_scan_goal.grid(row=2, column=0, columnspan=2, pady=(25, 0))
        self.radiobutton_goal_days.grid(row=3, column=0, padx=10, pady=(10, 0), sticky=customtkinter.W)
        self.entry_scan_days.grid(row=3, column=1, padx=10, pady=(10, 0), sticky=customtkinter.EW)
        self.radiobutton_goal_apps.grid(row=4, column=0, padx=10, pady=(10, 0), sticky=customtkinter.W)
        self.entry_scan_apps.grid(row=4, column=1, padx=10, pady=(10, 0), sticky=customtkinter.EW)
        self.button_scan.grid(row=5, column=0, columnspan=2, padx=10, pady=(25, 0), sticky=customtkinter.EW)

        self.button_scan_cb: Optional[Callable] = None

    def set_cb_button_scan(self, cb: Callable):
        self.button_scan_cb = cb

    def is_application_number_valid(self) -> bool:
        application_number: str = self.entry_app_num.get()
        return 25 == len(application_number) and application_number.isnumeric() and \
               application_number[0:4] == '2000'

    def get_consulate_code(self) -> Optional[int]:
        if self.is_application_number_valid():
            application_number: str = self.entry_app_num.get()
            return int(application_number[4:9])
        return None

    def get_short_application_number(self) -> Optional[int]:
        if self.is_application_number_valid():
            application_number: str = self.entry_app_num.get()
            return int(application_number[-8:])
        return None

    def get_application_date_str(self) -> Optional[str]:
        if self.is_application_number_valid():
            application_number: str = self.entry_app_num.get()
            return application_number[9:17]
        return None

    def get_goal_days(self) -> Optional[int]:
        days: str = self.entry_scan_days.get()
        if self.radio_var_scan_goal.get() != 'days' or not days:
            return None
        return int(days)

    def get_goal_apps(self) -> Optional[int]:
        apps: str = self.entry_scan_apps.get()
        if self.radio_var_scan_goal.get() != 'apps' or not apps:
            return None
        return int(apps)

    def reconfigure_button_scan(self):
        if self.button_scan.cget('text') == BUTTON_LABEL_START_SCAN:
            self.button_scan.configure(text=BUTTON_LABEL_STOP_SCAN)
        else:
            self.button_scan.configure(text=BUTTON_LABEL_START_SCAN)

    def __event_scan(self):
        if self.button_scan_cb is not None:
            self.button_scan_cb()
