from ui.constants import *
from PIL import Image
import customtkinter
import os

ICONS_TOOLBAR_WIDTH = 35
ICONS_TOOLBAR_HEIGHT = 35

ICONS_STATUS_WIDTH = 25
ICONS_STATUS_HEIGHT = 25


class Icons:
    icon_scanning = customtkinter.CTkImage(light_image=Image.open(os.path.join(ICON_SCANNING)),
                                           size=(28, 28))
    icon_idle = customtkinter.CTkImage(light_image=Image.open(os.path.join(ICON_IDLE)),
                                       size=(28, 28))

    @staticmethod
    def get_rotated_image(image_path: str, angle: int):
        return customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path)).rotate(angle=angle),
                                      size=(28, 28))
