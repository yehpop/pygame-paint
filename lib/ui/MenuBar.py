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
        xPosTopMenu = 0
        for menuKey, menuItem in self.menuData.items():
            # creates top menu buttons
            defaultFont = self.ui_manager.get_theme().get_font_dictionary(
            ).get_default_font()
            itemTextSize = defaultFont.size(menuItem['display_name'])
            UIButton(pygame.Rect(
                (xPosTopMenu, 0),
                (itemTextSize[0] + 16, self.menuBarContainer.rect.height)),
                     menuItem['display_name'],
                     self.ui_manager,
                     self.menuBarContainer,
                     object_id=menuKey,
                     parent_element=self)
            xPosTopMenu += itemTextSize[0] + 16

    # obvious and the code is pretty straightfoward
    def unfocus(self):
        if self.openMenu is not None:
            self.openMenu.kill()
            self.openMenu = None
        if self._selectedMenuButton is not None:
            self._selectedMenuButton.unselect()
            self._selectedMenuButton = None

    # because we have to kill more stuff
    def kill(self):
        self.menuBarContainer.kill()
        super().kill()

    def _open_top_menu(self, event):
        # kill any menu that's already open
        if self.openMenu is not None:
            self.openMenu.kill()
        # open selected top menu
        menuKey = event.ui_object_id.split('.')[-1]
        menuSize = ((len(self.menuData[menuKey]['items']) * 20) + (2 *
                                                                   (0 + 1)))
        itemData = [
            (itemData['display_name'], itemKey)
            for itemKey, itemData in self.menuData[menuKey]['items'].items()
        ]
        menuRect = pygame.Rect((0, 0), (200, menuSize))
        menuRect.topleft = event.ui_element.rect.bottomleft
        topUILayer = self.ui_manager.get_sprite_group().get_top_layer()
        self.openMenu = UISelectionList(menuRect,
                                        itemData,
                                        self.ui_manager,
                                        starting_height=topUILayer,
                                        parent_element=self,
                                        object_id=menuKey + '_items')
        self.ui_manager.set_focus_set(self)

    # open selected sub menu
    def _open_sub_menu(self, event, menuData):
        menuKey = event.ui_object_id.split('.')[-1]
        menuSize = ((len(menuData[menuKey]['items']) * 20) + (2 * (0 + 1)))
        itemData = [
            (itemData['display_name'], itemKey)
            for itemKey, itemData in menuData[menuKey]['items'].items()
        ]
        menuRect = pygame.Rect((0, 0), (200, menuSize))
        menuRect.topleft = event.ui_element.rect.topleft
        topUILayer = self.ui_manager.get_sprite_group().get_top_layer()
        self.openMenu = UISelectionList(menuRect,
                                        itemData,
                                        self.ui_manager,
                                        starting_height=topUILayer,
                                        parent_element=self.openMenu,
                                        object_id=menuKey + '_items')
        self.ui_manager.set_focus_set(self)

    def update(self, timeDelta: float):
        """
        A method called every update cycle of our application. Makes sure the menu's layer 'thickness' is
        accurate and handles window resizing.
        :param time_delta: time passed in seconds between one call to this method and the next.
        """
        super().update(timeDelta)
        if self.menuBarContainer.layer_thickness != self.layer_thickness:
            self.layer_thickness = self.menuBarContainer.layer_thickness

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

    # holy shit annotations are cool
    def process_event(self, event: pygame.event.Event) -> bool:
        """
        Blocks mouse click down events from passing through the menu.
        
        :param event: The event to process.
        :return: Should return True if this element consumes this event.
        """
        eventConsumed = False
        if (self is not None and event.type == pygame.MOUSEBUTTONDOWN
                and event.button in [pygame.BUTTON_LEFT, pygame.BUTTON_RIGHT]):
            scaledMousePos = (int(event.pos[0] *
                                  self.ui_manager.mouse_pos_scale_factor[0]),
                              int(event.pos[1] *
                                  self.ui_manager.mouse_pos_scale_factor[1]))
            if self.hover_point(scaledMousePos[0], scaledMousePos[1]):
                eventConsumed = True

        if (event.type == pygame.USEREVENT
                and event.user_type == gui.UI_BUTTON_ON_HOVERED
                and event.ui_element in self.menuBarContainer.elements
                and self.openMenu != None):
            if self._selectedMenuButton is not None:
                self._selectedMenuButton.unselect()
            self._selectedMenuButton = event.ui_element
            self._selectedMenuButton.select()
            self._open_top_menu(event)
        if (event.type == pygame.USEREVENT
                and event.user_type == gui.UI_BUTTON_START_PRESS
                and event.ui_element in self.menuBarContainer.elements):
            if self._selectedMenuButton is not None:
                self._selectedMenuButton.unselect()
            self._selectedMenuButton = event.ui_element
            self._selectedMenuButton.select()
            self._open_top_menu(event)
        if (event.type == pygame.USEREVENT
                and event.user_type == gui.UI_BUTTON_START_PRESS
                and event.ui_object_id == 'menu_bar.#view_menu_items.#theme'):
            themesData = {
                '#theme': {
                    'display_name': 'Themes',
                    'items': {
                        '#themes_default': {
                            'display_name': 'Default Theme',
                        },
                        '#themes_light': {
                            'display_name': 'Light Theme'
                        },
                        '#themes_dark': {
                            'display_name': 'Dark Theme'
                        }
                    }
                }
            }
            self._open_sub_menu(event, themesData)

        return eventConsumed