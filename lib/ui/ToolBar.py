import pygame
import pygame_gui as gui

from pygame_gui.elements import UIHorizontalSlider, UIButton, UILabel

from lib.tools import ToolBrush
from lib.tools import ToolBucket


class ToolBar(gui.elements.UIWindow):
    def __init__(self, rect, manager):
        super().__init__(rect,
                         manager,
                         "Tools",
                         object_id='#tool_bar',
                         resizable=True)
        # Tool Select Buttons
        brushButtonRect = pygame.Rect((15, 148), (64, 64))
        self.brushButton = UIButton(brushButtonRect,
                                    "",
                                    manager,
                                    self,
                                    object_id='#brush_button')
        bucketButtonRect = pygame.Rect((89, 148), (64, 64))
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

        self.paletteButton = UIButton(pygame.Rect((50, 21), (64, 64)),
                                      '',
                                      self.ui_manager,
                                      self,
                                      object_id='#palette_button')

        self.paletteButton.normal_image = pygame.Surface((58, 58),
                                                         flags=pygame.SRCALPHA,
                                                         depth=32)
        self.paletteButton.normal_image.fill(self.paletteColor)
        self.paletteButton.hovered_image = self.paletteButton.normal_image
        self.paletteButton.selected_image = self.paletteButton.normal_image
        self.paletteButton.rebuild()
        # is it normal that i so much wanna make the 5 lines above a func

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
                """
                so basically there's a dict 'option_data' in the classes of the tools
                and we iterate through the keys of this dict for the tool that is actively
                being used atm of this being called and we modify the tool bar accordingly
                """
                if optionData == 'palette_color':
                    self.toolOptions['palette_label'] = UILabel(
                        pygame.Rect((10, 95), (148, 20)), 'Palette Color',
                        self.ui_manager, self)
                elif optionData == 'opacity':
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

    def get_active_tool(self):
        return self.activeTool

    def set_active_tool(self, tool):
        if tool == 'brush':
            self.activeTool = ToolBrush(self.paletteColor, self.opacity,
                                        self.brushSize)
        if tool == 'bucket':
            self.activeTool = ToolBucket(self.paletteColor, self.opacity)

        self.refresh_tool_options()
        # I am fricking tired of looking into pygame_gui codes GODDD
        pygame.event.post(
            pygame.event.Event(
                pygame.USEREVENT,
                {
                    'user_type': "active_tool_changed",
                    'ui_element': self.most_specific_combined_id,  # wtf tbh
                    'ui_object_id': self,
                    'tool': self.activeTool
                }))

    def process_event(self, event: pygame.event.Event) -> bool:
        """
        This method will overwrite the super class process_event and I didn't
        call super().recall_events(event) bc it seems nicer if the user cant change the size

        :param event: Obvious.
        
        :return bool: False. Thats it, this doesn't consume any event
        """
        if (True):
            pass
        # vscode highlights a bunch of shit blue becase of the return annotation and
        # I did the above to block it... it really annoyed me

        # ↓↓↓ tool buttons ↓↓↓
        if (event.type == pygame.USEREVENT
                and event.user_type == gui.UI_BUTTON_PRESSED
                and event.ui_element == self.brushButton):
            self.set_active_tool('brush')
        if (event.type == pygame.USEREVENT
                and event.user_type == gui.UI_BUTTON_PRESSED
                and event.ui_element == self.bucketButton):
            self.set_active_tool('bucket')

        # ↓↓↓ color palette things ↓↓↓
        if (event.type == pygame.USEREVENT
                and event.user_type == gui.UI_BUTTON_PRESSED
                and event.ui_element == self.paletteButton):
            gui.windows.UIColourPickerDialog(rect=pygame.Rect((100, 200),
                                                              (390, 390)),
                                             manager=self.ui_manager,
                                             initial_colour=self.paletteColor)
        if (event.type == pygame.USEREVENT
                and event.user_type == gui.UI_COLOUR_PICKER_COLOUR_PICKED):
            self.paletteColor = event.colour
            self.activeTool.set_option('palette_color', self.paletteColor)
            self.paletteButton.normal_image = pygame.Surface(
                (58, 58), flags=pygame.SRCALPHA, depth=32)
            self.paletteButton.normal_image.fill(self.paletteColor)
            self.paletteButton.hovered_image = self.paletteButton.normal_image
            self.paletteButton.selected_image = self.paletteButton.normal_image
            self.paletteButton.rebuild()

        # ↓↓↓ sliders ↓↓↓
        if (event.type == pygame.USEREVENT
                and event.user_type == gui.UI_HORIZONTAL_SLIDER_MOVED
                and event.ui_object_id == '#tool_bar.#opacity_slider'):
            self.opacity = int(event.value)
            self.activeTool.set_option('opacity', self.opacity)
        if (event.type == pygame.USEREVENT
                and event.user_type == gui.UI_HORIZONTAL_SLIDER_MOVED
                and event.ui_object_id == '#tool_bar.#brush_size_slider'):
            self.brushSize = int(event.value)
            self.activeTool.set_option('brush_size', self.brushSize)

        # ↓↓↓ extra ↓↓↓
        if self.activeTool is not None:
            self.activeTool.process_event(event)

        return False

    def update(self, timeDelta: float):
        super().update(timeDelta)

        if self.activeTool is not None and self.activeTool.activeCanvas is not None:
            mousePos = self.ui_manager.get_mouse_position()
            if self.activeTool.activeCanvas.hover_point(
                    mousePos[0], mousePos[1]):
                if self.activeTool.activeCanvas.get_image_clipping_rect(
                ) is not None:
                    self.activeTool.update(
                        timeDelta,
                        self.activeTool.activeCanvas._pre_clipped_image,
                        self.activeTool.activeCanvas.rect.topleft,
                        self.activeTool.activeCanvas)
                else:
                    self.activeTool.update(
                        timeDelta, self.activeTool.activeCanvas.image,
                        self.activeTool.activeCanvas.rect.topleft,
                        self.activeTool.activeCanvas)
