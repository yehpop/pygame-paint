import pygame
import pygame_gui as gui

from pygame_gui.elements import UIScrollingContainer
from lib.ui.EditableCanvas import EditableCanvas


class CanvasWindow(gui.elements.UIWindow):
    def __init__(self, rect, manager, imageName, image):
        super().__init__(rect,
                         manager,
                         imageName,
                         object_id='#canvas_window',
                         resizable=True)
        contRect = pygame.Rect((0, 0), (self.get_container().get_size()))
        self.scrollableContainer = UIScrollingContainer(contRect,
                                                        self.ui_manager,
                                                        container=self,
                                                        anchors={
                                                            'left': 'left',
                                                            'right': 'right',
                                                            'top': 'top',
                                                            'bottom': 'bottom'
                                                        })
        self.scrollableContainer.set_scrollable_area_dimensions(
            (image.get_width() + 25, image.get_height() + 25))
        self.canvas_ui = EditableCanvas()
