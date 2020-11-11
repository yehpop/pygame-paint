from typing import Union, List
from pathlib import Path

import pygame
import pygame_gui

from pygame_gui.core import UIElement
from lib.tools import UndoRecord


class EditableCanvas(UIElement):
    # again lots of paramters
    def __init__(self,
                 rect,
                 imageSurface,
                 manager,
                 container=None,
                 parent=None,
                 object_id=None,
                 anchors=None):
        super().__init__(rect, manager, container, 1, 1, anchors=anchors)

        self._create_valid_ids(container, parent, object_id, 'editable_canvas')

        self.set_image(imageSurface)

        self.activeTool = None
        self.savePath = None  # type: Union[Path, None]

        self.undoStack = []  # type: List[Union[UndoRecord, None]]
        self.redoStack = []  # type: List[Union[UndoRecord, None]]

    def save_file_path(self, path):
        self.savePath = path

    def set_active_tool(self, tool):
        self.activeTool = tool

    def process_events(self, event: pygame.event.Event) -> bool:
        eventConsumed = False
        if (event.type == pygame.USEREVENT
                and event.user_type == 'paint_tool_changed'):
            self.set_active_tool(event.tool)

        if (self.activeTool is not None and self.activeTool.process_canvas(
                event, self, self.ui_manager.get_mouse_position)):
            self.activeTool.activeCanvas = self
            eventConsumed = True

        return eventConsumed

    def update(self, timeDelta: float):
        super().update(timeDelta)

    def get_image(self) -> pygame.Surface:
        if self.get_image_clipping_rect is not None:
            return self._pre_clipped_image
        else:
            return self.image