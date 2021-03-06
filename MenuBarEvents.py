from typing import Union, List
from pathlib import Path

import pygame

from pygame_gui.windows import UIFileDialog, UIMessageWindow
from pygame_gui import UI_BUTTON_START_PRESS, UI_WINDOW_MOVED_TO_FRONT, UI_WINDOW_CLOSE
from pygame_gui import UI_FILE_DIALOG_PATH_PICKED

from lib import CanvasWindow, NewCanvasDialog, UndoRecord


class MenuBarEvents:
    """
    This Class is to create an object that handles events for the menu bar.
    So an object of this is a menu bar event handler
    
    :param windowSurface: the display of the app
    :param ui_manager: The manager for the UI
    """
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
        if (event.type == pygame.USEREVENT
                and event.user_type == UI_FILE_DIALOG_PATH_PICKED
                and event.ui_object_id == '#save_file_dialog'):
            path = Path(event.text)
            self.lastUsedFilePath = path.parent
            try:
                pygame.image.save(self.activeCanvas.canvasUI.get_image(),
                                  str(path))
                self.activeCanvas.set_display_title(path.name)
                self.activeCanvas.canvasUI.savePath = path
                print(
                    f"Saving to... {str(self.activeCanvas.canvasUI.savePath)}")
            except pygame.error:
                msgRect = pygame.Rect((0, 0), (250, 160))
                msgRect.center = self.windowSurface.get_rect().center
                msgWindow = UIMessageWindow(
                    msgRect,
                    html_message='Unable to save image to selected path...<br>'
                    'This may be because of the image format<br>'
                    'Which must be <i>.bmp, .png, .jpg or .tga</i><br>',
                    manager=self.ui_manager,
                    window_title='Error')
                msgWindow.set_blocking(True)
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
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_z
                and event.mod & pygame.KMOD_CTRL):
            if event.mod & pygame.KMOD_SHIFT:
                self._try_redo()
            else:
                self._try_undo()
        # ↓↓↓ View Menu ↓↓↓
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
        if (event.type == pygame.USEREVENT
                and event.user_type == UI_BUTTON_START_PRESS
                and event.ui_object_id == 'menu_bar.#view_menu_items.#info'
                and self.activeCanvas is not None):
            msgRect = pygame.Rect((0, 0), (256 + 64, 128 + 64 + 16))
            msgRect.center = self.windowSurface.get_rect().center

            fileName = self.activeCanvas.window_display_title
            canvasSize = (str(self.activeCanvas.canvasUI.rect.width) + 'x' +
                          str(self.activeCanvas.canvasUI.rect.height) +
                          ' pixels.')
            msgWindow = UIMessageWindow(
                msgRect,
                html_message='<br><b>           Image Info</b><br>'
                '----------------------------------<br><br>'
                '<b>File Name: </b>' + fileName + '<br>'
                '<b>Size in Pixels: </b>' + canvasSize + '<br>',
                manager=self.ui_manager,
                window_title='Info')
            msgWindow.set_blocking(True)
        # ↓↓↓ Help Menu ↓↓↓
        if (event.type == pygame.USEREVENT
                and event.user_type == UI_BUTTON_START_PRESS
                and event.ui_object_id == 'menu_bar.#help_menu_items.#about'):
            msgRect = pygame.Rect((0, 0), (256, 194))
            msgRect.center = self.windowSurface.get_rect().center
            msgWindow = UIMessageWindow(
                msgRect,
                html_message='<br><b>     Pygame Paint</b><br>'
                '-----------------------<br><br>'
                '<b>Version: </b>1.0<br>'
                '<b>Created by: </b>Yüşa Erenci<br>',
                manager=self.ui_manager,
                window_title='About')
            msgWindow.set_blocking(True)

    def _try_undo(self):
        if (self.activeCanvas is not None
                and self.activeCanvas.canvasUI.undoStack):
            undoRecord = self.activeCanvas.canvasUI.undoStack.pop()

            redoSurf = pygame.Surface(undoRecord.rect.size,
                                      flags=pygame.SRCALPHA)
            redoSurf.blit(self.activeCanvas.canvasUI.get_image(), (0, 0),
                          undoRecord.rect)
            redoRecord = UndoRecord(redoSurf, undoRecord.rect.copy())
            self.activeCanvas.canvasUI.redoStack.append(redoRecord)
            self.activeCanvas.canvasUI.get_image().blit(
                undoRecord.image, undoRecord.rect)

    def _try_redo(self):
        if (self.activeCanvas is not None
                and self.activeCanvas.canvasUI.redoStack):
            redoRecord = self.activeCanvas.canvasUI.redoStack.pop()
            undoSurf = pygame.Surface(redoRecord.rect.size,
                                      flags=pygame.SRCALPHA)
            undoSurf.blit(self.activeCanvas.canvasUI.get_image(), (0, 0),
                          redoRecord.rect)
            undoRecord = UndoRecord(undoSurf, redoRecord.rect.copy())
            self.activeCanvas.canvasUI.undoStack.append(undoRecord)

            self.activeCanvas.canvasUI.get_image().blit(
                redoRecord.image, redoRecord.rect)
