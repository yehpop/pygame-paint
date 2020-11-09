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
        self.brushButton = UIButton(brushButtonRect,
                                    "",
                                    manager,
                                    self,
                                    object_id='#brush_button')
        bucketButtonRect = pygame.Rect((89, 132), (64, 64))
        self.bucketButton = UIButton(bucketButtonRect,
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

        self.paletteButton = UIButton(
            pygame.Rect((50, 16), (64, 64)),
            '',
            self.ui_manager,
            self,
        )

        self.paletteButton.normal_image = pygame.Surface((58, 58),
                                                         flags=pygame.SRCALPHA,
                                                         depth=32)
        self.paletteButton.normal_image.fill(self.paletteColor)
        self.paletteButton.hovered_image = self.paletteButton.normal_image
        self.paletteButton.selected_image = self.paletteButton.normal_image
        self.paletteButton.rebuild()

        self.refresh_tool_options()

    def refresh_tool_options(self):
        for key, widget in self.toolOptions.items():
            widget.kill()
        self.toolOptions.clear()

        leftBottomAnchor = {
            'left': 'left',
            'right': 'left',
            'top': 'bottom',
            'bottom': 'bottom'
        }
        if self.activeTool != None:
            yPosCurrent = -166
            self.toolOptions['opacity_label'] = UILabel(
                pygame.Rect((10, yPosCurrent), (148, 20)),
                "Tool Options",
                self.ui_manager,
                self,
                object_id='#tools_options_label',
                anchors=leftBottomAnchor)
            yPosCurrent += 30
            for optionData in self.activeTool.option_data:
                if optionData == 'opacity':
                    self.toolOptions['opacity_label'] = UILabel(
                        pygame.Rect((10, yPosCurrent), (148, 20)),
                        "Opacity: ",
                        self.ui_manager,
                        self,
                        anchors=leftBottomAnchor)
                    yPosCurrent += 20
                    self.toolOptions['opacity_slider'] = UIHorizontalSlider(
                        pygame.Rect((10, yPosCurrent), (148, 20)),
                        self.opacity, (0, 255),
                        self.ui_manager,
                        self,
                        object_id='#opacity_slider',
                        anchors=leftBottomAnchor)
                    yPosCurrent += 25

                elif optionData == 'brush_size':
                    self.toolOptions['brush_size_label'] = UILabel(
                        pygame.Rect((10, yPosCurrent), (148, 20)),
                        "Brush Size:",
                        self.ui_manager,
                        self,
                        anchors=leftBottomAnchor)
                    yPosCurrent += 20
                    self.toolOptions['brush_size_slider'] = UIHorizontalSlider(
                        pygame.Rect((10, yPosCurrent), (148, 20)),
                        self.brushSize, (1, 100),
                        self.ui_manager,
                        self,
                        object_id='#brush_size_slider',
                        anchors=leftBottomAnchor)
                    yPosCurrent += 25
