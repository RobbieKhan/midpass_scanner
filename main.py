from network.scanner import Scanner
from ui.window_main import UI_WindowMain
from ui.constants import GUI_WIDTH, GUI_HEIGHT, GUI_TITLE, GUI_VERSION
from tendo import singleton
import customtkinter
import os
import sys

if 'nt'.__eq__(os.name):
    theme = 'vista'
else:
    theme = 'radiance'

if __name__.__eq__('__main__'):
    customtkinter.set_appearance_mode('Light')
    customtkinter.set_default_color_theme('styles/custom_theme.json')
    customtkinter.set_widget_scaling(1.0)
    customtkinter.set_window_scaling(1.0)
    try:
        si = singleton.SingleInstance()
    except singleton.SingleInstanceException:
        # mb.showerror(title='Error', message='Another application is already running!')
        sys.exit()
    root = customtkinter.CTk()
    root.tk.call('tk', 'scaling', 1.33)
    root.geometry(f'{GUI_WIDTH}x{GUI_HEIGHT}')
    root.title(f'{GUI_TITLE} {GUI_VERSION}')
    root.resizable(True, True)
    # root.wm_iconbitmap(ICON_WINDOW_ICON)

    '''scan = Scanner()
    scan.set_consulate_code(93104)
    scan.set_application_number(11571)
    scan.set_application_date('20230313')
    scan.set_scanning_depth(applications=571, days=73)
    scan.start_scanning()'''

    ui_main_window = UI_WindowMain(root)
    ui_main_window.ui_start_mainloop()
