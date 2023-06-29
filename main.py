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
    root.minsize(GUI_WIDTH, GUI_HEIGHT)
    # root.wm_iconbitmap(ICON_WINDOW_ICON)

    ui_main_window = UI_WindowMain(root)
    ui_main_window.ui_start_mainloop()
