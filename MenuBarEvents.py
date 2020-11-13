from typing import Union, List
from pathlib import Path

import pygame
from pygame_gui.elements.ui_selection_list import UISelectionList

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
        # ↓↓↓ Canvas Stuff ↓↓↓
        if (event.type == pygame.USEREVENT
                and event.user_type == UI_WINDOW_MOVED_TO_FRONT
                and event.ui_object_id == '#canvas_window'):
            self.activeCanvas = event.ui_element
        if (event.type == pygame.USEREVENT
                and event.user_type == UI_WINDOW_CLOSE
                and event.ui_object_id == '#canvas_window'):
            self.activeCanvas = None
        # ↓↓↓ File Menu ↓↓↓
        if (event.type == pygame.USEREVENT
                and event.user_type == UI_BUTTON_START_PRESS
                and event.ui_object_id == 'menu_bar.#file_menu_items.#new'):
            newCanvasDialog = pygame.Rect((0, 0), (400, 300))
            newCanvasDialog.center = self.windowSurface.get_rect().center
            NewCanvasDialog(newCanvasDialog, self.ui_manager)
        if (event.type == pygame.USEREVENT
                and event.user_type == UI_BUTTON_START_PRESS
                and event.ui_object_id == 'menu_bar.#file_menu_items.#open'):
            fileDialogRect = pygame.Rect((0, 0), (400, 350))
            fileDialogRect.center = self.windowSurface.get_rect().center
            UIFileDialog(fileDialogRect,
                         self.ui_manager,
                         "Open...",
                         self.lastUsedFilePath,
                         '#open_file_dialog',
                         allow_existing_files_only=True)
        if (event.type == pygame.USEREVENT
                and event.user_type == UI_BUTTON_START_PRESS
                and event.ui_object_id == 'menu_bar.#file_menu_items.#save'
                and self.activeCanvas is not None
                and self.activeCanvas.canvasUI.savePath is not None):
            try:
                print(
                    f"Saving to... {str(self.activeCanvas.canvasUI.savePath)}")
                pygame.image.save(self.activeCanvas.canvasUI.get_image(),
                                  self.activeCanvas.canvasUI.savePath)
            except pygame.error:
                msgRect = pygame.Rect((0, 0), (250, 160))
                msgRect.center = self.windowSurface.get_rect().center
                msgWindow = UIMessageWindow(msgRect,
                                            html_message='Unable to save...',
                                            manager=self.ui_manager,
                                            window_title='Error')
                msgWindow.set_blocking(True)  # blocks clicking anything else
        if (event.type == pygame.USEREVENT
                and event.user_type == UI_BUTTON_START_PRESS
                and event.ui_object_id == 'menu_bar.#file_menu_items.#save_as'
                and self.activeCanvas is not None):
            fileDialogRect = pygame.Rect((0, 0), (400, 350))
            fileDialogRect.center = self.windowSurface.get_rect().center
            if self.activeCanvas.canvasUI.savePath is not None:
                filePath = self.activeCanvas.canvasUI.savePath
            else:
                filePath = (Path(self.lastUsedFilePath) /
                            self.activeCanvas.window_display_title)
            saveDialog = UIFileDialog(fileDialogRect,
                                      self.ui_manager,
                                      'Save As...',
                                      str(filePath),
                                      object_id='#save_file_dialog')
            saveDialog.set_blocking(True)
        # ↓↓↓ Edit Menu ↓↓↓
        if (event.type == pygame.USEREVENT
                and event.user_type == UI_BUTTON_START_PRESS
                and event.ui_object_id == 'menu_bar.#edit_menu_items.#undo'
                and self.activeCanvas is not None):
            self._try_undo()
        if (event.type == pygame.USEREVENT
                and event.user_type == UI_BUTTON_START_PRESS
                and event.ui_object_id == 'menu_bar.#edit_menu_items.#redo'
                and self.activeCanvas is not None):
            self._try_redo()
        # ↓↓↓ View Menu ↓↓↓
        if (event.type == pygame.USEREVENT
                and event.user_type == UI_BUTTON_START_PRESS and
                event.ui_object_id == 'menu_bar.#view_menu_items.#workspace'):
            pass
        if (event.type == pygame.USEREVENT
                and event.user_type == UI_BUTTON_START_PRESS
                and event.ui_object_id == 'menu_bar.#view_menu_items.#info'):
            pass
        ## ↓↓↓ Themes ↓↓↓
        if (event.type == pygame.USEREVENT
                and event.user_type == UI_BUTTON_START_PRESS
                and (event.ui_object_id == '#theme_items.#themes_default'
                     or event.ui_object_id == '#theme_items.#themes_light'
                     or event.ui_object_id == '#theme_items.#themes_dark')):
            if event.ui_object_id == '#theme_items.#themes_dark':
                themePath = "res\\dark_theme.json"
            elif event.ui_object_id == '#theme_items.#themes_light':
                themePath = "res\\light_theme.json"
            else:
                themePath = "res\\default_theme.json"
            pygame.event.post(
                pygame.event.Event(
                    pygame.USEREVENT, {
                        'user_type': 'theme_changed',
                        'ui_element': event.ui_element,
                        'ui_object_id': event.ui_object_id,
                        'theme_path': themePath
                    }))
        # ↓↓↓ Help Menu ↓↓↓
        if (event.type == pygame.USEREVENT
                and event.user_type == UI_BUTTON_START_PRESS
                and event.ui_object_id == 'menu_bar.#help_menu_itemse.#about'):
            pass

    def _try_undo(self):
        pass

    def _try_redo(self):
        pass