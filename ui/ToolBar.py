import pygame
import pygame_gui as gui

from pygame_gui.elements import UIHorizontalSlider, UIButton, UILabel

from tools.Brush import ToolBrush
from tools.Bucket import ToolBucket


class ToolBar(gui.elements.UIWindow):
    def __init__(self, rect, manager):
        super().__init__(rect,
                         manager,
                         "Tools",
                         object_id='#tool_bar',
                         resizable=True)
        # Tool Select Buttons
        brushButtonRect = pygame.Rect((15, 132), (64, 64))
        self.brushButton = gui.elements.UIButton(brushButtonRect,
                                                 "",
                                                 manager,
                                                 self,
                                                 object_id='#brush_button')
        bucketButtonRect = pygame.Rect((89, 132), (64, 64))
        self.bucketButton = gui.elements.UIButton(bucketButtonRect,
                                                  "",
                                                  manager,
                                                  self,
                                                  object_id='#bucket_button')

        self.toolOptions = {}
        # Tool Options Param
        self.paletteColor = pygame.Color(255, 255, 255, 255)
        self.brushSize = 16
        self.opacity = 255

        # starting tool
        self.activeTool = ToolBrush(self.paletteColor, self.opacity,
                                    self.brushSize)
