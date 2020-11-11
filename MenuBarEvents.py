from typing import Union, List
from pathlib import Path

import pygame

from pygame_gui.windows import UIFileDialog, UIMessageWindow
from pygame_gui import UI_BUTTON_START_PRESS, UI_WINDOW_MOVED_TO_FRONT, UI_WINDOW_CLOSE
from pygame_gui import UI_FILE_DIALOG_PATH_PICKED

from lib import CanvasWindow


class MenuBarEvents:
    def __init__(self, windowSurface, manager):
        pass

    def process_events(self, event):
        pass

    def _try_undo(self):
        pass

    def _try_redo(self):
        pass