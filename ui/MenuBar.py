from typing import Union, Dict, Tuple

import pygame
import pygame_gui as gui

from pygame_gui.core.interfaces import IContainerLikeInterface, IUIManagerInterface
from pygame_gui.core import UIElement, UIContainer
from pygame_gui.core.drawable_shapes import RectDrawableShape
from pygame_gui.elements.ui_button import UIButton
from pygame_gui.elements.ui_selection_list import UISelectionList


class MenuBar(UIElement):
    # get ready for loads of parameters
    def __init__(self,
                 rect: pygame.Rect,
                 menuData,
                 manager,
                 container: Union[IContainerLikeInterface, None] = None,
                 parent: Union[UIElement, None] = None,
                 object_id: Union[str, None] = None,
                 anchors: Union[Dict[str, str], None] = None):
        super().__init__(rect,
                         manager,
                         container=container,
                         starting_height=1,
                         layer_thickness=1,
                         anchors=anchors)

        self._create_valid_ids(container=container,
                               parent_element=parent,
                               object_id=object_id,
                               element_id='menu_bar')
        self.menuData = menuData

        self.bgColor = None
        self.borderColor = None
        self.shapeType = 'rectangle'

        self.openMenu = None
        self._selectedMenuButton = None

        self._closeOpenMenu = False

        self.rebuild_from_changed_theme_data()

        # I hate my life
        # yapf: disable
        self.containerRect = pygame.Rect(
            self.relative_rect.left + (self.shadow_width + self.border_width),
            self.relative_rect.top + (self.shadow_width + self.border_width),
            self.relative_rect.width
            - 2 * (self.shadow_width + self.border_width),
            self.relative_rect.height
            - 2 * (self.shadow_width + self.border_width))
        # yapf: enable
        # that was for a parameter of what's coming now lol
        self.menuBarContainer = UIContainer(self.containerRect,
                                            manager,
                                            starting_height=1,
                                            parent_element=self,
                                            object_id='#menu_bar_container')

    def unfocus(self):
        pass

    def __open_top_menu(self, event):
        pass

    def rebuild_from_changed_theme_data(self):
        """
        Checks if any theming parameters have changed, and if so triggers a rebuild
        """
        hasAnyChanged = False

        bgColor = self.ui_theme.get_colour_or_gradient(
            'normal_bg', self.combined_element_ids)
        if bgColor != self.bgColor:
            self.bgColor = bgColor
            hasAnyChanged = True

        borderColor = self.ui_theme.get_colour_or_gradient(
            'normal_border', self.combined_element_ids)
        if borderColor != self.borderColor:
            self.borderColor = borderColor
            hasAnyChanged = True

        # misc
        shapeTypeStr = self.ui_theme.get_misc_data('shape',
                                                   self.combined_element_ids)
        if (shapeTypeStr is not None and shapeTypeStr in ['rectangle']
                and shapeTypeStr != self.shapeType):
            self.shapeType = shapeTypeStr
            hasAnyChanged = True

        if self._check_shape_theming_changed(defaults={
                'border_width': 1,
                'shadow_width': 0,
                'shape_corner_radius': 0
        }):
            hasAnyChanged = True

        if hasAnyChanged:
            self.rebuild()

    def rebuild(self):
        themingParameters = {
            'normal_bg': self.bgColor,
            'normal_border': self.borderColor,
            'border_width': self.border_width,
            'shadow_width': self.shadow_width
        }

        if self.shapeType == 'rectangle':
            self.drawable_shape = RectDrawableShape(self.rect,
                                                    themingParameters,
                                                    ['normal'],
                                                    self.ui_manager)

        self.on_fresh_drawable_shape_ready()