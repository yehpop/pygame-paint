import pygame
import pygame_gui as gui

from pygame_gui.elements import UIHorizontalSlider, UIButton, UILabel


class CanvasWindow(gui.elements.UIWindow):
    def __init__(self, rect, manager, imageName, image):
        super().__init__(rect,
                         manager,
                         imageName,
                         object_id='#canvas_window',
                         resizable=True)
