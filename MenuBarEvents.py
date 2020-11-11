from lib.ui.DialogWindow import NewCanvasDialog
from typing import Union, List
from pathlib import Path

import pygame

from pygame_gui.windows import UIFileDialog, UIMessageWindow
from pygame_gui import UI_BUTTON_START_PRESS, UI_WINDOW_MOVED_TO_FRONT, UI_WINDOW_CLOSE
from pygame_gui import UI_FILE_DIALOG_PATH_PICKED

from lib import CanvasWindow
from lib import NewCanvasDialog


class MenuBarEvents:
    def __init__(self, windowSurface, ui_manager):
        self.windowSurface = windowSurface
        self.ui_manager = ui_manager

        self.lastUsedFilePath = str(Path('.').absolute())

        self.activeCanvas = None  # type: Union[CanvasWindow, None]

    def process_events(self, event):
        if (event.type == pygame.USEREVENT
                and event.user_type == UI_BUTTON_START_PRESS
                and event.ui_object_id == 'menu_bar.#file_menu.#new'):
            newCanvasDialog = pygame.Rect((0, 0), (400, 300))
            newCanvasDialog.center = self.windowSurface.get_rect().center
            NewCanvasDialog(newCanvasDialog, self.ui_manager)
        if (event.type == pygame.USEREVENT
                and event.user_type == UI_BUTTON_START_PRESS
                and event.ui_object_id == 'menu_bar.#file_menu.#open'):
            fileDialogRect = pygame.Rect((0, 0), (400, 350))
            fileDialogRect.center = self.windowSurface.get_rect().center
            UIFileDialog(fileDialogRect,
                         self.ui_manager,
                         "Open...",
                         self.lastUsedFilePath,
                         '#open_file_dialog',
                         allow_existing_files_only=True)

    def _try_undo(self):
        pass

    def _try_redo(self):
        pass